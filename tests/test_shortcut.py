"""Test the shortcut on both Model and Experiment instances"""

from types import SimpleNamespace
from mrfmsim.shortcut import loop_shortcut, remodel_shortcut
import pytest
from inspect import signature


def test_loop_shortcut(model, experiment):
    """Test loop shortcut.

    The resulting value should create a looped model of d. For experiment_mod,
    the d is already looped.
    """

    loop_model = loop_shortcut(model, "d")

    assert loop_model(a=0, b=2, d=[1, 2], f=3) == ([8, 0], 1.0)

    loop_expt = loop_shortcut(experiment, "f")

    assert loop_expt(a=0, b=2, d=1, f=[3, 4]) == ([8, 16], 1.0)


def test_loop_shortcut_single_node(model, experiment):
    """Test loop shortcut when the subgraph is a single node.

    The resulting value should create a looped model of d. For experiment_mod,
    the d is already looped.
    """

    loop_model = loop_shortcut(loop_shortcut(model, "d"), "d")
    assert loop_model(a=0, b=2, d=[[1, 2], [1, 2]], f=3) == ([[8, 0], [8, 0]], 1.0)

    loop_model = loop_shortcut(loop_shortcut(model, "f"), "f")
    # the output is actually k1, p1, k2, p2
    assert loop_model(a=0, b=2, d=1, f=[[1, 2], [3, 4]]) == ([[2, 4], [8, 16]], 1.0)


def test_loop_shortcut_top_level(model, experiment):
    """Test loop shortcut when the parameter is used at the top level.

    The resulting value should create a looped model of b
    (a top level parameter, as in the subgraph is the same as the graph).
    """

    loop_model = loop_shortcut(model, "b")
    assert loop_model(a=0, b=[2, 4], d=2, f=3) == (0, [1, 0.5])

    loop_expt = loop_shortcut(experiment, "b")
    assert loop_expt(a=0, b=[2, 4], d=2, f=3) == (0, [1, 0.5])


def test_loop_shortcut_component(experiment_mod):
    """Test loop shortcut of experiment with component.

    The component loop occurs first then the "d" parameter loop
    that is defined with the experiment instance.
    """

    loop_expt = loop_shortcut(experiment_mod, "component")

    comps = [SimpleNamespace(a=0, b=2), SimpleNamespace(a=2, b=16)]
    assert loop_expt(comps, d=[1, 2, 3], f=3)[0] == [(8, 1), (0, 1), (-8, 1)]
    assert loop_expt(comps, d=[1, 2, 3], f=3)[1] == [(192, 0.5), (128, 0.5), (64, 0.5)]


def test_loop_shortcut_incorrect_parameter(model):
    """Test loop shortcut when the parameter is not in model parameter.

    If a wrong parameter is chosen, an exception should be raised.
    """

    with pytest.raises(Exception, match="'c' is not a model parameter"):
        loop_shortcut(model, "c")


def test_loop_shortcut_with_stdout(model, experiment, capsys):
    """Test loop shortcut when the parameter is not in model parameter.

    If a wrong parameter is chosen, an exception should be raised.
    """

    loop_model = loop_shortcut(model, "a", {})
    loop_model(a=[0, 2], b=2, d=2, f=3)

    captured = capsys.readouterr()
    assert captured.out == "0 | a 0 | k 0 , m 1.0\n1 | a 2 | k 128 , m 2.0\n"

    unit = {"k": {"unit": "a.u.", "format": ":.3f"}}
    loop_model = loop_shortcut(experiment, "a", {"units": unit})
    loop_model(a=[0, 2], b=2, d=2, f=3)

    captured = capsys.readouterr()
    assert (
        captured.out
        == "0 | a 0 | k 0.000 a.u., m 1.0\n1 | a 2 | k 128.000 a.u., m 2.0\n"
    )

def test_remodel_shortcut(model, experiment_mod):
    """Test remodel shortcut."""

    # get rid of modifiers
    mod_model = remodel_shortcut(experiment_mod, modifiers=[])

    assert list(signature(mod_model).parameters.keys()) == ['a', 'b', 'd', 'f']
    assert mod_model.modifiers == []
