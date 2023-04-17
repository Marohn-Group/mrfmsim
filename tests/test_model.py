"""Test Experiment and Job Class."""

from types import SimpleNamespace
from textwrap import dedent


def test_experiment_str(experiment_mod, experiment):
    """Test if the experiment has the correct output."""

    expt_str = """\
    test_experiment(component, d, f)
    returns: (k, m)
    graph: test_graph
    handler: MemHandler
    modifiers:
      - loop_input('d')
      - replace_component({'component': ['a', 'b']})

    Test experiment with components."""

    ext_str_plain = """\
    test_experiment_plain(a, b, d, f)
    returns: (k, m)
    graph: test_graph
    handler: MemHandler"""

    assert str(experiment_mod) == dedent(expt_str)
    assert str(experiment) == dedent(ext_str_plain)


def test_experiment_execution(experiment_mod, experiment):
    """Test the experiment execute correctly."""

    assert experiment(0, 2, 1, 3) == (8, 1)

    comp = SimpleNamespace(a=0, b=2)
    assert experiment_mod(comp, d=[1, 2], f=3) == [(8, 1), (0, 1)]
