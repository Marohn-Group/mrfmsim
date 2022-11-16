"""Test Experiment Class"""

from types import SimpleNamespace


EXPT_STR = """test_experiment(component, d, f)
  returns: k, m
  handler: MemHandler, {}
  modifiers: [loop_modifier, {'parameter': 'd'}, component_modifier,
{'component_substitutes': {'component': ['a', 'b']}}]
test experiment with components"""


EXPT_PLAIN_STR = """test_experiment_plain(a, b, d, f)
  returns: k, m
  handler: MemHandler, {}
  modifiers: []"""


def test_experiment_str(experiment_mod, experiment):
    """Test if the experiment have the correct output"""

    assert str(experiment_mod) == EXPT_STR
    assert str(experiment) == EXPT_PLAIN_STR


def test_experiment_execution(experiment_mod, experiment):
    """Test the experiment execute correctly"""

    assert experiment(0, 2, 1, 3) == (8, 1)

    comp = SimpleNamespace(a=0, b=2)
    assert experiment_mod(comp, d=[1, 2], f=3) == [(8, 1), (0, 1)]
