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
    test_experiment(component, d_loop, f, h=2)
    returns: (k, m)
    return_units: {'k': 'm^2'}
    graph: test_graph
    handler: MemHandler
    modifiers:
    - loop_input('d')
    components:
    - component: [('a', 'a1'), ('b', 'b1')]

    Test experiment with components."""

    assert str(experiment) == dedent(ext_str_plain)
    assert str(experiment_mod) == dedent(expt_str)


def test_experiment_execution(experiment_mod, experiment):
    """Test the experiment execute correctly."""

    assert experiment(0, 2, 1, 3, 2) == (8, 1)

    comp = SimpleNamespace(a1=0, b1=2)
    assert experiment_mod(comp, d_loop=[1, 2], f=3) == [(8, 1), (0, 1)]
