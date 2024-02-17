from __future__ import annotations

import copy
import os
import warnings
from datetime import datetime
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import pytorch_lightning as pl
import torch
from pytorch_lightning import Callback
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import Logger
from pytorch_lightning.utilities.model_summary import ModelSummary

import aixd.data.constants as constants
import aixd.mlmodel.utils_mlmodel as ut
from aixd.data import DataObject, InputML, OutputML
from aixd.data.utils_data import convert_to, get_shape
from aixd.mlmodel.architecture import losses
from aixd.mlmodel.architecture.decoders import Decoder
from aixd.mlmodel.architecture.encoders import Encoder
from aixd.mlmodel.constants import SEP_LOSSES
from aixd.mlmodel.data.data_loader import DataModule
from aixd.mlmodel.utils_mlmodel import rec_concat_dict, to_torch
from aixd.utils import logs
from aixd.utils.utils import basename, dirname

FORMATS_IO = constants.formats_io

warnings.filterwarnings("ignore", ".*does not have many workers.*")
logger = logs.get_logger().get_child("cae-model")


class CondAEModel(pl.LightningModule):
    """
    Class representing a Conditional Autoencoder model.

    Parameters
    ----------
    input_ml_dblock : InputML
        A input ml data block defining the input heads of the model.
    output_ml_dblock : OutputML
        A output ml data block defining the output heads of the model.
    layer_widths : List[int]
        List of integers specifying the number of units in each hidden layer of the autoencoder's encoder and decoder (i.e., the "core" of the autoencoder).
        The first element of the list corresponds to the number of units in the first hidden layer of the encoder, the last element corresponds to the
        number of units in the last hidden layer of the decoder, and the elements in between correspond to the number of units in each hidden layer of
        the autoencoder in the order they appear (encoder followed by decoder).
    latent_dim : int
        Integer specifying the number of units in the latent (i.e., encoded) representation of the data.
    heads_layer_widths : Dict[str, List[int]], optional, default={}
        Dictionary specifying the number of units in the "head" layers that are added to the autoencoder. The keys of the dictionary are the names of the features,
        the values are a sequence of integers specifying the number of units in each hidden layer of the head. Default is an empty dictionary: {}.
    custom_losses : Dict[str, Callable[[torch.Tensor, torch.Tensor], torch.Tensor]], optional, default=None
        Dictionary containing custom losses to be computed on the outputs.
    loss_weights : Dict[str, float], optional, default=None
        Dictionary containing the weights with which each loss term should be multiplied before being added to the total loss used for backpropagation, including custom losses.
    activation : Union[torch.nn.Module, str], optional, default="leaky_relu"
        Activation function to be used in the latent layers of the autoencoder.
    optimizer : torch.optim.Optimizer, optional, default=None
        Optimizer to be used for updating the model's weights.
    pass_y_to_encoder : bool, optional, default=False
        Whether to pass the conditional features 'y' to the autoencoder's encoder (vanilla cVAE formulation) or not.
        If 'True', the encoder maps from 'x' to 'z' and is solely used for finding the latent vector needed to reconstruct 'x' given 'y'.
        In 'False', the encoder represents a surrogate model mapping from 'x' to 'y' as well as a latent vector 'z'.
    name : str, optional, default="CondAEModel"
        Name of the model.
    save_dir : str, optional, default=None
        Directory where the model related files will be saved, such as the models's checkpoint and logs.
    name_proj : str, optional, default=None
        Name of the project. If None, the name of the project is inferred from the save_dir.
    **kwargs : dict
        Additional arguments passed to :class:`pytorch_lightning.core.module.LightningModule`.
    """

    CHECKPOINT_HYPER_PARAMS_EXTRA_KEY = "__hparams_extra__"  # key for extra hyperparameters in checkpoint

    CHECKPOINT_DIR = "checkpoints"

    def __init__(
        self,
        input_ml_dblock: InputML,
        output_ml_dblock: OutputML,
        layer_widths: List[int],
        latent_dim: int,
        heads_layer_widths: Dict[str, List[int]] = {},
        custom_losses: Dict[str, Callable[[torch.Tensor, torch.Tensor], torch.Tensor]] = None,
        loss_weights: Dict[str, float] = None,
        activation: str = "leaky_relu",
        optimizer: torch.optim.Optimizer = None,
        pass_y_to_encoder: bool = False,
        name: str = "CondAEModel",
        save_dir: str = None,
        name_proj: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Save the hyperparameters
        # Ignore the datapath, since it differs between machines
        self.save_hyperparameters(ignore=["save_dir"])

        # Dictionary mapping from input feature names to tuples, where the first element in the tuple is the encoding head to be prepended to the encoder,
        # and the second element is the decoding head to be appended to the decoder.
        self.x_heads = {
            x_dobj.name: x_dobj.get_ml_heads(heads_layer_widths.get(x_dobj.name, []), layer_widths[0], activation, **kwargs) for x_dobj in input_ml_dblock.dobj_list_transf
        }

        # Dictionary mapping from output feature names to tuples, where the first element in the tuple is the encoding head to be prepended to the decoder,
        # and the second element is the decoding head to be appended to the encoder.
        self.y_heads = {
            y_dobj.name: y_dobj.get_ml_heads(heads_layer_widths.get(y_dobj.name, []), layer_widths[-1], activation, **kwargs) for y_dobj in output_ml_dblock.dobj_list_transf
        }

        # Get start and end indices for each feature in the input data vectors
        self.x_splits = {x_dobj.name: (x_dobj.position_index, x_dobj.position_index + x_dobj.dim) for x_dobj in input_ml_dblock.dobj_list_transf}
        self.y_splits = {y_dobj.name: (y_dobj.position_index, y_dobj.position_index + y_dobj.dim) for y_dobj in output_ml_dblock.dobj_list_transf}

        # Build the encoder based on the above head dictionaries. If `pass_y_to_encoder`, the conditional features y are also passed as inputs to the encoder.
        # In this case, the encoder is not tasked with predicting the conditional features y. Otherwise, the encoder is a surrogate model predicting y and z.
        self.encoder = Encoder(
            {x_key: x_heads[0] for x_key, x_heads in (self.x_heads.items() if not pass_y_to_encoder else (self.x_heads | self.y_heads).items())},
            {y_key: y_heads[1] for y_key, y_heads in self.y_heads.items() if not pass_y_to_encoder} if not pass_y_to_encoder else {},
            self.x_splits,
            layer_widths,
            latent_dim,
            activation,
        )
        # Build the decoder based on the above head dictionaries.
        self.decoder = Decoder(
            {y_key: y_heads[0] for y_key, y_heads in self.y_heads.items()},
            {x_key: x_heads[1] for x_key, x_heads in self.x_heads.items()},
            self.y_splits,
            layer_widths[::-1],
            latent_dim,
            activation,
        )

        self.input_ml_dblock = input_ml_dblock
        self.output_ml_dblock = output_ml_dblock

        self.save_dir = save_dir or os.getcwd()
        self.name_proj = name_proj or basename(self.save_dir)

        self.name = name
        self.layer_widths = layer_widths
        self.latent_dim = latent_dim
        self.heads_layer_widths = heads_layer_widths

        self.custom_losses = custom_losses if custom_losses else {}
        self.loss_weights = loss_weights if loss_weights else {}
        self.feature_losses = {dobj.name: dobj.get_objective() for dobj in input_ml_dblock.dobj_list_transf + output_ml_dblock.dobj_list_transf}
        self.losses_evaluate = {dobj.name: dobj.get_loss_evaluation() for dobj in input_ml_dblock.dobj_list_transf + output_ml_dblock.dobj_list_transf}

        self.activation = activation
        self.optimizer = optimizer
        self.pass_y_to_encoder = pass_y_to_encoder

        self.model_trainer = None  # Set in the fit method

        # Attributes to store extra parameters
        self.datamodule_parameters = None
        self.datamodule_checksum = None
        self._hparams_extra = getattr(self, "_hparams_extra", set())

    def configure_optimizers(self):
        """
        Configure the optimizers for the model.

        Returns
        -------
        dict
            A dictionary containing the optimizer(s) and learning rate scheduler(s) to be used during training.
        """
        # Initialize the optimizer with Adam, using the model parameters as the input arguments
        optimizer = self.optimizer if self.optimizer is not None else torch.optim.Adam(self.parameters())

        # Initialize the learning rate scheduler with ReduceLROnPlateau
        # This scheduler reduces the learning rate when the validation loss stops improving
        lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=6, verbose=True)

        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": lr_scheduler,
                "monitor": "val" + SEP_LOSSES + "loss",
            },
        }

    def _step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int, mode: str, step_ae: bool = True) -> Tuple[Dict[str, torch.Tensor], Dict[str, float]]:
        """
        Process a single batch of data.

        Parameters
        ----------
        batch : Tuple[torch.Tensor, torch.Tensor]
            A tuple of tensors containing the data for a single batch.
        batch_idx : int
            The index of the current batch.
        mode: str
            The mode in which the model is being run (either 'train' or 'val').
        step_ae : bool, optional, default=True
            Just to specify if the step is for an AE model or not. If True, the z_loss is computed.

        Returns
        -------
        Tuple[Dict[str, torch.Tensor], Dict[str, float]]
            A tuple where the first element is a dictionary with predictions, and the second element a dictionary with losses for the batch.
        """
        x, y = batch
        pred = self(batch)

        x_pred = {key: pred["x"][:, self.x_splits[key][0] : self.x_splits[key][1]] for key in self.decoder.out_heads.keys()}
        y_pred = {key: pred["y"][:, self.y_splits[key][0] : self.y_splits[key][1]] for key in self.encoder.out_heads.keys()}

        x_real = {key: x[:, self.x_splits[key][0] : self.x_splits[key][1]].float() for key in self.decoder.out_heads.keys()}
        y_real = {key: y[:, self.y_splits[key][0] : self.y_splits[key][1]].float() for key in self.encoder.out_heads.keys()}

        # Calculate the losses for the features in the decoder
        x_losses = {key: self.feature_losses[key](x_pred[key], x_real[key]) for key in self.decoder.out_heads.keys()}
        x_loss = torch.stack(list(x_losses.values()), dim=0).sum()

        # Calculate the losses for the features in the encoder
        y_losses = {key: self.feature_losses[key](y_pred[key], y_real[key]) for key in self.encoder.out_heads.keys()}
        y_loss = torch.stack(list(y_losses.values()), dim=0).sum() if len(y_losses) > 0 else 0.0

        # calculate only if decorrelation weight is > 0 to avoid computing gradients for nothing
        if self.loss_weights.get("decorrelation", 0) > 0 and len(self.encoder.out_heads) > 0:
            # decorrelate by reducing the covariance: https://arxiv.org/abs/1904.01277v1
            decorrelation_loss = ((pred["z"].T @ ((y - y.mean(axis=0)) / y.std(axis=0))) ** 2).mean()
        else:
            # weight is zero, so decorrelation_loss is detached from the graph
            decorrelation_loss = 0.0

        custom_losses = {
            name: self.loss_weights.get(name, 1.0) * custom_loss(x_pred | y_pred | {key: pred[key] for key in pred.keys() if key not in ["x", "y"]}, x_real | y_real)
            for name, custom_loss in self.custom_losses.items()
        }

        total_loss = (
            self.loss_weights.get("x", 1.0) * x_loss
            + self.loss_weights.get("y", 1.0) * y_loss
            + self.loss_weights.get("decorrelation", 0.0) * decorrelation_loss
            + (torch.stack(list(custom_losses.values()), dim=0).sum() if len(self.custom_losses) > 0 else 0)
        )

        loss_dict = (
            {
                mode + SEP_LOSSES + "loss": total_loss,
                mode + SEP_LOSSES + "features_loss": x_loss + y_loss,
                mode + SEP_LOSSES + "decorrelation_loss": decorrelation_loss,
            }
            | {mode + SEP_LOSSES + key + "_loss": value for key, value in x_losses.items()}
            | {mode + SEP_LOSSES + key + "_loss": value for key, value in y_losses.items()}
            | {mode + SEP_LOSSES + key: value for key, value in custom_losses.items()}
        )

        # this could now be moved to custom losses which would restore proper inheritance with VAE (no more step_ae flag)
        if step_ae:
            z_loss = losses.LossStd()(pred["z"])
            total_loss += self.loss_weights.get("z", 1.0) * z_loss
            loss_dict[mode + SEP_LOSSES + "z_loss"] = z_loss

        return pred, loss_dict

    def forward(self, data: Tuple[torch.Tensor, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Forward pass of the model.

        Parameters
        ----------
        data : Tuple[torch.Tensor, torch.Tensor]
            A tuple containing input data tensors, where the first element is 'x' and the second element is the conditional part 'y'.

        Returns
        -------
        Dict[str, torch.Tensor]
            A dictionary containing the model's output tensors. This could include the latent representation 'z', the reconstructed 'y', and the reconstructed 'x'.
        """
        x, y = data

        if self.pass_y_to_encoder:
            pred = self.encoder(torch.cat([x, y], dim=-1))
        else:
            pred = self.encoder(x)

        pred.update(self.decoder({"z": pred["z"], "y": y}))

        return pred

    def training_step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> float:
        """
        Perform a single training step.

        Parameters
        ----------
        batch : Tuple[torch.Tensor, torch.Tensor]
            A tuple containing the data for a single batch.
        batch_idx : int
            The index of the current batch.

        Returns
        -------
        float
            The training loss.
        """
        # Process the batch and retrieve the loss dictionary
        _, loss_dict = self._step(batch, batch_idx, mode="train")

        # Log the loss values to various outputs
        self.log_dict(loss_dict, on_step=True, on_epoch=False, prog_bar=True, logger=True)
        return loss_dict["train" + SEP_LOSSES + "loss"]

    def validation_step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> float:
        """
        Perform a single validation step.

        Parameters
        ----------
        batch : Tuple[torch.Tensor, torch.Tensor]
            A tuple containing the data for a single batch.
        batch_idx : int
            The index of the current batch.

        Returns
        -------
        float
            The validation loss.
        """
        # Process the batch and retrieve the loss dictionary
        _, loss_dict = self._step(batch, batch_idx, mode="val")

        # Log the loss values to various outputs
        self.log_dict(loss_dict, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        return loss_dict["val" + SEP_LOSSES + "loss"]

    def test_step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> float:
        """
        Perform a single test step.

        Parameters
        ----------
        batch : Tuple[torch.Tensor, torch.Tensor]
            A tuple containing the data for a single batch.
        batch_idx : int
            The index of the current batch.

        Returns
        -------
        float
            The test loss.
        """
        # Process the batch and retrieve the loss dictionary
        _, loss_dict = self._step(batch, batch_idx, mode="test")

        # Log the loss values to various outputs
        self.log_dict(loss_dict, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        return loss_dict["test" + SEP_LOSSES + "loss"]

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """
        Encode the input data into a latent representation.

        Parameters
        ----------
        x : torch.Tensor
            The input data.

        Returns
        -------
        torch.Tensor
            A tensor containing the latent representation of the input data.
        """
        return self.encoder(x)

    def decode(self, y: torch.Tensor, z: Union[np.array, torch.Tensor]) -> torch.Tensor:
        """
        Decode the latent representation into the original data space.

        Parameters
        ----------
        y : torch.Tensor
            The conditional data.
        z : Union[np.array, torch.Tensor]
            The latent representation to decode.

        Returns
        -------
        torch.Tensor
            A tensor containing the reconstructed (generated) data.
        """
        if not len(z):
            # Added self.device as it seems it cannot handle the passing to the device in the forward method
            z = torch.normal(mean=0.0, std=1.0, size=(len(y), self.latent_dim)).to(self.device)
        return self.decoder({"z": z.float() if torch.is_tensor(z) else torch.from_numpy(z).float(), "y": y})["x"]

    def forward_evaluation(
        self,
        data: Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor],
        format_out: str = "df",
        input_normalized: bool = False,
        output_normalized: bool = False,
        transform_output: bool = False,
    ) -> Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]:
        """
        Receives some values of inputML, and returns the corresponding outputML,
        as predicted by the model. The data can be provided in any format, and returned also in any format.
        It just relies on the encode method

        Parameters
        ----------
        data : Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]
            Input data to evaluate in the surrogate model
        format_out : str, optional, default="df"
            The format for the returned output. The possible formats are ["dict", "dict_list", "df_per_obj", "df", "array", "torch", "list"], and default is "df".
        input_normalized : bool, optional, default=False
            To indicate if the input data is already normalized
        output_normalized : bool, optional, default=False
            To indicate if the output data should be left normalized when returned
        transform_output : bool, optional, default=False
            If False, the data is returned in the original format of performance attributes, otherwise it is returned in the format of the outputML

        Returns
        -------
        Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]
            The outputML in the indicated format
        """
        if format_out not in FORMATS_IO:
            raise ValueError("The format is not valid. Valid format are: {}".format(", ".join(FORMATS_IO)))

        if isinstance(data, pd.DataFrame):
            data = data.drop(["uid"], axis=1) if "uid" in data.columns else data

        shape_in = get_shape(data)
        if shape_in[1] == len(self.input_ml_dblock.columns_df_transf):
            transform_input = False
        elif shape_in[1] == len(self.input_ml_dblock.columns_df):
            transform_input = True
        else:
            raise ValueError("* The input data does not have the correct number of columns")

        if transform_input:
            data = convert_to(data, format="array", dataobjects=self.input_ml_dblock.dobj_list)
            data, _ = self.input_ml_dblock.transform(data)
        else:
            data = convert_to(data, format="array", dataobjects=self.input_ml_dblock.dobj_list_transf)

        if not input_normalized:
            data = self.input_ml_dblock.normalize(data)

        y_est = self.encode(to_torch(data, torch.float32))["y"].cpu().detach().numpy()

        if not output_normalized:
            y_est = self.output_ml_dblock.unnormalize(y_est)

        if transform_output:
            y_est = convert_to(y_est, format=format_out, dataobjects=self.output_ml_dblock.dobj_list_transf)
        else:
            y_est, _ = self.output_ml_dblock.inverse_transform(y_est)
            y_est = convert_to(y_est, format=format_out, dataobjects=self.output_ml_dblock.dobj_list)

        return y_est

    @staticmethod
    def inverse_design():
        logger.info("To perform inverse design, use the generator class, as this is a more complex process.")

    def _check_datamodule(self, datamodule: DataModule, parameters_only: bool = True) -> DataModule:
        """Some basic checks to make sure that data module is compatible with the model and the corresponding stage."""
        params = datamodule.get_parameters()

        # Check general compatibility. We only check dimensions, so it is still possible that the training/validating/testing will fail.
        input_ml_dblock = params.pop("input_ml_dblock")
        input_ml_checks = (input_ml_dblock.get_dobj_dimensions(flag_transf=True) == self.input_ml_dblock.get_dobj_dimensions(flag_transf=True)) and (
            input_ml_dblock.get_dobj_dimensions(flag_transf=False) == self.input_ml_dblock.get_dobj_dimensions(flag_transf=False)
        )

        output_ml_dblock = params.pop("output_ml_dblock")
        output_ml_checks = (output_ml_dblock.get_dobj_dimensions(flag_transf=True) == self.output_ml_dblock.get_dobj_dimensions(flag_transf=True)) and (
            output_ml_dblock.get_dobj_dimensions(flag_transf=False) == self.output_ml_dblock.get_dobj_dimensions(flag_transf=False)
        )
        if not (input_ml_checks and output_ml_checks):
            raise ValueError(
                "The input_ml and output_ml of the model and the datamodule are not compatible. "
                "Make sure that the model was initialized with the same input_ml and output_ml as the datamodule e.g., with CondAEModel.from_datamodule(...)."
            )

        if self.datamodule_parameters is not None:
            # Check that the other datamodule parameters are the same as the ones used to initialize the model
            datamodule_params = copy.deepcopy(self.datamodule_parameters)
            datamodule_params.pop("input_ml_dblock")
            datamodule_params.pop("output_ml_dblock")

            # Check that the datamodule parameters are the same as the ones used to initialize the model
            if datamodule_params != params:
                raise ValueError(
                    "The datamodule parameters are not the same as the ones used to initialize the model. "
                    "Make sure that the model was initialized with the same parameters as the datamodule e.g., with CondAEModel.from_datamodule(...)."
                )

        # Check that the data of the datamodule has not changed since the model was initialized
        if self.datamodule_checksum is not None and not parameters_only and self.datamodule_checksum != datamodule.get_checksum():
            warnings.warn("The data of the DataModule has changed since the model was initialized. This may lead to inaccurate validation and test results.")

        return datamodule

    def fit(
        self,
        datamodule: DataModule,
        name_run: Optional[str] = "NoName",
        max_epochs: int = 100,
        callbacks: Optional[Union[Callback, List[Callback]]] = None,
        loggers: Optional[Union[Logger, Iterable[Logger]]] = None,
        accelerator: str = "auto",
        flag_early_stop: bool = False,
        criteria: str = "train" + SEP_LOSSES + "loss",
        flag_wandb: bool = False,
        **kwargs,
    ) -> None:
        """
        Train the model on the provided data using PyTorch Lightning's Trainer.

        Parameters
        ----------
        datamodule : pl.LightningDataModule
            The data module object that provides the training, validation, and test data.
        name_run : str, optional, default="NoName"
            Name of the current run, used for logging and saving checkpoints. Not used if flag_wandb is True.
        max_epochs : int, optional, default=100
            The maximum number of epochs to train the model.
        callbacks : Union[Callback, List[Callback]], optional, default=None
            List of callbacks or a single callback to be used during training.
        loggers : Union[Logger, Iterable[Logger]], optional, default=None
            List of logger instances or a single logger for logging training progress and metrics.
        accelerator : str, optional, default="auto"
            Supports passing different accelerator types ("cpu", "gpu", "tpu", "ipu", "hpu", "mps", "auto").
        flag_early_stop : bool, optional, default=False
            If True, enable early stopping based on the provided criteria.
        criteria : str, optional, default="train{`aixd.mlmodel.constants.SEP_LOSSES`}loss"
            The criteria used for early stopping.
        flag_wandb : bool, optional, default=False
            If True, enable logging using Weights & Biases (wandb).
        **kwargs
            Additional keyword arguments that can be passed to the Trainer. Default is an empty dictionary.
        """
        datamodule = self._check_datamodule(datamodule, parameters_only=False)

        if isinstance(callbacks, Callback):
            callbacks = [callbacks]
        callbacks = callbacks or []  # if callbacks is None set to empty list

        # Save some extra parameters
        self.save_extra_parameters(**{"max_epochs": max_epochs, "flag_early_stop": flag_early_stop, "criteria": criteria})

        if loggers is not None and flag_wandb:
            warnings.warn("Both loggers and flag_wandb are set. flag_wandb is ignored.")
            flag_wandb = False

        if flag_wandb:
            from pytorch_lightning.loggers.wandb import WandbLogger

            loggers = WandbLogger(project=self.name_proj, save_dir=self.save_dir)
            name_run = loggers.version  # WandB defines the name of the run by the version number

            # Saving extra parameters to wandb
            loggers.log_hyperparams({key: getattr(self, key) for key in self._hparams_extra})
            loggers.log_hyperparams({"datamodule_parameters": datamodule.get_parameters()})

        # Setup checkpoint callback
        name_run = name_run or "NoName"
        checkpoint_filename = self._checkpoint_filename(name_run, n_samples=len(datamodule.x_train))

        # If there is already a last checkpoint, its name is changed
        if os.path.exists(os.path.join(self.save_dir, self.CHECKPOINT_DIR, "last.ckpt")):
            date_f = self._get_file_creation_date(os.path.join(self.save_dir, self.CHECKPOINT_DIR, "last.ckpt"))
            os.rename(os.path.join(self.save_dir, self.CHECKPOINT_DIR, "last.ckpt"), os.path.join(self.save_dir, self.CHECKPOINT_DIR, "last_" + date_f + ".ckpt"))

        callbacks.append(
            ModelCheckpoint(
                monitor=criteria,
                save_top_k=2,
                mode="min",
                auto_insert_metric_name=False,
                save_last=True,
                dirpath=os.path.join(self.save_dir, self.CHECKPOINT_DIR),
                filename=checkpoint_filename,
            )
        )

        # Setup early stopping callback
        if flag_early_stop:
            from pytorch_lightning.callbacks.early_stopping import EarlyStopping

            if any(isinstance(callback, EarlyStopping) for callback in callbacks):
                warnings.warn("EarlyStopping is already in callbacks, and is not added again.")
                pass
            else:
                callbacks.append(EarlyStopping(monitor=criteria, mode="min", patience=8))

        # Create a model_trainer object and fit the model
        self.model_trainer = pl.Trainer(
            accelerator=accelerator,
            max_epochs=max_epochs,
            callbacks=callbacks,
            logger=loggers if loggers else None,
            default_root_dir=self.save_dir,
            **kwargs,
        )
        self.model_trainer.fit(self, datamodule=datamodule)

        if flag_wandb:
            import wandb

            wandb.finish()

    def validate(self, datamodule: DataModule, accelerator: str = "auto", **kwargs) -> Dict[str, float]:
        """
        Evaluate the model on the validation data.

        Parameters
        ----------
        datamodule : DataModule
            The data module object that provides validation data.
        accelerator : str, optional, default="auto"
            Supports passing different accelerator types ("cpu", "gpu", "tpu", "ipu", "hpu", "mps", "auto").

        Returns
        -------
        Dict[str, float]
            A dictionary containing the validation loss and metrics.
        """
        datamodule = self._check_datamodule(datamodule, parameters_only=False)

        # Create a model_trainer object if one does not already exist
        if self.model_trainer is None:
            self.model_trainer = pl.Trainer(accelerator=accelerator, default_root_dir=self.save_dir, **kwargs)

        return rec_concat_dict(self.model_trainer.validate(self, datamodule=datamodule))

    def evaluate(self, datamodule: DataModule, unnormalize: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Evaluate the model on the validation data. This method is similar to :meth:`CondAEModel.validate`, but it uses DataObject.get_loss_evaluation() instead
        of DataObject.get_objective() to compute the losses. It computes the losses per sample rather than summing/averaging them over the entire validation set.

        Parameters
        ----------
        datamodule : DataModule
            The data module object that provides validation data.
        unnormalize : bool, optional, default=False
            If True, the losses are computed in the unnormalized space.

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]
            A tuple containing the evaluation losses for the input and output features, as well as
            the values predicted for input and output features.

        Notes
        -----
        This method, for now, only works on CPU, as the unnormalization is done on the CPU.
        """
        datamodule = self._check_datamodule(datamodule, parameters_only=False)

        self.eval()
        self.to("cpu")  # we need to move the model to CPU, as the un-normalization is done on the CPU
        with torch.no_grad():
            preds, x_eval_losses, y_eval_losses = [], [], []
            for k, batch in enumerate(datamodule.val_dataloader()):
                # Forward pass
                x, y = batch
                pred = self(batch)

                if unnormalize:  # If True, we compute the losses in the unnormalized space
                    pred["x"], pred["y"] = datamodule.unnormalize(pred["x"], pred["y"])
                    x, y = datamodule.unnormalize(x, y)

                # Split and evaluate the losses for all the heads
                x_pred = {key: pred["x"][:, self.x_splits[key][0] : self.x_splits[key][1]] for key in self.decoder.out_heads.keys()}
                y_pred = {key: pred["y"][:, self.y_splits[key][0] : self.y_splits[key][1]] for key in self.encoder.out_heads.keys()}
                x_real = {key: x[:, self.x_splits[key][0] : self.x_splits[key][1]].float() for key in self.decoder.out_heads.keys()}
                y_real = {key: y[:, self.y_splits[key][0] : self.y_splits[key][1]].float() for key in self.encoder.out_heads.keys()}

                x_eval_loss = {key: self.losses_evaluate[key](x_pred[key], x_real[key]) for key in self.decoder.out_heads.keys()}
                y_eval_loss = {key: self.losses_evaluate[key](y_pred[key], y_real[key]) for key in self.encoder.out_heads.keys()}

                # Append the losses for the current batch
                preds.append(pred)
                x_eval_losses.append(x_eval_loss)
                y_eval_losses.append(y_eval_loss)

        # Concatenate the predictions for all the batches, and convert to pandas DataFrame
        preds = rec_concat_dict(preds)
        x_pred = pd.DataFrame(preds["x"].cpu().detach().numpy(), columns=self.input_ml_dblock.columns_df_transf)
        y_pred = pd.DataFrame(preds["y"].cpu().detach().numpy(), columns=self.output_ml_dblock.columns_df_transf)

        # Concatenate the losses for all the batches, and convert to pandas DataFrame
        # For evaluation losses of data objects of dim n, we assume that the losses are of shape (batch_size, n) or (batch_size, 1)
        x_eval_losses = self._to_loss_dataframe(rec_concat_dict(x_eval_losses), self.input_ml_dblock.dobj_list_transf)
        y_eval_losses = self._to_loss_dataframe(rec_concat_dict(y_eval_losses), self.output_ml_dblock.dobj_list_transf)

        return x_eval_losses, y_eval_losses, x_pred, y_pred

    @staticmethod
    def _to_loss_dataframe(loss_dict: Dict[str, torch.Tensor], dobj_list: List[DataObject]) -> pd.DataFrame:
        """Converts a dictionary of losses to a pandas DataFrame, by inferring the column names from the data objects."""
        dobj_dict = {dobj.name: dobj for dobj in dobj_list}
        loss_dict = {key: loss if len(loss.size()) > 1 else loss.unsqueeze(-1) for key, loss in loss_dict.items()}

        if set(dobj_dict.keys()) != set(loss_dict.keys()):
            raise ValueError(f"Losses dictionary keys do not match the data objects. Expected keys are {set(dobj_dict.keys())}, but got {set(loss_dict.keys())}.")

        columns = []
        for key, loss in loss_dict.items():
            if loss.size(1) == dobj_dict[key].dim:
                columns.extend(dobj_dict[key].columns_df)
            elif loss.size(1) == 1:
                columns.append(dobj_dict[key].name)
            else:
                raise ValueError(f"Loss tensor has wrong shape. Expected shape is (*, {dobj_dict[key].dim}) or (*, 1), but got (*, {loss.size(1)}).")

        return pd.DataFrame(torch.cat(list(loss_dict.values()), dim=1).cpu().detach().numpy(), columns=columns)

    def test(self, datamodule: DataModule, accelerator: str = "auto", **kwargs) -> Dict[str, float]:
        """
        Evaluate the model on the test data.

        Parameters
        ----------
        datamodule : DataModule
            A compatible data module object that provides test data.
        accelerator : str, optional, default="auto"
            Which accelerator should be used (e.g. cpu, gpu, mps, etc.).

        Returns
        -------
        Dict[str, float]
            A dictionary containing the test loss and metrics.
        """
        datamodule = self._check_datamodule(datamodule, parameters_only=False)

        # Create a model_trainer object if one does not already exist
        if self.model_trainer is None:
            self.model_trainer = pl.Trainer(accelerator=accelerator, default_root_dir=self.save_dir, **kwargs)

        return rec_concat_dict(self.model_trainer.test(self, datamodule=datamodule))

    def predict(self, data: Union[DataModule, Tuple[torch.Tensor, torch.Tensor], Tuple[np.ndarray, np.ndarray]], accelerator: str = "auto", **kwargs) -> Dict[str, Any]:
        """
        Make predictions using the model.

        Parameters
        ----------
        data : Union[DataModule, Tuple[torch.Tensor, torch.Tensor], Tuple[np.array, np.array]]
            A PyTorch DataModule object, or a tuple of two PyTorch Tensors, or a tuple of two numpy arrays, containing data from which to make predictions.
        accelerator : str, optional, default="auto"
            Which accelerator should be used (e.g. cpu, gpu, mps, etc.).
        **kwargs
            Additional keyword arguments that can be passed to the Trainer. Default is an empty dictionary.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the model's predictions.
        """
        if isinstance(data, DataModule):
            datamodule = data
        elif isinstance(data, tuple):
            x, y = data
            if self.datamodule_parameters is None:
                raise ValueError("The model was not initialized from a DataModule, so the data module can not be recovered.")
            datamodule = DataModule.from_parameters(x, y, predict=True, **self.datamodule_parameters)
        else:
            raise ValueError("The data argument must be a DataModule or a tuple of two tensors or numpy arrays.")

        datamodule = self._check_datamodule(datamodule)

        pred = pl.Trainer(accelerator=accelerator, default_root_dir=self.save_dir, **kwargs).predict(self, datamodule=datamodule)
        pred = rec_concat_dict(pred)

        return self._to_prediction(pred, datamodule)

    @staticmethod
    def _to_prediction(pred: Dict[str, torch.Tensor], datamodule: DataModule) -> Dict[str, Any]:
        """Helper method to convert the model's predictions to the original data space."""
        x_pred_unnorm, y_pred_unnorm = datamodule.unnormalize(pred["x"], pred["y"])
        x_pred_org_space, _ = datamodule.input_ml_dblock.inverse_transform(x_pred_unnorm)
        y_pred_org_space, _ = datamodule.output_ml_dblock.inverse_transform(y_pred_unnorm)

        # TODO: maisseal, how to name the keys of the dictionary? Will be solve with issue #94
        return pred | {"x_org_space": x_pred_org_space, "y_org_space": y_pred_org_space}

    def summary(self, max_depth: int = 1, flag_print: bool = True) -> Union[str, None]:
        """
        Prints a summary of the encoder and decoder, including the number of parameters, the layers,
        their names, and the dimensionality.

        Parameters
        ----------
        max_depth : int, optional, default=1
            Maximum depth of modules to show. Use -1 to show all modules or 0 to show no summary.
        flag_print : bool, optional, default=True
            If True, print the summary to the console. Otherwise, return the summary as a string.
        """
        # Register example input array such that ModelSummary can print data shapes
        self.example_input_array = (
            (
                torch.zeros(1, max([x_dobj.position_index + x_dobj.dim for x_dobj in self.input_ml_dblock.dobj_list_transf])),
                torch.zeros(1, max([y_dobj.position_index + y_dobj.dim for y_dobj in self.output_ml_dblock.dobj_list_transf])),
            ),
        )
        if flag_print:
            print(ModelSummary(self, max_depth=max_depth))
        else:
            return str(ModelSummary(self, max_depth=max_depth))

    @classmethod
    def from_datamodule(cls, datamodule: DataModule, **kwargs) -> CondAEModel:
        """
        Create a model from a data module.

        Parameters
        ----------
        datamodule : DataModule
            The data module object that provides the training, validation, and test data.
        **kwargs
            Additional keyword arguments that can be passed to the model. See CondAEModel.__init__() for more details.

        Returns
        -------
        CondAEModel
            The model object.

        """
        model = cls(input_ml_dblock=datamodule.input_ml_dblock, output_ml_dblock=datamodule.output_ml_dblock, **kwargs)
        model.datamodule_parameters = datamodule.get_parameters()
        model.datamodule_checksum = datamodule.get_checksum()
        return model

    def save_extra_parameters(self, *args: Any, **kwargs) -> None:
        """
        Extra parameters that are saved as part of the model checkpoint. All extra parameters need to be in self.
        One can save extra parameters not yet in self by passing them in kwargs, which will be added to self and self._extra_hparams.

        Parameters
        ----------
        **args : Any
            Extra parameters passed in args need to be in self.
        **kwargs
            Extra parameters passed in kwargs, does not need to be in self.
        """

        for arg in args:
            # Hyperparameters passed in args need to be in self
            if isinstance(arg, str) and hasattr(self, arg):
                self._hparams_extra.add(arg)
            else:
                raise ValueError("Argument {} is not a valid attribute of the model".format(arg))

        # Save kwargs, does not need to be in self, but will be added to self and self._extra_hparams
        for key, value in kwargs.items():
            setattr(self, key, value)
            self._hparams_extra.add(key)

    def on_save_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        """
        Save the extra hyperparameters to the model checkpoint.

        Parameters
        ----------
        checkpoint : Dict[str, Any]
            The full checkpoint dictionary before it gets dumped to a file.
        """
        checkpoint["datamodule_parameters"] = getattr(self, "datamodule_parameters", None)
        checkpoint["datamodule_checksum"] = getattr(self, "datamodule_checksum", None)  # This is neither a datamodule parameter nor a hyperparameter of the model
        checkpoint[self.CHECKPOINT_HYPER_PARAMS_EXTRA_KEY] = {k: getattr(self, k) for k in self._hparams_extra}

        super().on_save_checkpoint(checkpoint)

    def on_load_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        """
        Load the extra hyperparameters from the model checkpoint. The data module parameters are also loaded, if they exist.

        Parameters
        ----------
        checkpoint : Dict[str, Any]
            Loaded checkpoint.
        """
        self.datamodule_parameters = checkpoint.get("datamodule_parameters", None)
        self.datamodule_checksum = checkpoint.get("datamodule_checksum", None)
        for k, v in checkpoint[self.CHECKPOINT_HYPER_PARAMS_EXTRA_KEY].items():
            setattr(self, k, v)

        super().on_load_checkpoint(checkpoint)

    @classmethod
    def load_model_from_checkpoint(cls, path: str, **model_kwargs) -> CondAEModel:
        """
        Load a model from a checkpoint file. If the checkpoint is in the default checkpoint directory, then the data path is restored.

        Parameters
        ----------
        path : str
            The path to the checkpoint file.
        **model_kwargs
            Additional keyword arguments that can be passed to the model. See CondAEModel.__init__() for more details.

        Returns
        -------
        CondAEModel
            The loaded model object.

        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Checkpoint file {path} does not exist.")

        if "save_dir" in model_kwargs:
            save_dir = model_kwargs.pop("save_dir")
        elif basename(dirname(path)) == cls.CHECKPOINT_DIR:
            # If the checkpoint is in the default checkpoint directory, then the data path is the parent directory
            save_dir = dirname(dirname(path))
        else:
            save_dir = os.getcwd()
            warnings.warn(f"Checkpoint file {path} is not in the default checkpoint directory. The data path can not be restored, so it will be set to os.getcwd().")

        return cls.load_from_checkpoint(path, save_dir=save_dir, **model_kwargs)

    @staticmethod
    def _checkpoint_filename(name_run: str, n_samples: int, timestamp=True) -> str:
        """
        Generate a checkpoint filename based on the given name and an optional timestamp.

        Parameters
        ----------
        name_run : str
            The name of the run.
        n_samples : int
            The number of samples used for training.
        timestamp : bool, optional, default=True
            If True, append a timestamp to the filename.

        Returns
        -------
        str
            The checkpoint filename.
        """
        filename = f"{name_run}_{ut.timestamp_to_string()}" if timestamp else name_run
        filename += f"_NSamples_{n_samples}"

        return ut.check_filename(filename) + "_epoch_{epoch}_val_loss_{val/loss:.3E}"

    @staticmethod
    def _get_file_creation_date(file_path, time_fmt="%Y-%m-%d_%H-%M"):
        """Auxiliary function to check the creation date of a file."""
        # Get the file creation time in seconds since the epoch
        creation_time = os.path.getmtime(file_path)

        # Convert the creation time to a datetime object
        creation_date = datetime.fromtimestamp(creation_time)

        # Format the datetime object as a string in the desired format
        formatted_date = creation_date.strftime(time_fmt)

        return formatted_date
