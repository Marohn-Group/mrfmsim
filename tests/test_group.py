import pytest
from mrfmsim.group import ExperimentGroup
from mrfmsim.model import Experiment
from mrfmsim.graph import Graph
from textwrap import dedent



def test_experiment_group_initialization(experiment_group):
    assert experiment_group.name == "Test Group"
    assert experiment_group._node_objects == {"node1": object(), "node2": object()}
    assert experiment_group._model_recipes == {"exp1": Experiment, "exp2": Experiment}
    assert experiment_group._model_defaults == {"default1": "value1", "default2": "value2"}
    assert experiment_group.doc == "This is a test experiment group."

def test_experiment_group_experiments_property(experiment_group):
    assert experiment_group.experiments == experiment_group._models

def test_experiment_group_experiment_defaults_property(experiment_group):
    assert experiment_group.experiment_defaults == experiment_group._model_defaults

def test_experiment_group_str(experiment_group):
    expected_str = """\
    Test Group
    experiments: ['exp1']
    nodes: ['add', 'subtract', 'power', 'multiply', 'log']
    experiment_defaults:
    - components: {'replace_obj': ['a', 'b']}
    - modifiers: [loop_input(parameter='d')]

    This is a test experiment group."""

    assert str(experiment_group) == dedent(expected_str)