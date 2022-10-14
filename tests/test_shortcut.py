"""Test the shortcut on both Model and Experiment instances"""

from types import SimpleNamespace
from mrfmsim.shortcut import loop_shortcut
import pytest


def test_loop_shortcut(model, expt_plain):
    """Test loop shortcut

    The resulting value should create a looped model of d. For expt,
    the d is already looped.
    """

    loop_model = loop_shortcut(model, "d")

    assert loop_model(a=0, b=2, d=[1, 2], f=3) == ([8, 0], 1.0, 9)

    loop_expt = loop_shortcut(expt_plain, "f")
    print(loop_expt.graph.nodes["f_loop_node"]["func"](c=2, e=1, f=[3, 4]))
    assert loop_expt(a=0, b=2, d=1, f=[3, 4]) == ((8, 9), 1.0, (16, 16))


def test_loop_shortcut_single_node(model, expt_plain):
    """Test loop shortcut when the subgraph is a single node

    The resulting value should create a looped model of d. For expt,
    the d is already looped.
    """

    loop_model = loop_shortcut(loop_shortcut(model, "d"), "d")
    assert loop_model(a=0, b=2, d=[[1, 2], [1, 2]], f=3) == ([[8, 0], [8, 0]], 1.0, 9)

    loop_model = loop_shortcut(loop_shortcut(model, "f"), "f")
    # the output is actually k1, p1, k2, p2
    assert loop_model(a=0, b=2, d=1, f=[[3, 4], [3, 4]]) == (
        [(8, 9), (16, 16)],
        1.0,
        [(8, 9), (16, 16)],
    )


def test_loop_shortcut_top_level(model, expt_plain):
    """Test loop shortcut when the parameter is used at the top level

    The resulting value should create a looped model of b
    (a top level parameter, as in the subgraph is the same as the graph)
    """

    loop_model = loop_shortcut(model, "b")
    assert loop_model(a=0, b=[2, 4], d=2, f=3) == [(0, 1), (128, 1)]

    loop_expt = loop_shortcut(expt_plain, "b")
    assert loop_expt(a=0, b=[2, 4], d=2, f=3) == [(0, 1), (128, 1)]


def test_loop_shortcut_component(expt):
    """Test loop shortcut of experiment with component

    The component loop occurs first then the "d" parameter loop
    that is defined with the experiment instance.
    """

    loop_expt = loop_shortcut(expt, "component")

    comps = [SimpleNamespace(a=0, b=3), SimpleNamespace(a=2, b=2)]
    assert loop_expt(comps, d=[1, 2, 3], f=3)[0] == [(54, 1), (27, 1), (0, 1)]
    assert loop_expt(comps, d=[1, 2, 3], f=3)[1] == [(192, 2), (128, 2), (64, 2)]


def test_loop_shortcut_incorrect_parameter(model):
    """Test loop shortcut when the parameter is not in model parameter

    If a wrong parameter is chosen, an exception should be raised
    """

    with pytest.raises(Exception, match="'c' is not a model parameter"):
        loop_shortcut(model, "c")
