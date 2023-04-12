from mrfmsim.configuration import (
    import_object,
    MrfmSimLoader,
    MrfmSimDumper,
)
import sys
import pytest
import yaml

# from tests.conftest import graph_equal
from mrfmsim.shortcut import loop_shortcut
from mrfmsim.experiment import Job
from textwrap import dedent
import numpy as np


def test_import_object():
    """Load the function from the user module using dot path."""

    func = import_object("operator.add")
    assert func.__name__ == "add"
    assert func(1, 2) == 3

    func = import_object("numpy.emath.power")
    assert func.__name__ == "power"
    assert np.array_equal(func([2, 4], 2), [4, 16])


def test_import_object_error():
    """Test if it raises an error when the object is not found."""

    with pytest.raises(ModuleNotFoundError, match="Cannot import 'module.addition'."):
        import_object("module.addition")


def test_graph_constructor(experiment):
    """Test the graph constructor parsing the graph correctly."""
    graph_yaml = """
    # graph tag
    !graph
    name: test_graph
    grouped_edges:
        - [add, [subtract, power, log]]
        - [[subtract, power], multiply]
    node_objects:
        add:
            func: !import numpy.add
            output: c
            inputs: [a, [constant, 2]]
        subtract:
            func: !import operator.sub
            output: e
            inputs: [c, d]
        power:
            func: !import math.pow
            output: g
            inputs: [c, f]
        multiply:
            func: !import numpy.multiply
            output: k
            inputs: [e, g]
        log:
            func: !import math.log
            output: m
            inputs: [c, b]
    """

    graph = yaml.load(dedent(graph_yaml), MrfmSimLoader)

    # Check if the two graphs are the same
    # however the function is directly parsed. Therefore
    # we can only check if the function names are the same.

    assert (
        graph.graph["parser"]._parser_dict
        == experiment.graph.graph["parser"]._parser_dict
    )
    assert list(graph.nodes) == list(experiment.graph.nodes)
    assert graph.edges == graph.edges

    for nodes, attrs in graph.nodes.items():
        model_attrs = experiment.graph.nodes[nodes]
        assert attrs.pop("_func").__name__ == model_attrs.pop("_func").__name__
        assert attrs.pop("func").__name__ == model_attrs.pop("func").__name__
        assert attrs == model_attrs


def test_func_constructor():
    """Test if it can load lambda function correctly."""

    lambda_yaml = """
    !func 'lambda a, b: a + b'
    """

    lambda_func = yaml.load(dedent(lambda_yaml), MrfmSimLoader)
    assert lambda_func(1, 2) == 3


def test_execute_constructor():
    """Test if it can load execute object correctly."""

    def add(a, b):
        """Add two numbers."""
        return a + b

    execute_yaml = """
    !execute add(a, b)
    """
    execute_func = yaml.load(dedent(execute_yaml), MrfmSimLoader)

    assert execute_func(add, 1, 2) == 3


def test_import_multi_obj_constructor():
    """Test import_multi_constructor that returns an SimpleNamespace instance."""

    dataobj_str = """
    !import:types.SimpleNamespace
    a: 1
    b: 'test'
    """

    dataobj = yaml.load(dataobj_str, MrfmSimLoader)
    assert dataobj.a == 1
    assert dataobj.b == "test"


def test_job_dumper():
    """Test job dumper can dump the correct values.

    Job dumper currently only supports plain template dumping.
    """
    job_str = """\
    !import:mrfmsim.experiment.Job
    name: test
    inputs:
      a: 1
      b: 2
    shortcuts: []
    """

    job = Job("test", {"a": 1, "b": 2})

    job_yaml = yaml.dump(job, Dumper=MrfmSimDumper, sort_keys=False)

    assert dedent(job_str) == job_yaml


def test_job_constructor():
    """Test job constructor parsing job yaml."""

    job_str = """\
    !import:mrfmsim.experiment.Job
    name: test
    inputs:
      a: 1
      b: 2
    shortcuts:
        - !import mrfmsim.shortcut.loop_shortcut
    """

    job = yaml.load(job_str, Loader=MrfmSimLoader)
    assert job.name == "test"
    assert job.inputs == {"a": 1, "b": 2}
    assert job.shortcuts[0] == loop_shortcut


def test_job_constructor_no_shortcut():
    """Test load job object when shortcuts are not specified."""

    job_str_plain = """\
    !import:mrfmsim.experiment.Job
    name: ''
    inputs: {}
    """

    job = yaml.load(dedent(job_str_plain), Loader=MrfmSimLoader)
    assert job.name == ""
    assert job.inputs == {}
    assert job.shortcuts == []
