"""Test the shortcut functions"""

from mrfmsim.shortcut import loop_shortcut
import pytest


def test_loop_shortcut(model):
    """Test loop shortcut
    
    The resulting value should create a looped model of d
    """

    loop_model = loop_shortcut(model, "d")

    assert loop_model(a=2, b=2, d=[1, 2, 3], f=2) == ([24, 16, 8], 2.0)

def test_loop_shortcut_top_level(model):
    """Test loop shortcut when the parameter is used at the top level

    The resulting value should create a looped model of b
    (a top level parameter, as in the subgraph is the same as the graph)
    """

    loop_model = loop_shortcut(model, "b")

    assert loop_model(a=0, b=[2, 4], d=2, f=2) == [(0, 1), (16, 1)]


def test_loop_shortcut_incorrect_parameter(model):
    """Test loop shortcut when the parameter is not in model parameter
    
    If a wrong parameter is chosen, an exception should be raised
    """

    with pytest.raises(Exception, match="'c' is not in model parameter"):
        loop_shortcut(model, "c")

    