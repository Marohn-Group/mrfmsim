"""Configuration for testing

The configuration file provides several default graph fixtures
and test functions
"""


import pytest
import math
from mmodel import ModelGraph
from mmodel.modifier import loop_input
from mrfmsim.model import Experiment
from textwrap import dedent
import numpy as np
import operator


@pytest.fixture
def modelgraph():
    """Model graph for creating experiment and model.

    The results are:
    k = (a + 2 - d)(a + 2)^f
    m = log(a + 2, b)
    """

    grouped_edges = [
        ("add", ["subtract", "power", "log"]),
        (["subtract", "power"], "multiply"),
    ]

    node_objects = [
        ("add", np.add, "c", ["a", ("constant", 2)]),
        ("subtract", operator.sub, "e", ["c", "d"]),
        ("power", math.pow, "g", ["c", "f"]),
        ("multiply", np.multiply, "k", ["e", "g"]),
        ("log", math.log, "m", ["c", "b"]),
    ]

    G = ModelGraph(name="test_graph")
    G.add_grouped_edges_from(grouped_edges)
    G.set_node_objects_from(node_objects)

    return G


@pytest.fixture
def experiment(modelgraph):
    """Test experiment instance with default settings."""
    return Experiment("test_experiment_plain", modelgraph)


@pytest.fixture
def experiment_mod(modelgraph):
    """Test experiment instance with modifiers and component substitutions."""

    return Experiment(
        "test_experiment",
        modelgraph,
        replace_inputs={"component": ["a", "b"]},
        modifiers=[loop_input(parameter="d")],
        description="Test experiment with components.",
    )


@pytest.fixture
def units():
    return {
        "b1": {
            "unit": "[mT]",
            "format": ":.3f",
            "description": "transverse magnetic field",
        },
        "b0": {
            "unit": "[mT]",
            "format": ":.3e",
            "description": "longitudinal magnetic field",
        },
        "b_tot": {
            "unit": "[mT]",
            "format": ":.1f",
            "description": "total magnetic field",
        },
    }


@pytest.fixture
def expt_file(tmp_path):
    """Create a custom module for testing."""

    expt_yaml = """\
    !import:mrfmsim.model.Experiment
    name: test_experiment
    graph:
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
    replace_inputs: {component: [a, b]}
    description: Test experiment with components.
    modifiers: [!import:mmodel.modifier.loop_input {parameter: d}]
    """

    expt_yaml = dedent(expt_yaml)

    module_path = tmp_path / "expt.yaml"
    module_path.write_text(expt_yaml)
    return module_path
