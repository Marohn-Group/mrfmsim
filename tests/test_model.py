"""Test Experiment Class."""

from types import SimpleNamespace
from textwrap import dedent


def test_experiment_str(experiment_mod, experiment):
    """Test if the experiment has the correct output."""

    ext_str_plain = """\
    test_experiment_plain(a, b, d, f, h=2)
    returns: (k, m)
    return_units: {'k': 'm^2'}
    graph: test_graph
    handler: MemHandler"""

    expt_str = """\
    test_experiment(d_loop, f, replace_obj, h=2)
    returns: (k, m)
    return_units: {'k': 'm^2'}
    graph: test_graph
    handler: MemHandler
    modifiers:
    - loop_input(parameter='d')
    components:
    - replace_obj: ['a', 'b']

    Test experiment with components."""

    assert str(experiment) == dedent(ext_str_plain)
    assert str(experiment_mod) == dedent(expt_str)


def test_experiment_execution(experiment_mod, experiment):
    """Test the experiment execute correctly."""

    assert experiment(0, 2, 1, 3, 2) == (8, 1)

    replace_obj = SimpleNamespace(a=0, b=2)
    assert experiment_mod(d_loop=[1, 2], f=3, replace_obj=replace_obj) == [
        (8, 1),
        (0, 1),
    ]


def test_experiment_component_deepcopy(experiment_mod):
    """Test the experiment components are deepcopied."""

    components = experiment_mod.components
    components["replace_obj"].append("c")

    assert components["replace_obj"] == ["a", "b", "c"]
    assert experiment_mod.components["replace_obj"] == ["a", "b"]
