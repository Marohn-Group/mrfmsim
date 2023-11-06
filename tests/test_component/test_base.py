"""Test the ComponentBase class"""


import numpy as np
from dataclasses import dataclass, field
from mrfmsim.component import ComponentBase
import pytest
import pint
from textwrap import dedent


# class used for testing
@dataclass
class Component(ComponentBase):
    array: np.ndarray = field(metadata={"unit": ""})
    float: float
    list: list
    str: str
    tuple: tuple
    B0: float = field(init=False, metadata={"unit": "mT", 'format': '.3e'})
    B1: list = field(init=False)

    def __post_init__(self):
        self.B0 = 100.0
        self.B1 = [1, 2, 3]
        self._private = 1
        self.other = 1


def test_component_str():
    """Test the string representation of a component object.

    The "_private" and the "other" does not show up in the string.
    The float has a custom format with 3 decimal places. And the
    B0 has a format of 3 decimal places of scientific notation.
    """

    str_no_unit = """\
    Component(array=[1.e+03 1.e-04 3.e+00]
    \tfloat=1.000
    \tlist=[1, 2, 3]
    \tstr=str
    \ttuple=(1, 2, 3)
    \tB0=1.000e+02 mT
    \tB1=[1, 2, 3])"""

    obj = Component(np.array([1e3, 0.0001, 3]), 1.0, [1, 2, 3], "str", (1, 2, 3))

    assert str(obj) == dedent(str_no_unit)


def test_ComponentBase_get_metadata():
    """Test the get_metadata method of ComponentBase."""

    obj = Component(np.array([1e3, 0.0001, 3]), 1.0, [1, 2, 3], "str", (1, 2, 3))

    assert obj._get_metadata("array") == {"unit": ""}
    assert obj._get_metadata("float") == {}
    assert obj._get_metadata("B0") == {"unit": "mT", 'format': '.3e'}
    assert obj._get_metadata("other") == {}


def test_ComponentBase_get_unit():
    """Test the get_unit method of ComponentBase."""

    obj = Component(np.array([1e3, 0.0001, 3]), 1.0, [1, 2, 3], "str", (1, 2, 3))

    assert obj.get_unit("array") == ""
    assert obj.get_unit("float") == ""
    assert obj.get_unit("B0") == "mT"
    assert obj.get_unit("other") == ""
    with pytest.raises(
        AttributeError, match="'Component' object has no attribute 'not_an_attribute'"
    ):
        obj.get_unit("not_an_attribute")
