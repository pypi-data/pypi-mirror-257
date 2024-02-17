"""
Function for the definition of the generator class
It intervenes in the last part of the process. Receives the following elements:
- Datamodule instance
- Model instance

Besides, it also uses an instance of the sampler class.

It uses then all these elements, and the sampler for generation, to perform
the following actions:
- Provide some feasible vector to the decoder, given a request
- Generate samples for a large range of values, to be used by the plotter

"""

import itertools
import warnings
from typing import Dict, List, Tuple, Union

import numpy as np
import pandas as pd
import torch

from aixd.data import DataBlock, DataObject, TransformableDataBlock
from aixd.data.custom_callbacks import AnalysisCallback, CustomCallback
from aixd.data.utils_data import combine_formats, convert_to
from aixd.mlmodel.architecture.cond_ae_model import CondAEModel
from aixd.mlmodel.data.data_loader import DataModule
from aixd.mlmodel.generation.sampling import GenSampler
from aixd.mlmodel.utils_mlmodel import ids_attrib, to_torch
from aixd.utils import logs

logger = logs.get_logger().get_child("mlmodel-generator")


class Generator:
    """
    Initialize a Generator instance. This instance is used to request the trained model
    the generation of sets of design parameters for a given set of attributes.

    Parameters
    ----------
    model : CondAEModel, optional, default=None
        The LightningModule that defines the generation process. If not provided,
        generation will be performed without a specific model.
    datamodule : DataModule optional, default=None
        The LightningDataModule that handles data loading and preprocessing.
        If not provided, data handling should be managed externally.
    sampling_type : str, optional, default="sampling"
        The type of sampling to be used for generation. The options are: "bayesian",
        and "sampling". See notes for more details.
    over_sample: int, optional, default=10
        If we request to generate n_samples, we will generate n_samples * over_sample,
        and then select the best n_samples.
    callbacks_class : class, optional, default=None
        A custom callback class to be used during the data generation process.
        This class should be derived from LightningCallbacks.
    fast_generation : bool, optional, default=False
        If True, the generation process will be faster, but the values of z will not be
        generated conditioned on the y requested. Only applicable to the Conditional AE model.

    Notes
    -----
    - All the instances of `datamodule` and `model` (with the checkpoint) loaded
        are required
    - The default `sampling_type` type is "sampling", and also the most recommended. "bayesian" is too
        slow.
    - If you want to use custom callbacks, provide a user-defined class via the
    `callbacks_class` parameter.
    """

    def __init__(
        self,
        model: CondAEModel,
        datamodule: DataModule,
        sampling_type: str = "sampling",
        over_sample: int = 10,
        callbacks_class: CustomCallback = None,
        fast_generation: bool = True,
    ) -> None:
        # Check if the model is on GPU, and if so, move it to CPU
        if not next(model.parameters()).is_cpu:
            model = model.to("cpu")
            warnings.warn("The generator currently only support models on CPU. The model has been moved to CPU.")

        self.model = model
        self.datamodule = datamodule
        self.fast_generation = fast_generation
        if isinstance(datamodule, DataModule):
            self.attributes_valid = self.datamodule.output_ml_dblock.columns_df  # _transf
            self.info_attributes_req()
        else:
            logger.warning("A valid data module should be provided")
        self.sampler = GenSampler(sampling_type, datamodule)
        if isinstance(model, CondAEModel):
            self.sampler_z = GenSampler(sampling_type, datamodule)
        self.callbacks_class = callbacks_class
        self.over_sample = over_sample  # How many more samples are obtaining, to later choose the indicated number

    def info_attributes_req(self) -> None:
        """
        It just prints the attributes that could be requested for generation
        """
        print("* Possible individual attributes to request for the design are:")
        print('     "{}"'.format('", "'.join(self.attributes_valid)))
        print("\n* You can also request for full data objects, with the following format: [None, 2, None]:")
        print("  For 'A' with dim = 3, y_req = [None, 2, None], which would be similar to requesting for 'A_1' = 2")
        print('     "{}"'.format('", "'.join(self.datamodule.output_ml_dblock.names_list)))
        val_gen = "Fast" if self.fast_generation else "Slow"
        print("\n* The generation process is set to: {}".format(val_gen))
        if self.fast_generation:
            print(
                """
    In this case, the values of z will not be generated conditioned on the y requested.
    This vastly accelerates the generation process, and is compensated by the over_sample
    parameter, which will allow generating more designs to then choose the best.
                """
            )
        else:
            print(
                """
    In this case, the values of z are generated conditioned on the y requested. This is quite
    costly, but allows generating samples that will lead to more precise generations, reducing the
    need for over sampling and the selection of the best designs.
                """
            )

    def generation(
        self,
        request: Dict[str, Union[int, float, bool, str, List]] = None,
        y_req: List[Union[int, float, bool, str, List]] = None,
        attributes: List[str] = None,
        weights: Dict[str, Union[int, float, bool, str, List]] = None,
        format_out: str = "df",
        n_samples: int = 50,
        print_results: bool = True,
        analyzer: "AnalysisCallback" = None,
        **kwargs,
    ) -> Tuple[Union[Dict, List, pd.DataFrame], Dict[str, Dict]]:
        """
        Wrapper method to call the generation process. It takes care of adapting the request,
        running the generator, and then providing the output in the specified format. Some of the options
        are simplified, as this is the function exposed to the user. For example, we assume the values are
        requested in the original domain, and that we are performing a single request.
        To run more specific generation process, it is better to use .run method.

        Parameters
        ----------
        self : object
            The instance of the class containing this method.
        request : Dict[str, Union[int, float, bool, str, List]], optional, default=None
            A dictionary with the attributes and values requested for generation. If provided,
            the `y_req` and `attributes` parameters are ignored.
        y_req : List[int, float, bool, str, List[int, float, bool, str]], optional, default=None
            The values requested for each of the attributes specified. Depending on the type of attribute,
            we can have to provide an specific type. Besides, if we want to generate in an interval, we can
            alternatively provide a List.
        attributes : List[str], optional, default=None
            The list of attribute names used to run the generative process.
        weights : Dict[str, Union[int, float, bool, str, List]], optional, default=None
            To assign different weighting to each attribute, when selecting the best instances
        format_out : str, optional, default=None
            The format of the output. The options are: "dict", "dict_list", "array", "torch", "list",
            "df_per_obj", "df". If not provided, the output will be a dictionary with
            all the information gathered from the generation process.
        n_samples : int, optional, default=50
            The number of samples of design parameters to generate.
        print_results : bool, optional, default=True
            Print an overview of the samples generated, and the errors computed.
        analyzer : AnalysisCallback, optional, default=None
            If provided, the generator will use the analyzer to compute the ground truth values. This is
            only possible when the InputML and OutputML are aligned with the DesignParameters and the
            PerformanceAttributes. If not, these values won't be computed.

        Returns
        -------
        Tuple[Union[Dict, List, pd.DataFrame]
            The dataframe with the combined inputML and outputML data, in the format specified by `format_out`.
        Dict[str, Dict]]
            This dictionary contains all the information gathered from the generation process. Hence, it can
            be used in other methods, from plotting, to computing errors, etc.
        """
        # Adapting the request to refer to specific columns
        y_req, attributes = self._adapt_request(request, y_req, attributes)

        weights = {o: 1 for o in attributes} if weights is None else weights
        self.weights = [weights[o] if o in weights.keys() else 1 for o in attributes]

        # Calling the generation
        dict_res = self.run(y_req, attributes, n_samples, request_orig_range=True, flag_peratt=False, nbins=1, **kwargs)

        if analyzer is not None and self._check_analyzer_sets(analyzer):
            y_gt = analyzer.analyze(input=dict_res["all"]["unnormalize"]["x_gen_best"], format_in="array", format_out="array")
            dict_res = self._update_with_gt(dict_res, y_gt)

        # Printing the results
        if print_results:
            self.print_results_gen(dict_res)

        # Converting the output to the desired format
        if format_out is None:
            return dict_res
        else:
            in_ml = dict_res["all"]["unnormalize"]["x_gen_best"]
            out_ml = dict_res["all"]["unnormalize"]["y_est_best_all"] if analyzer is None else dict_res["all"]["unnormalize"]["y_gt_best_all"]
            in_ml = convert_to(in_ml, format_out, self.datamodule.input_ml_dblock.dobj_list)
            out_ml = convert_to(out_ml, format_out, self.datamodule.output_ml_dblock.dobj_list)
            return combine_formats([in_ml, out_ml], format_out), dict_res

    def _check_analyzer_sets(self, analyzer: "AnalysisCallback") -> bool:
        all_val = True
        if not set(self.datamodule.output_ml_dblock.names_list).issubset(analyzer.perf_attributes.names_list):
            all_val = False
            subset = np.setdiff1d(self.datamodule.output_ml_dblock.names_list, analyzer.perf_attributes.names_list)
            print("Some outputML attributes are missing from the performance attributes: {}".format(", ".join(subset)))

        if not set(analyzer.design_par.names_list).issubset(self.datamodule.input_ml_dblock.names_list):
            all_val = False
            subset = np.setdiff1d(analyzer.design_par.names_list, self.datamodule.perf_attributes.names_list)
            print("Not all design parameters missing from inputML: {}".format(", ".join(subset)))

        return all_val

    def _update_with_gt(self, dict_res: Dict[str, Dict], y_gt_unnorm: np.ndarray, n_samples: int) -> Dict[str, Dict]:
        """Given the gt values computed using the CAD/FEM, the dict is updated with the new error values"""

        y_gt = self.datamodule.output_ml_dblock.transform(y_gt_unnorm)[0]
        y_gt = self.datamodule.normalize_y(y_gt)

        # Dummy block with splitted dimensions
        dummy_dblock = TransformableDataBlock(name="dummy", dobj_list=self.datamodule.output_ml_dblock.dobj_list, flag_split_perdim=True)

        # Gt error
        y_diff_gt, y_diff_gt_unnorm = self._compute_error(
            dummy_dblock.dobj_list_transf, y_gt, dict_res["all"]["normalize"]["y_samp"], y_gt_unnorm, dict_res["all"]["unnormalize"]["y_samp"]
        )

        # Model error
        y_diff_gt_est, y_diff_gt_est_unnorm = self._compute_error(
            dummy_dblock.dobj_list_transf, y_gt, dict_res["all"]["normalize"]["y_est_all"], y_gt_unnorm, dict_res["all"]["unnormalize"]["y_est_all"]
        )

        ind_sort_all, ind_sort_best, ind_attribute = dict_res["all"]["ind_sort"], dict_res["all"]["ind_sort_best"], dict_res["all"]["ids_att"]

        error_gt = y_diff_gt[:, ind_attribute].reshape(len(y_diff_gt), -1).mean(dim=-1)[ind_sort_all]
        error_gt_best = error_gt[ind_sort_best]

        # Storing errors
        dict_res["all"]["normalize"]["error_gt"] = error_gt
        dict_res["all"]["normalize"]["error_gt_best"] = error_gt_best

        # Storing individual errors per attributes and output of model - Unnormalized, i.e. original range
        dict_res["all"]["unnormalize"]["y_gt"] = y_gt_unnorm[:, ind_attribute][ind_sort_all].reshape(len(y_gt_unnorm), -1)
        dict_res["all"]["unnormalize"]["y_gt_best"] = y_gt_unnorm[ind_sort_best, :][:, ind_attribute].reshape(n_samples, -1)
        dict_res["all"]["unnormalize"]["y_gt_all"] = y_gt_unnorm[ind_sort_all].reshape(len(y_gt_unnorm), -1)
        dict_res["all"]["unnormalize"]["y_gt_best_all"] = y_gt_unnorm[ind_sort_best, :].reshape(n_samples, -1)
        dict_res["all"]["unnormalize"]["y_diff_gt"] = y_diff_gt_unnorm[:, ind_attribute][ind_sort_all].reshape(len(y_diff_gt_unnorm), -1)
        dict_res["all"]["unnormalize"]["y_diff_gt_best"] = y_diff_gt_unnorm[ind_sort_best, :][:, ind_attribute].reshape(n_samples, -1)
        dict_res["all"]["unnormalize"]["y_diff_gt_est"] = y_diff_gt_est_unnorm[:, ind_attribute][ind_sort_all].reshape(len(y_diff_gt_est_unnorm), -1)
        dict_res["all"]["unnormalize"]["y_diff_gt_est_best"] = y_diff_gt_est_unnorm[ind_sort_best, :][:, ind_attribute].reshape(n_samples, -1)

        # Storing individual errors per attributes and output of model - Normalized
        dict_res["all"]["normalize"]["y_gt"] = y_gt[:, ind_attribute][ind_sort_all].reshape(len(y_gt_unnorm), -1)
        dict_res["all"]["normalize"]["y_gt_best"] = y_gt[ind_sort_best, :][:, ind_attribute].reshape(n_samples, -1)
        dict_res["all"]["normalize"]["y_gt_all"] = y_gt[ind_sort_all].reshape(len(y_gt_unnorm), -1)
        dict_res["all"]["normalize"]["y_gt_best_all"] = y_gt[ind_sort_best, :].reshape(n_samples, -1)
        dict_res["all"]["normalize"]["y_diff_gt"] = y_diff_gt[:, ind_attribute][ind_sort_all].reshape(len(y_diff_gt_unnorm), -1)
        dict_res["all"]["normalize"]["y_diff_gt_best"] = y_diff_gt[ind_sort_best, :][:, ind_attribute].reshape(n_samples, -1)
        dict_res["all"]["normalize"]["y_diff_gt_est"] = y_diff_gt_est[:, ind_attribute][ind_sort_all].reshape(len(y_diff_gt_est_unnorm), -1)
        dict_res["all"]["normalize"]["y_diff_gt_est_best"] = y_diff_gt_est[ind_sort_best, :][:, ind_attribute].reshape(n_samples, -1)

        return self._dict_all_tocdn(dict_res)

    def run(
        self,
        y_req: List[Union[int, float, bool, str, List]],
        attributes: List[str],
        n_samples: int,
        request_orig_range: bool = True,
        flag_peratt: bool = False,
        nbins: int = 1,
        **kwargs,
    ) -> Dict[str, Dict]:
        """
        Method to generate sets of design parameters given a set of attributes from `outputML`,
        and the values for the generation.

        Parameters
        ----------
        self : object
            The instance of the class containing this method.
        request : Dict[str, Union[int, float, bool, str, List]], optional, default=50
            A dictionary with the attributes and values requested for generation. If provided,
            the `y_req` and `attributes` parameters are ignored.
        y_req : List[int, float, bool, str, List[int, float, bool, str]], optional, default=50
            The values requested for each of the attributes specified. Depending on the type of attribute,
            we can have to provide an specific type. Besides, if we want to generate in an interval, we can
            alternatively provide a List.
        attributes : List[str], optional, default=50
            The list of attribute names used to run the generative process.
        n_samples : int, optional, optional, default=50
            The number of samples of design parameters to generate.
        request_orig_range : bool, optional, optional, default=False
            If True, the `y_req` is specified within the original range of the real data.
        flag_peratt : bool, optional, optional, default=False
            If True, make independent generation requests for each attribute provided.
        nbins : int, optional, optional, default=1
            Using `nbins` is mostly intended for plotting purposes. It allows to generate
            many different requests in a binarize interval, and compute the error. Hence, it works
            differently as a request with a provided interval
        **kwargs : dict
            Additional keyword arguments specific to the generation method.

        Returns
        -------
        dict_out : Dict[str, Dict]
            This dictionary contains all the information gathered from the generation process. Hence,
            it can be used for many purposes, from plotting, to computing errors, or to extract
            the set of best generated samples

        Notes
        -----
        - The 'y_req' list should have the same length as the 'attributes' list.
        - If 'flag_peratt' is True, 'n_samples' will be divided equally among attributes.
        - When nbins = 1, the error for the attribute assigned to an interval is 0 if the value is within the interval
            When nbins > 1, which is intended for plotting purposes, the error is not 0, but the difference to requested
            value, which is sampled in that interval

        Example:
        --------
        >>> data_gen = Generator(datamodule, model, over_sample=1) # doctest: +SKIP
        >>> y_req = [3, 4.5, 'bananas'] # doctest: +SKIP
        >>> attributes = ['Age', 'Income', 'Fruit'] # doctest: +SKIP
        >>> samples_gen_dict = data_gen.generation(y_req, attributes, n_samples=100, request_orig_range=True) # doctest: +SKIP
        """

        # TODO account for the case we request for a full dobj, proving a list and Nones
        dummy_dblock = TransformableDataBlock(name="dummy", dobj_list=self.datamodule.output_ml_dblock.dobj_list, flag_split_perdim=True)

        # Checking if the all attributes are valid
        y_req, attributes_req, dobj_req, flag_range = self._get_corr_attributes(dummy_dblock, y_req, attributes)
        self.weights = [1 for o in attributes_req]
        nbins = 1 if not flag_range else nbins
        if len(attributes_req):
            # Calling generation
            dict_out = self._call_gen(dummy_dblock, y_req, attributes_req, n_samples, request_orig_range, flag_peratt, flag_range, nbins, dobj_req, max_samples_per=5000, **kwargs)
            # Calling selection of best
            dict_out = self._choose_best(dict_out, n_samples, nbins, dummy_dblock.dobj_list_transf, flag_range=flag_range)

            return self._dict_all_tocdn(dict_out)
        else:
            # print("None of the attributes specified were found in the dataset")
            logger.warning("None of the attributes specified were found in the dataset")
            return None

    def _adapt_request(self, request: Dict[str, Union[int, float, bool, str, List]] = None, y_req: List[Union[int, float, bool, str, List]] = None, attributes: List[str] = None):
        """
        It takes care of collecting the request, and adapting it to the format required by the generation
        method. Possible input types are:

        Having A dimension 2 and B dimension 3
        req = {'A_1': 1, 'B_0': 2}
        attributes = ['A_1', 'B_0'], y_req = [1,2]

        Or referring to the Data Objects
        req = {'A': [None, 1], 'B': [2, None, None]}
        attributes = ['A', 'B'], y_req = [[None, 1],[2, None, None]]

        We can also mix names of columns and dobjects
        req = {'A': [None, 1], 'B_0': [2]}

        Besides, we have the extra level of complexity, when we are requesting ranges, or mix of
        ranges and single values
        req = {'A_1': [1,3], 'B_0': 2}
        attributes = ['A_1', 'B_0'], y_req = [[1,3],2]

        req = {'A': [None, [1,3]], 'B': [2, None, None]}
        attributes = ['A', 'B'], y_req = [[None, [1,3]],[2, None, None]]

        All these different types of inputs need to be converted to the following format:

        attributes = ['A_1', 'B_0'], y_req = [1,2]

        because the main method, .run, is using one dataobject per column, as required by the sampler
        """

        # Obtaining the requested values
        if request is not None:
            attributes = list(request.keys())
            y_req = [request[k] for k in attributes]
        elif y_req is None or attributes is None:
            raise ValueError("You have to provide a request or the values and attributes requested")

        assert len(y_req) == len(attributes), "The number of attributes and values requested do not match"

        # Now, we just form the new attributes and y_req, only with information
        outputML = self.datamodule.output_ml_dblock
        y_req_def = []
        attributes_def = []
        for ind, att in enumerate(attributes):
            if att in self.attributes_valid:
                attributes_def.append(att)
                y_req_def.append(y_req[ind])
            elif att in outputML.names_list:
                dobjs = outputML.get_dobjs([att])
                req_aux = y_req[ind]
                for indr, req in enumerate(req_aux):
                    if req is not None:
                        attributes_def.append(dobjs[0].columns_df[indr])
                        y_req_def.append(req)
            else:
                logger.warning(f"Attribute/Data Object {att} not found in the dataset")
        return y_req_def, attributes_def

    def print_results_gen(self, dict_out: Dict[str, Dict]) -> None:
        """
        Print the results stored in a dictionary of dictionaries.

        This method takes a dictionary of dictionaries as input, where the outer dictionary
        represents categories or groups, and the inner dictionaries contain results or data
        associated with each category. It prints the results in a readable format.

        Parameters:
        ----------
        self : object
            The instance of the class containing this method.

        dict_out : Dict[str, Dict])
            The dictionary generated by the `generation` method, which contains a lof of nested
            dictionaries with the results of the generation process.
        """

        print("###########")
        print("Error during generation")
        print("###########\n")
        for key in dict_out.keys():
            str_req = [str(o) + " = " + str(i) for o, i in zip(dict_out[key]["attributes"], dict_out[key]["unnormalize"]["y_req"])]
            print("* Errors when requesting: {}".format(", ".join(str_req)))
            n_samples = len(dict_out[key]["unnormalize"]["y_diff_est_best"])
            mean_err = np.mean(dict_out[key]["unnormalize"]["y_diff_est_best"], axis=0)
            print("Mean for {} samples: {}".format(n_samples, ", ".join([str(o) for o in mean_err])))
            mean_err = np.mean(dict_out[key]["unnormalize"]["y_diff_est_best"][: int(np.ceil(n_samples / 10))], axis=0)
            print("Mean for {} sample(s): {}\n".format(np.ceil(n_samples / 10), ", ".join([str(o) for o in mean_err])))
            print("Best sample: {}\n".format(", ".join([str(o) for o in dict_out[key]["unnormalize"]["y_est_best"][0]])))

    def _get_corr_attributes(self, datablock: DataBlock, y: List[Union[int, float, bool, str, List]], attributes: List[str]) -> Tuple[List, List, List[DataObject], bool]:
        """
        Print the results stored in a dictionary of dictionaries.

        This method takes a dictionary of dictionaries as input, where the outer dictionary
        represents categories or groups, and the inner dictionaries contain results or data
        associated with each category. It prints the results in a readable format.

        Parameters:
        ----------
        self : object
            The instance of the class containing this method.
        y : List[Union[int, float, bool, str, List]]
            The list of requested values, also including list that can specify intervals
        attributes : List[str]
            The list of attributes requested

        Returns:
        ----------
        y_req : List
            List of requested value, only including the valid ones, according to the attributes checked
        attributes_req : List
            Only the names correctly specified are returned
        dobj_req : List[DataObject]
            DataObject instances for the attributes requested, to be used in later steps
        flag_range : bool
            Indicates if the list of requests include intervals or not
        """

        flag_range = False
        attributes_req = []
        dobj_req = []
        y_req = []

        for ind, att in enumerate(attributes):
            name_att = att.strip().replace(" ", "_")
            if name_att in self.attributes_valid:
                # TODO: maisseal, this can be solved better, in the end we want to retrieve a data object by name
                # TODO: maisseal, Do we need the transformed objects here?
                dobj = datablock.dobj_list[self.attributes_valid.index(name_att)]
                attributes_req.append(att.strip().replace(" ", "_"))
                dobj_req.append(dobj)
                val_req = y[ind]
                if not isinstance(val_req, list):
                    val_req = [val_req]
                if dobj.domain.domain_type == "Interval":
                    y_req.append(val_req[:2])
                else:
                    y_req.append(val_req)

                if len(val_req) > 1:
                    # Also applies for the case we request more than 1 possible option
                    flag_range = True
            else:
                logger.warning(f"Attribute {att} not found in the dataset")
        return y_req, attributes_req, dobj_req, flag_range

    def _call_gen(
        self,
        datablock: DataBlock,
        y_req: List[Union[int, float, bool, str, List]],
        attributes: List[str],
        n_samples: int = 50,
        request_orig_range: bool = False,
        flag_peratt: bool = False,
        flag_range: bool = False,
        nbins: int = 1,
        dobj_req: List[DataObject] = None,
        max_samples_per: int = 5000,
        **kwargs,
    ):
        """
        Call the function that generates the sets of design parameters, either per attributes
        or for all attributes simultaneously

        Parameters:
        -----------
        self : object
            The instance of the class containing this method.
        y_req : List[int, float, bool, str, List[int, float, bool, str]]
            The values requested for each of the attributes specified. Depending on the type of attribute,
            we can have to provide an specific type. Besides, if we want to generate in an interval, we can
            alternatively provide a List.
        attributes : List[str]
            The list of attribute names used to run the generative process.
        n_samples : int, optional, default=50
            The number of samples of design parameters to generate.
        request_orig_range : bool, optional, default=False
            If True, the `y_req` is specified within the original range of the data.
        flag_peratt : bool, optional, default=False
            If True, make independent generation requests for each attribute provided.
        flag_range : bool, optional, default=False
            If True, indicates if the list of requests include intervals or not
        nbins : int, optional, default=1
            Using `nbins` is mostly intended for plotting purposes. It allows to generate
            many different requests in a binarize interval, and compute the error. Hence, it works
            differently as a request with a provided interval
        dobj_req : List[DataObject], optional, default=None
            A list of DataObject instances used by the sampler
        max_samples_per : int, optional, default=5000
            To avoid passing batches too large through the decoder, we can limit the number of samples,
            and compute the decode step as this maximum is beign achieved

        **kwargs
            Additional keyword arguments for customization.

        Returns:
        --------
        dict_out : Dict[str, Dict]
            This dictionary contains all the information gathered from the generation process. Hence,
            it can be used for many purposes, from plotting, to computing errors, or to extract
            the set of best generated samples
        """

        if not isinstance(attributes, list):
            attributes = list(attributes)

        ids_att = ids_attrib(self.attributes_valid, attributes)

        dict_params = self.sampler._default_params() | kwargs

        dict_out = {}
        if flag_peratt:
            for ind, att in enumerate(attributes):
                flag_range_aux = False
                nbins_aux = 1
                if len(y_req[ind]) > 1:
                    flag_range_aux = True
                    nbins_aux = nbins
                x_gen, y_samp, y_req_norm, y_bins = self._gen_single_or_range(
                    datablock, [y_req[ind]], [att], n_samples * self.over_sample, request_orig_range, flag_range_aux, [dobj_req[ind]], nbins_aux, max_samples_per, **dict_params
                )
                dict_out[att] = {"attributes": [att], "y_req": y_bins, "y_req_norm": y_req_norm, "x_gen": x_gen, "y_samp": y_samp, "ids_att": ids_att[ind]}

        else:
            x_gen, y_samp, y_req_norm, y_bins = self._gen_single_or_range(
                datablock, y_req, attributes, n_samples * self.over_sample, request_orig_range, flag_range, dobj_req, nbins, max_samples_per, **dict_params
            )
            dict_out["all"] = {"attributes": attributes, "y_req": y_bins, "y_req_norm": y_req_norm, "x_gen": x_gen, "y_samp": y_samp, "ids_att": ids_att}

        return dict_out

    def _decode(self, y_samp: torch.Tensor, z: torch.Tensor = []) -> torch.Tensor:
        """
        Process a single batch of data.

        Parameters
        ----------
        self : object
            The instance of the class containing this method.
        y_samp : torch.Tensor, optional, default=[]
            The outputML, y, to pass through the decoder.

        Returns
        -------
        x_gen : torch.Tensor
            Sets of inputML generated by the decoder.
        """

        x_gen = self.model.decode(to_torch(y_samp, torch.float32), z)
        if self.callbacks_class is not None:
            x_gen = self.callbacks_class.run(x_gen)
        else:
            # We apply the unnormalization and normalization again to apply any transformation
            # in case of a special transformation. To really provide the generated input
            # as it should be
            x_unnorm = self.datamodule.unnormalize_x(x_gen)
            x_gen = self.datamodule.normalize_x(x_unnorm)
        return x_gen.type(torch.float32)

    def _get_z(
        self,
        datablock: DataBlock,
        y_req: Union[torch.Tensor, np.ndarray, List],
    ) -> Union[torch.Tensor, List]:
        # For the Standard AE model, we need to sample the Z conditioned to the requested Y
        epsilon_sampler_z = 0.1
        if not self.fast_generation and isinstance(self.model, CondAEModel):
            z, _ = self.sampler_z.generate_z(
                datablock,
                y_req.cpu().numpy(),
                n_samples=1,
                epsilon_sampler=epsilon_sampler_z,
                model=self.model,
            )
            return z
        else:
            return []

    def _gen_single_or_range(
        self,
        datablock: DataBlock,
        y_req: List[Union[int, float, bool, str, List]],
        attributes: List[str],
        n_samples: int = 50,
        request_orig_range: bool = False,
        flag_range: bool = False,
        dobj_req: List[DataObject] = None,
        nbins: int = 1,
        max_samples_per: int = 5000,
        **kwargs,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, List]:
        """
        Calls first the function to generate the outputML, and then the function to decode it
        into the generated samples

        Returns
        -------
        datablock : Datablock
            Data block with the information of all data objects
        y_req : List[Union[int, float, bool, str, List]]
            Requested values for the attributes
        attributes : List[str]
            The names for the requested attributes
        n_samples : int, optional, default=50
            Samples to generate
        request_orig_range : bool, optional, default=False
            If True, the `y_req` is specified within the original range of the real data.
        flag_range : bool, optional, default=False
            If True, the list of requests include intervals
        dobj_req : List[DataObject], optional, default=None
            List of data objects for the requested attributes
        nbins : int, optional, default=1
            Number of bins to use for the generation
        max_samples_per : int, optional, default=5000
            To avoid passing batches too large through the decoder, we can limit the number of samples,
            and compute the decode step as this maximum is beign achieved

        Returns
        -------
        x_gen : torch.Tensor
            Sets of inputML generated by the decoder.
        y_samp : torch.Tensor
            Sets of outputML obtained through sampling, and fed to the decoder.
        y_req_norm : torch.Tensor
            Normalized requested values
        vec_iter_par : List
            When using bins, the list of all independent requests generated

        Notes
        -----
        - The parameters are fully shared with function _call_gen
        """

        # Generating ranges
        if not flag_range:
            y_samp, y_req_norm = self.sampler.generate(datablock, y_req, attributes, n_samples, request_orig_range, dobj_req, flag_range, **kwargs)
            z = self._get_z(datablock, y_samp)
            return self._decode(y_samp, z), y_samp, y_req_norm, y_req
        else:
            # This case is more complex because we can use bins for the intervals
            lists_ranges = []

            for i in range(len(attributes)):
                if len(y_req[i]) == 2 and dobj_req[i].domain.domain_type == "Interval":
                    aux_range = np.linspace(y_req[i][0], y_req[i][1], nbins + 1)
                    lists_ranges.append([[aux_range[i], aux_range[i + 1]] for i in range(len(aux_range) - 1)])
                else:
                    lists_ranges.append([y_req[i]])
            vec_iter_par = list(itertools.product(*lists_ranges))

            # Generating samples
            x_gen = []
            y_samp = []
            y_samp_aux = []
            y_req_norm = []
            n_samples_per = int(n_samples / len(vec_iter_par))
            for list_ranges in vec_iter_par:
                y_samp_aux1, y_req_norm_aux = self.sampler.generate(datablock, list_ranges, attributes, n_samples_per, request_orig_range, dobj_req, flag_range, **kwargs)
                y_samp_aux.append(y_samp_aux1)
                y_req_norm.append(y_req_norm_aux)

                if len(y_samp_aux) * n_samples_per > max_samples_per:
                    y_samp_aux = torch.cat(y_samp_aux, dim=0)
                    z = self._get_z(datablock, y_samp_aux)
                    x_gen.append(self._decode(y_samp_aux, z))
                    y_samp.append(y_samp_aux)
                    y_samp_aux = []

            if len(y_samp_aux):
                y_samp_aux = torch.cat(y_samp_aux, dim=0)
                z = self._get_z(datablock, y_samp_aux)
                x_gen.append(self._decode(y_samp_aux, z))
                y_samp.append(y_samp_aux)

            return torch.cat(x_gen).type(torch.float32), torch.cat(y_samp).type(torch.float32), y_req_norm, vec_iter_par

    @staticmethod
    def _compute_error(dobjs: List[DataObject], y_pred: torch.Tensor, y_real: torch.Tensor, y_pred_unnorm: np.ndarray, y_real_unnorm: np.ndarray):
        """Using the method from the data objects to compute the errors"""

        def _c_error(dobjs, y_p, y_r, y_pu, y_ru, norm=True, eval=False):
            y_d = []
            yp, yr = (y_p, y_r) if norm else (y_pu, y_ru)
            for dobj in dobjs:
                aux_l = dobj.get_loss_evaluation(eval=eval)
                if dobj.type in ["categorical", "bool", "ordinal"]:
                    y_d.append(
                        aux_l(y_p[:, dobj.position_index : (dobj.position_index + dobj.dim)], y_r[:, dobj.position_index : (dobj.position_index + dobj.dim)]).reshape(len(y_p), -1)
                    )
                else:
                    y_d.append(
                        aux_l(
                            to_torch(yp[:, dobj.position_index : (dobj.position_index + dobj.dim)], torch.float32),
                            to_torch(yr[:, dobj.position_index : (dobj.position_index + dobj.dim)], torch.float32),
                        ).reshape(len(y_p), -1)
                    )
            return torch.cat(y_d, dim=1)

        y_diff_est = _c_error(dobjs, y_pred, y_real, y_pred_unnorm, y_real_unnorm, norm=True, eval=False)
        y_diff_est_unnorm = _c_error(dobjs, y_pred, y_real, y_pred_unnorm, y_real_unnorm, norm=False, eval=True)

        return y_diff_est, y_diff_est_unnorm

    def _choose_best(self, dict_out: Dict[str, Dict], n_samples: int, nbins: int, dobjs: List[DataObject], flag_range: bool = False) -> Dict[str, Dict]:
        """
        Call the function that generates the sets of design parameters, either per attributes
        or for all attributes simultaneously

        Parameters
        ----------
        self : object
            The instance of the class containing this method.
        dict_out : Dict[str, Dict]
            This dictionary contains all the information gathered from the generation process.
        n_samples : int
            The number of samples of design parameters to generate.
        nbins : int
            Using `nbins` is mostly intended for plotting purposes. It allows to generate
            many different requests in a binarize interval, and compute the error. Hence, it works
            differently as a request with a provided interval
        dobjs : List[DataObject]
            A list of DataObject instances used by the sampler
        flag_range : bool, optional, default=False
            If True, indicates if the list of requests include intervals or not

        Returns
        -------
        dict_results: Dict[str, Dict]
            Dictionary created from dict_out with all the final results

        """

        dict_results = {}
        for ind, att in enumerate(dict_out.keys()):
            # Still normalized variables
            y_est = self.model.encode(to_torch(dict_out[att]["x_gen"], torch.float32))["y"]
            ind_attribute = dict_out[att]["ids_att"]
            y_req = dict_out[att]["y_req_norm"]

            # All unnormalized variables
            y_req_unnorm = dict_out[att]["y_req"]

            y_samp_unnorm = self.datamodule.unnormalize_y(self._cdn(dict_out[att]["y_samp"]))
            y_samp_unnorm = self.datamodule.output_ml_dblock.inverse_transform(y_samp_unnorm)[0]

            y_est_unnorm = self.datamodule.unnormalize_y(self._cdn(y_est))
            y_est_unnorm = self.datamodule.output_ml_dblock.inverse_transform(y_est_unnorm)[0]

            x_gen_unnorm = self.datamodule.unnormalize_x(self._cdn(dict_out[att]["x_gen"]))
            x_gen_unnorm = self.datamodule.input_ml_dblock.inverse_transform(x_gen_unnorm)[0]

            # TODO: maisseal & luis: Untransformed can not be converted to a float tensor, as there might be categorical variables
            # TODO: luis : I believe we should compute these errors using the evaluation method of each data object. And for
            # the case of categorical variables, we should use the hamming distance for example. Or just a function that works with
            # both transformed and untransformed data, for example [0 1 0 0] == [1 0 0 0] will work also with 'dog' == 'cat'

            # TODO: maisseal & luis: Untransformed can not be converted to a float tensor, as there might be categorical variables
            y_diff_est, y_diff_est_unnorm = self._compute_error(dobjs, y_est, dict_out[att]["y_samp"], y_est_unnorm, y_samp_unnorm)
            weights = to_torch(np.asarray(self.weights), torch.float32).reshape(1, -1)
            y_diff_est_weighted = y_diff_est[:, ind_attribute].reshape(len(y_diff_est), -1) * weights

            # The errors are averaged over the attributes requested, and selected per bins
            if flag_range and nbins > 1:
                # If nbins > 1, the error is not considered as in the case of single ranges. This nbin
                # option is used for plotting, when we want to generate many designs in some bin. Therefore, the errors
                # is still respect to the value requested.
                ind_sort_all = []
                ind_sort_best = []

                sampler_per = int(len(y_est) / len(y_req))
                for ind_bin, ybin in enumerate(y_req):
                    # ind_bin = np.argwhere((self._cdn(dict_out[att]["y_samp"])[:,ind_attribute].flatten() >= ybin[0]) &
                    #                      (self._cdn(dict_out[att]["y_samp"])[:,ind_attribute].flatten() < ybin[1])).flatten()
                    offset_bin = int(ind_bin * sampler_per)
                    ind_bin = np.arange(offset_bin, offset_bin + sampler_per)
                    error_bin = y_diff_est_weighted[ind_bin, :].reshape(len(y_diff_est[ind_bin]), -1).mean(dim=-1)
                    _, ind_sort = error_bin.sort(dim=0)
                    ind_sort_all.append(ind_bin[ind_sort])
                    ind_sort_best.append(ind_bin[ind_sort[: int(n_samples / len(y_req))]])

                ind_sort_all = np.concatenate(ind_sort_all)
                ind_sort_best = np.concatenate(ind_sort_best)

            else:
                if flag_range:
                    y_req = y_req[0]
                    y_req_unnorm = y_req_unnorm[0]
                    # For the case of intervals, the error is 0 if the value is within the interval,
                    # and the difference to the mean of the interval otherwise
                    for ind_att, pos_att in enumerate(ind_attribute):
                        if len(y_req[ind_att]) == 2 and dobjs[ind_att].domain.domain_type == "Interval":
                            # condition = self.sampler._create_condition([dobj_req[ind_att]], [y_req[0][ind_att]], 0.05)
                            # valid = condition.evaluate(y_est).flatten() if condition is not None else np.ones(len(y_est)).astype(bool)
                            valid = np.asarray(
                                (self._cdn(y_est)[:, pos_att].flatten() >= y_req[ind_att][0]) & (self._cdn(y_est)[:, pos_att].flatten() < y_req[ind_att][1])
                            ).flatten()
                            y_diff_est_weighted[valid, ind_att] = 0
                            y_diff_est_unnorm[valid, pos_att] = 0
                            mean_val = 0.5 * (y_req[ind_att][0] + y_req[ind_att][1])
                            y_diff_est_weighted[~valid, ind_att] = torch.sub(y_est[~valid, pos_att], mean_val).abs() * weights[0, ind_att]
                            mean_val = 0.5 * (y_req_unnorm[ind_att][0] + y_req_unnorm[ind_att][1])
                            y_diff_est_unnorm[~valid, pos_att] = torch.sub(to_torch(y_est_unnorm[~valid, pos_att], torch.float32), mean_val).abs()
                        if len(y_req[ind_att]) >= 2 and dobjs[ind_att].domain.domain_type == "Options":
                            valid = np.isin(self._cdn(y_est)[:, pos_att].flatten(), y_req[ind_att][0]).flatten()
                            y_diff_est_weighted[valid, ind_att] = 0
                            y_diff_est_unnorm[valid, pos_att] = 0

                error_all_est = y_diff_est_weighted.reshape(len(y_diff_est), -1).mean(dim=-1)
                _, ind_sort_all = error_all_est.sort(dim=0)
                ind_sort_best = ind_sort_all[:n_samples]

            error_all_est = y_diff_est_weighted.reshape(len(y_diff_est), -1).mean(dim=-1)
            error_all_est_best = error_all_est[ind_sort_best]

            dict_results[att] = {"attributes": dict_out[att]["attributes"], "ids_att": ind_attribute, "ind_sort": ind_sort_all, "ind_sort_best": ind_sort_best}
            dict_results[att]["normalize"] = {
                "y_req": y_req,
                "x_gen": dict_out[att]["x_gen"][ind_sort_all],
                "x_gen_best": dict_out[att]["x_gen"][ind_sort_best],
                "y_samp": dict_out[att]["y_samp"][ind_sort_all],
                "y_samp_best": dict_out[att]["y_samp"][ind_sort_best],
                "y_est": y_est[:, ind_attribute][ind_sort_all].reshape(len(y_diff_est), -1),
                "y_est_best": y_est[ind_sort_best, :][:, ind_attribute].reshape(n_samples, -1),
                "y_est_best_all": y_est[ind_sort_best, :].reshape(n_samples, -1),
                "y_est_all": y_est[ind_sort_all].reshape(len(y_diff_est), -1),
                "y_diff_est": y_diff_est[:, ind_attribute][ind_sort_all].reshape(len(y_diff_est), -1),
                "y_diff_est_best": y_diff_est[:, ind_attribute][ind_sort_best].reshape(n_samples, -1),
                "error_est": error_all_est,
                "error_est_best": error_all_est_best,
            }

            dict_results[att]["unnormalize"] = {
                "y_req": y_req_unnorm,
                "x_gen": x_gen_unnorm[ind_sort_all],
                "x_gen_best": x_gen_unnorm[ind_sort_best],
                "y_samp": y_samp_unnorm[ind_sort_all],
                "y_samp_best": y_samp_unnorm[ind_sort_best],
                "y_est": y_est_unnorm[:, ind_attribute][ind_sort_all].reshape(len(y_diff_est), -1),
                "y_est_best": y_est_unnorm[ind_sort_best, :][:, ind_attribute].reshape(n_samples, -1),
                "y_est_best_all": y_est_unnorm[ind_sort_best, :].reshape(n_samples, -1),
                "y_est_all": y_est_unnorm[ind_sort_all].reshape(len(y_diff_est), -1),
                "y_diff_est": y_diff_est_unnorm[:, ind_attribute][ind_sort_all].reshape(len(y_diff_est), -1),
                "y_diff_est_best": y_diff_est_unnorm[:, ind_attribute][ind_sort_best].reshape(n_samples, -1),
            }

        return self._dict_all_tocdn(dict_results)

    def _dict_all_tocdn(self, dict_conv: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Converts iteratively all entries of a dictionary to numpy arrays

        Parameters
        ----------
        dict_conv : Dict[str, Dict]
            Dictionary to convert

        Returns
        -------
        dict_conv : Dict[str, Dict]
            Converted dictionary
        """
        for key in dict_conv.keys():
            if isinstance(dict_conv[key], dict):
                dict_conv[key] = self._dict_all_tocdn(dict_conv[key])
            else:
                dict_conv[key] = self._cdn(dict_conv[key])
        return dict_conv

    def _cdn(self, x: Union[torch.Tensor, np.ndarray]) -> np.ndarray:
        """
        Detachs, moves to cpu, and convert to numpy array

        Parameters
        ----------
        x : Union[torch.Tensor, np.ndarray]
            Entry to convert

        Returns
        -------
        x : np.ndarray
            x in numpy array format
        """
        if isinstance(x, torch.Tensor):
            return x.cpu().detach().numpy()
        return x
