"""Test component base

ComponentBase class provides the __repr__ output
of all component classes.
"""


import numpy as np
from mrfmsim.component import ComponentBase
import pytest
from textwrap import dedent


@pytest.fixture
def component_obj(units):
    """Create an object with different types of attributes."""

    obj = ComponentBase()
    obj._units = units
    # obj._parameters = ('b0', 'b1', 'b_tot', 'list', 'str', 'tuple')

    obj.b0 = 100.0  # float
    obj.b1 = np.array([1, 2, 3])  # int
    obj.b_tot = np.array([1.0, 2.0, 3.0])  # float
    obj.list = [1, 2, 3]
    obj.tuple = (1, 2, 3)
    obj.str = "str"
    obj._private_attr = 1

    return obj


def test_attrs_to_dict(component_obj):
    """Test the component object to create a dictionary from public attributes.

    The test makes sure that private attributes ("_private_attr")
    and methods ("attrs_to_dict") are not included.
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


def test_str(component_obj):
    """Test representation of different types."""

    base_str = """\
    ComponentBase(
      b0=100.0 [mT] # longitudinal magnetic field
      b1=[1.000 2.000 3.000] [mT] # transverse magnetic field
      b_tot=[1.0 2.0 3.0] [mT] # total magnetic field
      list=[1, 2, 3]
      str=str
      tuple=(1, 2, 3)
    )"""

    assert str(component_obj) == dedent(base_str)


def test_str_no_unit(component_obj):
    """Test representation if units are not defined."""

    str_no_unit = """\
    ComponentBase(
      b0=100.0
      b1=[1 2 3]
      b_tot=[1.0 2.0 3.0]
      list=[1, 2, 3]
      str=str
      tuple=(1, 2, 3)
    )"""
    component_obj._units = {}
    assert str(component_obj) == dedent(str_no_unit)
