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
from textwrap import dedent


def test_load_module(user_module):
    """Test the user module in imported."""
    load_module("user_module", user_module)
    assert "user_module" in sys.modules


def test_load_func(user_module):
    """Load the function from user module using dot path."""

    load_module("user_module", user_module)
    func = load_func("user_module.addition")
    assert func.__name__ == "addition"
    assert func(1, 2) == 3


def test_func_constructor():
    """Test function constructor correctly loads function."""

    func_yaml = """\
    !Func numpy.sum
    """
    yaml_func = yaml.load(dedent(func_yaml), MrfmSimLoader)
    assert yaml_func.__name__ == "sum"
    assert yaml_func([1, 2]) == 3


def test_graph_constructor(experiment, user_module):
    """Test the graph constructor parsing the graph correctly."""
    graph_yaml = """
    # graph tag
    !Graph
    name: test
    grouped_edges:
        - [add, [subtract, power, log]]
        - [[subtract, power], multiply]
    node_objects:
        add:
            func: !Func user_module.addition
            output: c
        subtract:
            func: !Func user_module.subtraction
            output: e
        power:
            func: !Func user_module.power
            output: g
        multiply:
            func: !Func user_module.multiplication
            output: k
        log:
            func: !Func user_module.logarithm
            output: m
    """

    load_module("user_module", user_module)
    graph = yaml.load(dedent(graph_yaml), MrfmSimLoader)

    # check if the two graph are the same
    # however the function are directly parse therefore
    # we can only check if the function names are the same

    assert graph.graph == experiment.graph.graph
    assert list(graph.nodes) == list(experiment.graph.nodes)
    assert graph.edges == graph.edges

    for nodes, attrs in graph.nodes.items():
        model_attrs = experiment.graph.nodes[nodes]
        assert attrs.pop("_func").__name__ == model_attrs.pop("_func").__name__
        assert attrs.pop("func").__name__ == model_attrs.pop("func").__name__
        assert attrs == model_attrs

    # assert graph_equal(graph, model.graph)


def test_experiment_constructor(expt_file, experiment_mod):
    """Test experimental constructor."""

    with open(expt_file, "r") as f:
        yaml_expt = yaml.load(f.read(), MrfmSimLoader)
    assert str(yaml_expt) == str(experiment_mod)


def test_func_representer():
    """Test if it identifies object and dump function into the correct tag."""

    def func(a, b):
        return

    func_yaml = yaml.dump(func, Dumper=MrfmSimDumper, sort_keys=False)
    assert func_yaml.strip() == "!Func 'tests.test_configuration.func'"


def test_dataobj_constructor():
    """Test dataobj constructor."""

    dataobj_str = """
    !Dataobj
    a: 1
    b: 'test'
    """

    dataobj = yaml.load(dataobj_str, MrfmSimLoader)
    assert dataobj.a == 1
    assert dataobj.b == "test"


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
    """Test job dumper can dump the correct values.

    Job dumper currently only supports plain template dumping.
    """

    job = Job("test", {"a": 1, "b": 2}, [loop_shortcut])

    job_yaml = yaml.dump(job, Dumper=MrfmSimDumper, sort_keys=False)

    assert JOB_STR == job_yaml


def test_job_constructor():
    """Test job constructor parsing job yaml."""

    job = yaml.load(JOB_STR, Loader=MrfmSimLoader)
    assert job.name == "test"
    assert job.inputs == {"a": 1, "b": 2}
    assert job.shortcuts[0] == loop_shortcut


def test_job_constructor_no_shortcut():
    """Test load job object when shortcuts are not specified."""

    job_str_plain = """\
    !Job
    name: ''
    inputs: {}
    """

    job = yaml.load(dedent(job_str_plain), Loader=MrfmSimLoader)
    assert job.name == ""
    assert job.inputs == {}
    assert job.shortcuts == []
