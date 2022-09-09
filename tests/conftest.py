"""Configuration for testing

The configuration file provides several default graph fixtures
and test functions

1. `standard_G` - test graph generated using DiGraph, scope: function
2. `mmodel_G` - test graph generated using ModelGraph. scope: function
"""


import pytest
import math
from mmodel import Model, PlainHandler, ModelGraph


@pytest.fixture()
def model():
    """Mock test graph generated using ModelGraph

    The result is:
    k = (a + b - d)(a + b)f
    m = log(a + b, b)
    """

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

    doc = "test object\n\nlong description"

    grouped_edges = [
        ("add", ["subtract", "multiply", "log"]),
        (["subtract", "multiply"], "poly"),
    ]

    node_objects = [
        ("add", addition, ["c"]),
        ("subtract", subtraction, ["e"]),
        ("multiply", multiplication, ["g"]),
        ("poly", polynomial, ["k"]),
        ("log", logarithm, ["m"]),
    ]

    G = ModelGraph(name="test", doc=doc)
    G.add_grouped_edges_from(grouped_edges)
    G.set_node_objects_from(node_objects)

    model = Model(G, (PlainHandler, {}))

    return model


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
        }
        # 'bz': {'unit': '[mT]', "format": ":.3f"}, # comment the entry for testing
    }
