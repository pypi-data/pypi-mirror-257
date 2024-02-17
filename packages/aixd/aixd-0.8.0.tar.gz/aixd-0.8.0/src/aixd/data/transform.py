from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Optional

import numpy as np

from aixd.data.domain import Options

if TYPE_CHECKING:  # avoid circular imports, as the following is only used for type checking
    from aixd.data.data_objects import DataObject

_registered_transformations = {}


def register_transformation(name):
    """Defines the decorator to register transformations. The decorator takes a name as argument and sets it as a static attribute on the class."""

    def decorator(transformation_class):
        if name in _registered_transformations:
            raise Exception(f"Transformation with name {name} already registered.")
        transformation_class.name = name
        _registered_transformations[name] = transformation_class
        return transformation_class

    return decorator


def resolve_transformation(name, *args, **kwargs) -> DataObjectTransform:
    """Simple resolver that returns the transformation by its name."""
    if name in _registered_transformations:
        transformation_class = _registered_transformations[name]
        return transformation_class(*args, **kwargs)
    else:
        raise ValueError(f"Transformation '{name}' is not registered. Use the decorator @register_transformation()")


class DataObjectTransform:
    """Abstract base class to implement DataObject transformation."""

    name: str = None  # set by the decorator

    def fit(self, data_mat: np.array, dobj: Optional[DataObject]):
        """Method to implement to fit transformation."""
        return self

    def is_fitted(self) -> bool:
        """Returns true if transformation strategy is fitted."""
        raise NotImplementedError()

    def reset(self):
        """Method to implement to reset fitted values."""
        return self

    def fit_transform(self, data_mat: np.array, dobj: Optional[DataObject]):
        """Fits and transform."""
        return self.fit(data_mat, dobj).transform(data_mat, dobj)

    def transform(self, data_mat: np.array, dobj: Optional[DataObject]):
        """Transforms the input."""
        raise NotImplementedError()

    def inverse_transform(self, data_mat: np.array, dobj: Optional[DataObject]):
        """Inverse transform of the input."""
        raise NotImplementedError()

    def copy(self, reset=False):
        """Copies the transformation."""
        obj_copy = copy.copy(self)
        if reset:
            obj_copy.reset()
        return obj_copy


@register_transformation("log10")
class Log10Transform(DataObjectTransform):
    """
    Implements a log10 transformation of the data.
    """

    def is_fitted(self) -> bool:
        return True

    def transform(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        return np.log10(data_mat + 1)

    def inverse_transform(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        return np.power(10, data_mat) - 1


@register_transformation("sigmoid")
class SigmoidTransform(DataObjectTransform):
    """
    Implements a scaled sigmoid transformation of the data.
    """

    def __init__(self):
        super().__init__()
        self.scale_factor = None

    def is_fitted(self) -> bool:
        return self.scale_factor is not None

    def reset(self):
        self.scale_factor = None

    def fit(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        self.scale_factor = np.abs([1 / np.min(data_mat), 1 / np.max(data_mat)]).max()
        return self

    def transform(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        return 1 / (1 + np.exp(-data_mat * self.scale_factor))

    def inverse_transform(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        return (1 / self.scale_factor) * np.log(data_mat / (1 - data_mat + 1e-16))


@register_transformation("cat_to_id")
class CatToId(DataObjectTransform):
    """
    Implements and encoding for string to integers.
    """

    def __init__(self):
        super().__init__()
        self.mapping = None

    def is_fitted(self) -> bool:
        return self.mapping is not None

    def reset(self):
        self.mapping = None

    def fit(self, data_mat: np.array, dobj: Optional[DataObject]):
        if not isinstance(dobj.domain, Options):
            # if not dobj.domain.domain_type == 'Options': # When updating the object, it loses the type TODO: solve this
            raise Exception("Domain must be of type Options.")

        # This is required to reduce the dimensionality of the one-hot-encoding vector
        dobj.update_obj(data_mat)
        self.mapping = {cat: i for i, cat in enumerate(dobj.domain.array)}
        return self

    def transform(self, data_mat: np.array, dobj: Optional[DataObject]):
        data_mat_id = np.zeros_like(data_mat, dtype=int)
        for cat, i in self.mapping.items():
            data_mat_id[data_mat == cat] = i
        return data_mat_id

    def inverse_transform(self, data_mat: np.array, dobj: Optional[DataObject]):
        data_mat_cat = np.zeros_like(data_mat, dtype=dobj.dtype)
        for cat, i in self.mapping.items():
            data_mat_cat[data_mat == i] = cat
        return data_mat_cat


@register_transformation("cat_to_one_hot")
class CatToOneHot(CatToId):
    """
    Implements one hot encoding for string and integer data. Can be used for categorical and ordinal data.
    """

    def transform(self, data_mat: np.array, dobj: Optional[DataObject]):
        """Returns the encoded categories."""

        if not (dobj.type == "categorical" or dobj.type == "ordinal"):
            raise Exception("DataObject must be of type DataCategorical.")

        if data_mat.ndim == 1:
            data_mat = data_mat.T

        assert data_mat.ndim == 2 and data_mat.shape[1] == 1  # Assumes one dimensional array or column vector

        # Encode to integer id
        data_mat_id = super().transform(data_mat, dobj)

        # Expand to one-hot
        if len(self.mapping) == 2:
            return data_mat_id
        else:
            return np.eye(len(self.mapping.keys()))[data_mat_id.flatten()]

    def inverse_transform(self, data_mat: np.array, dobj: Optional[DataObject]):
        """Returns the decoded categories in a column vector."""

        if not (dobj.type == "categorical" or dobj.type == "ordinal"):
            raise Exception("DataObject must be of type DataCategorical or DataOrdinal.")

        if len(self.mapping) == 2:
            # If the data is one dimensional, it is binary
            # DataCategorical and DataOrdinal are approximated by logits, meaning that positive values are mapped to 1 and negative (including 0) to 0
            return super().inverse_transform(np.where(data_mat <= 0, 0, 1), dobj)
        else:
            # else it is one-hot encoded
            # DataCategorical and DataOrdinal are approximated by logits, meaning that the highest value is mapped to 1 and the rest to 0
            data_mat_id = np.argmax(data_mat, axis=1).reshape(-1, 1)
            return super().inverse_transform(data_mat_id, dobj)


@register_transformation("to_float")
class ToFloat(DataObjectTransform):
    """
    Implement a transformation to convert integers to floats. The inverse transforms ensures that values are not outside the domain.
    """

    def is_fitted(self) -> bool:
        return True

    def transform(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        return np.asarray(data_mat).astype(float)

    def inverse_transform(self, data_mat: np.array, dobj: Optional[DataObject]):
        mat_int = np.round(data_mat).astype(int)
        min_max = [np.min(dobj.domain.array), np.max(dobj.domain.array)]
        mat_int[mat_int < min_max[0]] = min_max[0]
        mat_int[mat_int > min_max[1]] = min_max[1]
        return mat_int
