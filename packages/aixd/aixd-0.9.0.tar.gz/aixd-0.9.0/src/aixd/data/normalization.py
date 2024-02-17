from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Optional, Tuple

import numpy as np

from aixd.data.domain import IntervalMasked

if TYPE_CHECKING:  # avoid circular imports, as the following is only used for type checking
    from aixd.data.data_objects import DataObject

_registered_normalizations = {}


def register_normalization(name):
    """Defines the decorator to register normalizations. The decorator takes a name as argument and sets it as a static attribute on the class."""

    def decorator(normalization_class):
        if name in _registered_normalizations:
            raise Exception(f"Normalization with name {name} already registered.")
        normalization_class.name = name
        _registered_normalizations[name] = normalization_class
        return normalization_class

    return decorator


def resolve_normalization(name, *args, **kwargs) -> DataObjectNormalization:
    """Simple resolver that returns the normalization by its name."""
    if name in _registered_normalizations:
        normalization_class = _registered_normalizations[name]
        return normalization_class(*args, **kwargs)
    else:
        raise ValueError(f"Normalization '{name}' is not registered. Use the decorator @register_normalization()")


class DataObjectNormalization:
    """Abstract base class to implement DataObject normalization"""

    name: str = None  # identifier of the normalization and set by the decorator @register_normalization(...)

    def fit(self, data_mat: np.array, dobj: DataObject = None):
        """Method to implement to estimate values used for normalization, e.g., mean, std, min, max, etc."""
        return self

    def fit_normalize(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        """Fits and normalizes."""
        return self.fit(data_mat, dobj).normalize(data_mat, dobj)

    def is_fitted(self) -> bool:
        """Returns true if normalization strategy is fitted."""
        raise NotImplementedError()

    def reset(self):
        """Method to reset fitted values."""
        return self

    def normalize(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        """Normalizes the input."""
        raise NotImplementedError()

    def unnormalize(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        """Un-normalizes the input."""
        raise NotImplementedError()

    def copy(self, reset=False):
        """Copies the normalization."""
        obj_copy = copy.copy(self)
        if reset:
            obj_copy.reset()
        return obj_copy


class MinusDivNormalization(DataObjectNormalization):
    """
    Class defining normalizations of the form (x - minus_term) / divisor_term.

    Parameters
    ----------
    per_column : bool
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, per_column: bool = True):
        super().__init__()
        self.minus_term = None
        self.divisor_term = None
        self.per_column = per_column

    def fit_minus_div_term(self, data_mat: np.array, dobj: Optional[DataObject] = None) -> Tuple[np.array, np.array]:
        raise NotImplementedError

    def is_fitted(self) -> bool:
        return self.minus_term is not None and self.divisor_term is not None

    def fit(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        """Computes minus term and divisor term."""
        self.minus_term, self.divisor_term = self.fit_minus_div_term(data_mat, dobj)
        return self

    def reset(self):
        self.minus_term = None
        self.divisor_term = None
        return self

    def normalize(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        return (data_mat - self.minus_term) / (self.divisor_term + 1e-10)

    def unnormalize(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        return data_mat * self.divisor_term + self.minus_term


@register_normalization("norm_standard")
class Standardization(MinusDivNormalization):
    """
    Implements standardization as (x - mean) / std.

    Parameters
    ----------
    per_column : bool
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, per_column=True):
        super().__init__(per_column)

    def fit_minus_div_term(self, data_mat: np.array, dobj: Optional[DataObject] = None) -> np.array:
        minus_term = np.mean(data_mat, axis=0) if self.per_column else np.mean(data_mat)
        divisor_term = np.std(data_mat, axis=0) if self.per_column else np.std(data_mat)
        return minus_term, divisor_term


@register_normalization("norm_0to1")
class ZeroToOne(MinusDivNormalization):
    """
    Implements the zero-to-one (or min-max) normalization as (x - min) / (max - min).

    Parameters
    ----------
    per_column : bool
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, per_column=True):
        super().__init__(per_column)

    def fit_minus_div_term(self, data_mat: np.array, dobj: Optional[DataObject] = None) -> np.array:
        minimum = np.min(data_mat, axis=0) if self.per_column else np.min(data_mat)
        maximum = np.max(data_mat, axis=0) if self.per_column else np.max(data_mat)
        return minimum, maximum - minimum


@register_normalization("norm_m1to1")
class MinusOneToOne(ZeroToOne):
    """
    Implements the minus-one-to-one normalization as 2 * (((x - min) / (max - min)) - 0.5).

    Parameters
    ----------
    per_column : bool
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, per_column=True):
        super().__init__(per_column)

    def normalize(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        return 2 * (super().normalize(data_mat, dobj) - 0.5)

    def unnormalize(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        return super().unnormalize(data_mat * 0.5 + 0.5, dobj)


@register_normalization("masked_norm_0to1")
class MaskedZeroToOne(MinusDivNormalization):
    """
    Implements the zero-to-one (or min-max) normalization as (x - min) / (max - min) for DataObject's with a MaskedInterval domain.

    Parameters
    ----------
    per_column : bool
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, per_column=True):
        super().__init__(per_column)

    def fit_minus_div_term(self, data_mat: np.array, dobj: Optional[DataObject] = None) -> np.array:
        if dobj.domain is not None and isinstance(dobj.domain, IntervalMasked):
            if self.per_column:
                all_min = np.asarray([np.min(data_mat[:, o][~np.isin(data_mat[:, o], dobj.domain.options)]) for o in range(data_mat.shape[1])])
                all_max = np.asarray([np.max(data_mat[:, o][~np.isin(data_mat[:, o], dobj.domain.options)]) for o in range(data_mat.shape[1])])
            else:
                all_min = np.min(data_mat[~np.isin(data_mat, dobj.domain.options)])
                all_max = np.max(data_mat[~np.isin(data_mat, dobj.domain.options)])

            return all_min, all_max - all_min
        else:
            raise Exception("Expected DataObject with domain of type IntervalMasked.")


@register_normalization("masked_norm_m1to1")
class MaskedMinusOneToOne(MaskedZeroToOne):
    """
    Implements the minus-one-to-one normalization as 2 * (((x - min) / (max - min)) - 0.5) for DataObject's with a MaskedInterval domain.

    Parameters
    ----------
    per_column : bool
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, per_column=True):
        super().__init__(per_column)

    def normalize(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        return 2 * (super().normalize(data_mat, dobj) - 0.5)

    def unnormalize(self, data_mat: np.array, dobj: Optional[DataObject] = None):
        return super().unnormalize(data_mat * 0.5 + 0.5, dobj)
