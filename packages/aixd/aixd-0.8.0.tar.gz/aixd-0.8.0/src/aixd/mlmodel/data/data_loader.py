import hashlib
import inspect
import warnings
from typing import List, Tuple, Union

import numpy as np
import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader
from torch.utils.data import Dataset as TorchDataset
from torch.utils.data import random_split

from aixd.data import Dataset, InputML, OutputML
from aixd.data.data_blocks import DataBlockNormalization
from aixd.mlmodel.constants import RANDOM_SEED_SPLIT
from aixd.mlmodel.utils_mlmodel import apply_numpy_func, to_numpy, to_torch


class _Data(TorchDataset):
    """This is just a convenience class to create a torch dataset that is used with the dataloader."""

    def __init__(self, x, y):
        self.x = to_torch(x)
        self.y = to_torch(y)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


class DataModule(pl.LightningDataModule):
    """
    Data module for the ML model. It takes care of splitting the data into train, val and test sets, normalizing the data.

    Parameters
    ----------
    x : Union[np.ndarray, torch.Tensor]
        The input fata matrix.
    y : Union[np.ndarray, torch.Tensor]
        The output data matrix.
    input_ml_dblock : InputML
        Input data block, defining normalizations, the type of the input data, and the heads for the ML model.
    output_ml_dblock : OutputML
        Output data block, defining normalizations, the type of the output data, and the heads for the ML model.
    batch_size : int, optional
        Batch size. The default is 512.
    split_ratios : List[Union[int, float]], optional
        List of ratios for splitting the data into train, val and test sets. The default is [0.8, 0.1, 0.1].
    random_seed : int, optional
        Random seed for splitting the data. The default is RANDOM_SEED_SPLIT.
    predict : bool, optional
        Whether to create a predict set. The default is False.

    """

    def __init__(
        self,
        x: Union[np.ndarray, torch.Tensor],
        y: Union[np.ndarray, torch.Tensor],
        input_ml_dblock: InputML,
        output_ml_dblock: OutputML,
        batch_size: int = 512,
        split_ratios: List[Union[int, float]] = None,
        random_seed: int = RANDOM_SEED_SPLIT,
        predict: bool = False,
    ):
        super().__init__()

        self.input_ml_dblock = input_ml_dblock
        self.output_ml_dblock = output_ml_dblock

        self.batch_size = batch_size
        self.split_ratios = split_ratios or [0.8, 0.1, 0.1]
        self.random_seed = random_seed

        self._setup_data(x, y, predict)

    def _setup_data(self, x: Union[np.ndarray, torch.Tensor], y: Union[np.ndarray, torch.Tensor], predict: bool = False):
        """
        Splits the data into train, val and test sets. If predict is True, then only the predict set is created.
        Applies normalizations according to the input and output data blocks.
        """
        x, y = self._check_data_types(x), self._check_data_types(y)

        x, _ = self.input_ml_dblock.transform(x)
        y, _ = self.output_ml_dblock.transform(y)

        # Check that the input and output data have the correct number of columns
        self._check_input_output_ml_sizes(x, y)

        # Convert to np.float32
        x, y = x.astype(np.float32), y.astype(np.float32)

        if not predict:
            train_data, val_data, test_data = random_split(
                _Data(x, y),
                self.split_ratios,
                generator=torch.Generator().manual_seed(self.random_seed),
            )
            # Normalization is fitted only once
            self._train_data = self._normalize_data(train_data)
            self._val_data = self._normalize_data(val_data)
            self._test_data = self._normalize_data(test_data)

        else:
            # Assumes that normalizations are already fitted
            if not (self.input_ml_dblock.normalization_is_fitted() and self.output_ml_dblock.normalization_is_fitted()):
                raise ValueError("If predict is True, then the input and output data blocks must have fitted normalizations.")
            self._predict_data = self._normalize_data(_Data(x, y))

    @staticmethod
    def _check_data_types(data: Union[np.ndarray, torch.Tensor]) -> np.ndarray:
        """Checks the type of the data."""
        if isinstance(data, (np.ndarray, np.generic)):
            return data
        elif isinstance(data, torch.Tensor):
            return data.float().cpu().detach().numpy()
        else:
            raise TypeError("Data must be of type torch.Tensor or np.ndarray")

    def _check_input_output_ml_sizes(self, x: np.ndarray, y: np.ndarray):
        """Checks that the input and output data have the correct number of columns."""
        expected_size_x = sum([dobj.dim for dobj in self.input_ml_dblock.dobj_list_transf])
        expected_size_y = sum([dobj.dim for dobj in self.output_ml_dblock.dobj_list_transf])

        size_x = x.shape[1]
        size_y = y.shape[1]

        if size_x != expected_size_x:
            raise ValueError(f"Input data has {size_x} columns, but {expected_size_x} were expected. ")
        if size_y != expected_size_y:
            raise ValueError(f"Output data has {size_y} columns, but {expected_size_y} were expected. ")

    def _normalize_data(self, data: _Data) -> _Data:
        x, y = data[: len(data)]
        return _Data(*self.normalize(x, y))

    def _unnormalize_data(self, data: _Data) -> _Data:
        x, y = data[: len(data)]
        return _Data(*self.unnormalize(x, y))

    def print_ml_configuration(self):
        # TODO: maissel, implement something similar as we had before on the dataset to print the input and output configuration of the model
        raise NotImplementedError()

    @property
    def x(self) -> np.ndarray:
        """Returns the transformed and normalized input data."""
        return np.concatenate([self.x_train, self.x_val, self.x_test], axis=0)

    @property
    def y(self) -> np.ndarray:
        """Returns the transformed and normalized output data."""
        return np.concatenate([self.y_train, self.y_val, self.y_test], axis=0)

    @property
    def y_train(self) -> np.ndarray:
        """Returns the transformed and normalized training output data."""
        if not hasattr(self, "_train_data"):
            raise AttributeError("Training data is not available. You must set predict=False when creating the data module.")
        return to_numpy(self._train_data.y)

    @property
    def x_train(self) -> np.ndarray:
        """Returns the transformed and normalized training input data."""
        if not hasattr(self, "_train_data"):
            raise AttributeError("Training data is not available. You must set predict=False when creating the data module.")
        return to_numpy(self._train_data.x)

    @property
    def y_val(self) -> np.ndarray:
        """Returns the transformed and normalized validation output data."""
        if not hasattr(self, "_val_data"):
            raise AttributeError("Validation data is not available. You must set predict=False when creating the data module.")

        return to_numpy(self._val_data.y)

    @property
    def x_val(self) -> np.ndarray:
        """Returns the transformed and normalized validation input data."""
        if not hasattr(self, "_val_data"):
            raise AttributeError("Validation data is not available. You must set predict=False when creating the data module.")

        return to_numpy(self._val_data.x)

    @property
    def y_test(self) -> np.ndarray:
        """Returns the transformed and normalized test output data."""
        if not hasattr(self, "_test_data"):
            raise AttributeError("Test data is not available. You must set predict=False when creating the data module.")

        return to_numpy(self._test_data.y)

    @property
    def x_test(self) -> np.ndarray:
        """Returns the transformed and normalized test input data."""
        if not hasattr(self, "_test_data"):
            raise AttributeError("Test data is not available. You must set predict=False when creating the data module.")
        return to_numpy(self._test_data.x)

    def normalize(self, x: Union[np.ndarray, torch.Tensor], y: Union[np.ndarray, torch.Tensor]) -> Tuple[Union[np.ndarray, torch.Tensor], Union[np.ndarray, torch.Tensor]]:
        """
        Normalize the input and output data. Takes care of the case where x and y are numpy arrays or torch tensors.

        Parameters
        ----------
        x : Union[np.ndarray, torch.Tensor]
            Input data to be normalized, either a numpy array or a torch tensor.
        y : Union[np.ndarray, torch.Tensor]
            Output data to be normalized, either a numpy array or a torch tensor.

        Returns
        -------
        Tuple[Union[np.ndarray, torch.Tensor], Union[np.ndarray, torch.Tensor]]
            A tuple containing the normalized input and output data.

        """
        return self.normalize_x(x), self.normalize_y(y)

    def unnormalize(self, x: Union[np.ndarray, torch.Tensor], y: Union[np.ndarray, torch.Tensor]) -> Tuple[Union[np.ndarray, torch.Tensor], Union[np.ndarray, torch.Tensor]]:
        """
        Unnormalize the input and output data. Takes care of the case where x and y are numpy arrays or torch tensors.

        Parameters
        ----------
        x : Union[np.ndarray, torch.Tensor]
            Input data to be unnormalized, either a numpy array or a torch tensor.
        y : Union[np.ndarray, torch.Tensor]
            Output data to be unnormalized, either a numpy array or a torch tensor.

        Returns
        -------
        Tuple[Union[np.ndarray, torch.Tensor], Union[np.ndarray, torch.Tensor]]
            A tuple containing the unnormalized input and output data.

        """
        return self.unnormalize_x(x), self.unnormalize_y(y)

    def normalize_x(self, x: Union[torch.Tensor, np.ndarray]) -> Union[torch.Tensor, np.ndarray]:
        """
        Normalize only the input data. Takes care of the case where x is a numpy array or a torch tensor.

        Parameters
        ----------
        x : Union[torch.Tensor, np.ndarray]
            A numpy array or a torch tensor to be normalized.

        Returns
        -------
        Union[torch.Tensor, np.ndarray]
            The normalized data. The output has the same type as the input.

        """
        return apply_numpy_func(x, self.input_ml_dblock.normalize)

    def unnormalize_x(self, x: Union[torch.Tensor, np.ndarray]) -> Union[torch.Tensor, np.ndarray]:
        """
        Unnormalize only the input data. Takes care of the case where x is a numpy array or a torch tensor.

        Parameters
        ----------
        x : Union[torch.Tensor, np.ndarray]
            A numpy array or a torch tensor to be unnormalized.

        Returns
        -------
        Union[torch.Tensor, np.ndarray]
            The unnormalized data. The output has the same type as the input.

        """
        return apply_numpy_func(x, self.input_ml_dblock.unnormalize)

    def unnorm_inv_transf_x(self, x: Union[torch.Tensor, np.ndarray]) -> Union[torch.Tensor, np.ndarray]:
        """
        Unnormalize and do the inverse transformation of the data.
        Takes care of the case where y is a numpy array or a torch tensor.

        Parameters
        ----------
        x : Union[torch.Tensor, np.ndarray]
            A numpy array or a torch tensor to be unnormalized.

        Returns
        -------
        Union[torch.Tensor, np.ndarray]
            The unnormalized data. The output has the same type as the input.

        """
        return apply_numpy_func(apply_numpy_func(x, self.input_ml_dblock.unnormalize), self.input_ml_dblock.inverse_transform)[0]

    def normalize_y(self, y: Union[torch.Tensor, np.ndarray]) -> Union[torch.Tensor, np.ndarray]:
        """
        Normalize only the output data. Takes care of the case where y is a numpy array or a torch tensor.

        Parameters
        ----------
        y : Union[torch.Tensor, np.ndarray]
            A numpy array or a torch tensor to be normalized.

        Returns
        -------
        Union[torch.Tensor, np.ndarray]
            The normalized data. The output has the same type as the input.

        """
        return apply_numpy_func(y, self.output_ml_dblock.normalize)

    def unnormalize_y(self, y: Union[torch.Tensor, np.ndarray]) -> Union[torch.Tensor, np.ndarray]:
        """
        Unnormalize only the output data. Takes care of the case where y is a numpy array or a torch tensor.

        Parameters
        ----------
        y : Union[torch.Tensor, np.ndarray]
            A numpy array or a torch tensor to be unnormalized.

        Returns
        -------
        Union[torch.Tensor, np.ndarray]
            The unnormalized data. The output has the same type as the input.

        """
        return apply_numpy_func(y, self.output_ml_dblock.unnormalize)

    def unnorm_inv_transf_y(self, y: Union[torch.Tensor, np.ndarray]) -> Union[torch.Tensor, np.ndarray]:
        """
        Unnormalize and do the inverse transformation of the data.
        Takes care of the case where y is a numpy array or a torch tensor.

        Parameters
        ----------
        y : Union[torch.Tensor, np.ndarray]
            A numpy array or a torch tensor to be unnormalized.

        Returns
        -------
        Union[torch.Tensor, np.ndarray]
            The unnormalized data. The output has the same type as the input.

        """
        return apply_numpy_func(apply_numpy_func(y, self.output_ml_dblock.unnormalize), self.output_ml_dblock.inverse_transform)[0]

    def _adjust_batch_size(self, data: _Data, mode: str):
        batch_size = self.batch_size
        if len(data) < batch_size:
            batch_size = len(data)
            warnings.warn(f"Batch size was adjusted from {self.batch_size} to {batch_size} for {mode} dataloader.")
        return batch_size

    def train_dataloader(self):
        return DataLoader(
            self._train_data,
            batch_size=self._adjust_batch_size(self._train_data, "training"),
            shuffle=True,
            drop_last=True,
            pin_memory=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self._val_data,
            batch_size=self._adjust_batch_size(self._val_data, "validation"),
            shuffle=False,
            drop_last=False,
            pin_memory=True,
        )

    def test_dataloader(self):
        return DataLoader(
            self._test_data,
            batch_size=self._adjust_batch_size(self._test_data, "testing"),
            shuffle=False,
            drop_last=True,
            pin_memory=True,
        )

    def predict_dataloader(self):
        return DataLoader(
            self._predict_data,
            batch_size=self._adjust_batch_size(self._predict_data, "prediction"),
            shuffle=False,
            drop_last=False,
        )

    def get_parameters(self):
        """Get parameters defining the data module."""
        params = {name: getattr(self, name) for name in inspect.signature(self.__class__.__init__).parameters.keys() if name not in ["x", "y", "self", "predict"]}
        return params

    def get_checksum(self):
        """Computes a checksum for the training/validation/test data."""
        md5 = hashlib.md5()
        for row in np.concatenate([self.x, self.y], axis=1):
            md5.update(row.tobytes())
        return md5.hexdigest()

    def summary_input_output_dimensions(self, print_summary: bool = True) -> Tuple[int, int, str]:
        """
        Calculates the dimensions of the input and output of the ML model.


        Parameters:
        -----------
        print_summary : bool
            Whether to print the summary text.

        Returns:
        --------
        input_ml_total : int
            Total number of dimensions of the input of the ML model.
        output_ml_total : int
            Total number of dimensions of the output of the ML model.
        summary : str
            Summary text.
        """

        dims_input_ml = {dobj.name: dobj.dim for dobj in self.input_ml_dblock.dobj_list_transf}
        dims_output_ml = {dobj.name: dobj.dim for dobj in self.output_ml_dblock.dobj_list_transf}

        input_ml_total = sum(dims_input_ml.values())
        output_ml_total = sum(dims_output_ml.values())

        summary = f"Dimension of the input to the model ({self.input_ml_dblock.display_name}): {input_ml_total} \n"
        for k, v in dims_input_ml.items():
            summary += f"   {k}: {v} \n"

        summary += f"Dimension of the output of the model ({self.output_ml_dblock.display_name}): {output_ml_total} \n"
        for k, v in dims_output_ml.items():
            summary += f"   {k}: {v} \n"

        if print_summary:
            print(summary)
        return input_ml_total, output_ml_total, summary

    @classmethod
    def from_parameters(cls, x: Union[np.ndarray, torch.Tensor], y: Union[np.ndarray, torch.Tensor], **datamodule_kwargs):
        """
        Creates a data module from parameters returned by the `get_parameters(...)` method.

        Parameters
        ----------
        x : Union[np.ndarray, torch.Tensor]
            The input data.
        y : Union[np.ndarray, torch.Tensor]
            The output data.
        **datamodule_kwargs
            Additional keyword arguments to be passed to the data module.

        Returns
        -------
        DataModule
            The data module created from the parameters.

        """
        return cls(x, y, **datamodule_kwargs)

    @classmethod
    def from_dataset(
        cls,
        dataset: Dataset,
        input_ml_names: List[str] = None,
        output_ml_names: List[str] = None,
        input_ml_normalization: DataBlockNormalization = None,
        output_ml_normalization: DataBlockNormalization = None,
        **kwargs,
    ):
        """
        Creates a data module from a dataset.

        Parameters
        ----------
        dataset : Dataset
            The dataset to be used to create the data module.
        input_ml_names : List[str], optional
            List of names of the input data to be used for the ML model. The default is None. If None, then all the design parameters are used.
        output_ml_names : List[str], optional
            List of names of the output data to be used for the ML model. The default is None. If None, then all the performance attributes are used.
        input_ml_normalization : DataBlockNormalization, optional
            Custom normalization to be used for the input data. The default is None.
        output_ml_normalization: DataBlockNormalization, optional
            Custom normalization to be used for the output data. The default is None.
        **kwargs
            Additional keyword arguments to be passed to the data module.

        Returns
        -------
        DataModule
            The data module created from the dataset.

        """
        # Set default input and output names
        input_ml_names = input_ml_names or dataset.design_par.names_list
        output_ml_names = output_ml_names or dataset.perf_attributes.names_list

        x, dobj_list_input = dataset.data_mat_with_dobjs(dobj_names=input_ml_names, flag_transf=False)
        y, dobj_list_output = dataset.data_mat_with_dobjs(dobj_names=output_ml_names, flag_transf=False)

        input_ml_dblock = InputML(dobj_list=dobj_list_input, normalization_class=input_ml_normalization)
        output_ml_dblock = OutputML(dobj_list=dobj_list_output, normalization_class=output_ml_normalization)

        return cls(x, y, input_ml_dblock, output_ml_dblock, **kwargs)
