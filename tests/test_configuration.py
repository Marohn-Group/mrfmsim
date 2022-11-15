from mrfmsim.configuration import (
    load_module,
    load_func,
    MrfmSimLoader,
    MrfmSimDumper,
)
import sys
import pytest
import yaml
from tests.conftest import graph_equal
from mrfmsim.shortcut import loop_shortcut
from mrfmsim.experiment import Job

MODULE_STR = """
# Test python script

import math

def addition(a, b=2):
    return a + b

def subtraction(c, d):
    return c - d

def polynomial(c, f):
    return c**f

def multiplication(e, g):
    return e * g

def logarithm(c, b):
    return math.log(c, b)
"""


@pytest.fixture
def user_module(tmp_path):
    """Create a custom module for testing"""
    module_path = tmp_path / "user_module.py"
    module_path.write_text(MODULE_STR)

    yield module_path
    # runs after the test is complete
    if "user_module" in sys.modules:
        del sys.modules["user_module"]


def test_load_module(user_module):
    """Test the user module in imported"""
    load_module("user_module", user_module)
    assert "user_module" in sys.modules


def test_load_func(user_module):
    """Load the function from user module using dot path"""

    load_module("user_module", user_module)
    func = load_func("user_module.addition")
    assert func.__name__ == "addition"
    assert func(1, 2) == 3


FUNC_YAML = """
!Func numpy.sum
"""


def test_func_constructor():
    """Test function constructor correctly loads function"""

    yaml_func = yaml.load(FUNC_YAML, MrfmSimLoader)
    assert yaml_func.__name__ == "sum"
    assert yaml_func([1, 2]) == 3


GRAPH_YAML = """
# graph tag
!Graph
name: test
grouped_edges:
    - [add, [subtract, poly, log]]
    - [[subtract, poly], multiply]
node_objects:
    add:
        func: !Func user_module.addition
        output: c
    subtract:
        func: !Func user_module.subtraction
        output: e
    poly:
        func: !Func user_module.polynomial
        output: g
    multiply:
        func: !Func user_module.multiplication
        output: k
    log:
        func: !Func user_module.logarithm
        output: m
"""


def test_graph_constructor(model, user_module):
    """Test the graph constructor parse the graph correctly"""
    load_module("user_module", user_module)
    graph = yaml.load(GRAPH_YAML, MrfmSimLoader)

    # check if the two graph are the same
    # however the function are directly parse therefore
    # we can only check if the function names are the same

    assert graph.graph == model.graph.graph
    assert list(graph.nodes) == list(model.graph.nodes)
    assert graph.edges == graph.edges

    for nodes, attrs in graph.nodes.items():
        model_attrs = model.graph.nodes[nodes]
        assert attrs.pop("base_func").__name__ == model_attrs.pop("base_func").__name__
        assert attrs.pop("func").__name__ == model_attrs.pop("func").__name__
        assert attrs == model_attrs

    assert graph_equal(graph, model.graph)


EXPT_YAML = """
!Experiment
user_module:
    !Module
    user_module: {user_module_path}
name: test_experiment
graph:
    !Graph
    name: test
    grouped_edges:
        - [add, [subtract, poly, log]]
        - [[subtract, poly], multiply]
    node_objects:
        add:
            func: !Func user_module.addition
            output: c
        subtract:
            func: !Func user_module.subtraction
            output: e
        poly:
            func: !Func user_module.polynomial
            output: g
        multiply:
            func: !Func user_module.multiplication
            output: k
        log:
            func: !Func user_module.logarithm
            output: m
component_substitutes:
    component: [a, b]
description: test experiment with components
modifiers:
    - [!Func mmodel.loop_modifier, {{'parameter': 'd'}}]
"""


def test_experiment_constructor(user_module, expt):
    """Test experimental constructor"""
    expt_yaml = EXPT_YAML.format(user_module_path=user_module)

    yaml_expt = yaml.load(expt_yaml, MrfmSimLoader)
    assert str(yaml_expt) == str(expt)


def test_func_representer():
    """Test if it identifies object and dump function into the correct tag"""

    def func(a, b):
        return

    func_yaml = yaml.dump(func, Dumper=MrfmSimDumper, sort_keys=False)
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

    job_yaml = yaml.dump(job, Dumper=MrfmSimDumper, sort_keys=False)

    assert JOB_STR == job_yaml


def test_job_constructor():
    """Test job constructor parsing job yaml"""

    job = yaml.load(JOB_STR, Loader=MrfmSimLoader)
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

    job = yaml.load(JOB_STR_PLAIN, Loader=MrfmSimLoader)
    assert job.name == ""
    assert job.inputs == {}
    assert job.shortcuts == []
