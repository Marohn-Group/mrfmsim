from mrfmsim.configuration import (
    load_module,
    load_func,
    MrfmsimLoader,
    MrfmsimJobLoader,
    MrfmsimDumper,
)
import sys
import pytest
import yaml
from tests.conftest import graph_equal
from mrfmsim.shortcut import loop_shortcut
from mrfmsim.modifier import component_modifier
from mrfmsim.experiment import Experiment, Job
from mmodel import ModelGraph, Model

MODULE_STR = """
# Test python script

import math

def addition(a, b=2):
    return a + b

def subtraction(c, d):
    return c - d

def multiplication(c, f):
    return c * f

def polynomial(e, g):
    return e * g

def logarithm(c, b):
    return math.log(c, b)

"""


@pytest.fixture
def user_module(tmp_path):
    """Create a custom module for testing"""
    module_path = tmp_path / "user_module.py"
    module_path.write_text(MODULE_STR)
    return module_path


def test_load_module(user_module):
    """Test the user module in imported"""
    load_module("user_module", user_module)
    assert "user_module" in sys.modules
    del sys.modules["user_module"]


def test_load_func(user_module):
    """Load the function from user module using dot path"""

    load_module("user_module", user_module)
    func = load_func("user_module.addition")
    assert func.__name__ == "addition"
    assert func(1, 2) == 3
    del sys.modules["user_module"]


FUNC_YAML = """
!Func numpy.sum
"""


def test_func_constructor():
    """Test function constructor correctly loads function"""

    yaml_func = yaml.load(FUNC_YAML, MrfmsimLoader)
    assert yaml_func.__name__ == "sum"
    assert yaml_func([1, 2]) == 3


GRAPH_YAML = """
# graph tag
!Graph
name: test
grouped_edges:
    - [add, [subtract, multiply, log]]
    - [[subtract, multiply], poly]
node_objects:
    add:
        func: !Func user_module.addition
        returns: [c]
    subtract:
        func: !Func user_module.subtraction
        returns: [e]
    multiply:
        func: !Func user_module.multiplication
        returns: [g]
    poly:
        func: !Func user_module.polynomial
        returns: [k]
    log:
        func: !Func user_module.logarithm
        returns: [m]
"""


def test_graph_constructor(model, user_module):
    """Test the graph constructor parse the graph correctly"""
    load_module("user_module", user_module)
    graph = yaml.load(GRAPH_YAML, MrfmsimLoader)

    assert graph_equal(graph, model._graph)


EXPT_YAML = """
!Experiment
user_module:
    !Module
    user_m: {user_module_path}
graph:
    !Graph
    name: test
    grouped_edges:
        - [add, [subtract, multiply, log]]
        - [[subtract, multiply], poly]
    node_objects:
        add:
            func: !Func user_module.addition
            returns: [c]
        subtract:
            func: !Func user_module.subtraction
            returns: [e]
        multiply:
            func: !Func user_module.multiplication
            returns: [g]
        poly:
            func: !Func user_module.polynomial
            returns: [k]
        log:
            func: !Func user_module.logarithm
            returns: [m]
component_substitutes:
    component: [a, b]
description: yaml test experiment
modifiers:
    - [!Func mmodel.loop_modifier, {{'parameter': 'd'}}]
"""

EXPT_STR = """test model
  signature: component, d, f
  returns: k, m
  handler: MemHandler, {}
  modifiers: [component_modifier, {'component_substitutes': \
{'component': ['a', 'b']}}, loop_modifier, {'parameter': 'd'}]
yaml test experiment"""


def test_experiment_constructor(user_module):
    """Test experimental constructor"""
    expt_yaml = EXPT_YAML.format(user_module_path=user_module)

    yaml_expt = yaml.load(expt_yaml, MrfmsimLoader)
    assert str(yaml_expt) == EXPT_STR


# def test_experiment_representer(model):
#     """Test experiment representer parse experiment object"""

#     # turn the model into an experiment object

#     model.modifier = [
#         component_modifier,
#         {"component_substitutes": {"component": ["a", "b"]}},
#     ]

#     experiment_dumper = yaml.Dumper
#     experiment_dumper.add_representer(types.FunctionType, func_representer)
#     experiment_dumper.add_representer(Model, experiment_representer)

#     expt_yaml = yaml.dump(model, Dumper=experiment_dumper, sort_keys=False)


def test_func_representer():
    """Test if it identifies object and dump function into the correct tag"""

    def func(a, b):
        return

    func_yaml = yaml.dump(func, Dumper=MrfmsimDumper, sort_keys=False)
    assert func_yaml.strip() == "!Func 'tests.test_configuration.func'"


JOB_STR = """\
!Job
name: test
inputs:
  a: 1
  b: 2
shortcuts:
- !Func 'mrfmsim.shortcut.loop_shortcut'
"""


def test_job_dumper():
    """Test job dumper can dump the correct values

    Job dumper currently only supports plain template dumping
    """

    job = Job("test", {"a": 1, "b": 2}, [loop_shortcut])

    job_yaml = yaml.dump(job, Dumper=MrfmsimDumper, sort_keys=False)

    assert JOB_STR == job_yaml


def test_job_constructor():
    """Test job constructor parsing job yaml"""

    job = yaml.load(JOB_STR, Loader=MrfmsimJobLoader)
    assert job.name == "test"
    assert job.inputs == {"a": 1, "b": 2}
    assert job.shortcuts[0] == loop_shortcut


JOB_STR_PLAIN = """\
!Job
name: ''
inputs: {}
"""


def test_job_constructor_no_shortcut():
    """Test load job object when shortcuts are not specified"""

    job = yaml.load(JOB_STR_PLAIN, Loader=MrfmsimJobLoader)
    assert job.name == ""
    assert job.inputs == {}
    assert job.shortcuts == []


# def test_mrfmsim_loader():
#     """Test mrfmsim_loader loads the correct constructors"""
#     loader = mrfmsim_loader("!Job", "!Graph")
#     cons_dict = loader.yaml_constructors

#     assert "!Job" in cons_dict and "!Graph" in cons_dict
#     assert "!Experiment" not in cons_dict and "!Func" not in cons_dict
#     loader = mrfmsim_loader()


# def test_mrfmsim_dumper():
#     """Test mrfmsim_loader loads the correct constructors"""
#     dumper = mrfmsim_dumper("!Job")

#     assert "!Job" in dumper.yaml_representers
#     assert "!Func" not in dumper.yaml_representers
