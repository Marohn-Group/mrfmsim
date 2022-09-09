"""Test component base

ComponentBase class provides the __repr__ output
of all component classes.
"""


import numpy as np
from mrfmsim.component import ComponentBase
import pytest


@pytest.fixture
def component_obj(units):
    """Create a object with different types of attributes"""

    obj = ComponentBase()
    obj._units = units

    obj.b0 = 100.0  # float
    obj.b1 = np.array([1, 2, 3])  # int
    obj.b_tot = np.array([1.0, 2.0, 3.0])  # float
    obj.list = [1, 2, 3]
    obj.tuple = (1, 2, 3)
    obj.str = "str"
    obj._private_attr = 1

    return obj


def test_attrs_to_dict(component_obj):
    """Test the component object create dictionary from public attributes

    The tests makes sure that private attributes ("_private_attr")
    and methods ("attrs_to_dict") are not included
    """

    attr_dict = component_obj.attrs_to_dict()

    assert list(attr_dict.keys()) == [
        "b0",
        "b1",
        "b_tot",
        "list",
        "str",
        "tuple",
    ]


BASE_STR = """ComponentBase(
  b0=1.000e+02 [mT] # longitudinal magnetic field
  b1=[1.000 2.000 3.000] [mT] # transverse magnetic field
  b_tot=[1.0 2.0 3.0] [mT] # total magnetic field
  list=[1 2 3]
  str=str
  tuple=[1 2 3]
)"""


def test_str(component_obj):
    """Test representation of different types"""
    assert str(component_obj) == BASE_STR


NO_UNIT_STR = """ComponentBase(
  b0=100.0
  b1=[1 2 3]
  b_tot=[1.0 2.0 3.0]
  list=[1 2 3]
  str=str
  tuple=[1 2 3]
)"""


def test_str_no_unit(component_obj):
    """Test representation if units are not defined"""
    component_obj._units = {}
    assert str(component_obj) == NO_UNIT_STR