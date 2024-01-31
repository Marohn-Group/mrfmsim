import math
import operator
import numpy as np
from mrfmsim import Node, ExperimentCollection
import pytest
from textwrap import dedent


@pytest.fixture
def node_objects():
    return [
        Node("add", np.add, inputs=["a", "h"], output="c"),
        Node("subtract", operator.sub, inputs=["c", "d"], output="e"),
        Node("power", math.pow, inputs=["c", "f"], output="g"),
        Node("multiply", np.multiply, inputs=["e", "g"], output="k", output_unit="m^2"),
        Node("log", math.log, inputs=["c", "b"], output="m"),
    ]


@pytest.fixture
def grouped_edges():
    return [
        ("add", ["subtract", "power", "log"]),
        (["subtract", "power"], "multiply"),
    ]


def test_add_node_objects(node_objects):
    """Test the nodes property of the collection."""
    collection = ExperimentCollection("Test_collection")
    collection.add_node_objects_from(node_objects)
    assert collection.node_objects == node_objects
    assert list(collection.nodes.keys()) == [
        "add",
        "subtract",
        "power",
        "multiply",
        "log",
    ]


def test_add_node_object(node_objects):
    """Test the add_node_object raises an exception if the node already exists."""

    collection = ExperimentCollection("Test_collection", "", node_objects)

    with pytest.raises(KeyError, match="node 'add' already exists"):
        collection.add_node_object(node_objects[0])


def test_instruction(node_objects, grouped_edges):
    """Test the instruction property of the collection."""

    instruction = {"grouped_edges": grouped_edges, "doc": "Test individual docstring."}
    collection = ExperimentCollection(
        "test_collection_object",
        "Test collection description.",
        node_objects,
        {"test": instruction},
    )

    assert collection.instructions == {"test": instruction}
    assert collection.description == "Test collection description."
    assert collection["test"].doc == "Test individual docstring."
    assert collection["test"].graph.name == "test_graph"
    assert collection["test"].collection == "test_collection_object"
    print(collection["test"])


def test_instruction_duplicate(node_objects, grouped_edges):
    """Test the instruction property of the collection."""

    instruction = {"grouped_edges": grouped_edges}
    collection = ExperimentCollection(
        "test_collection_object",
        "Test collection description.",
        node_objects,
        {"test": instruction},
    )

    with pytest.raises(KeyError, match="experiment 'test' already exists"):
        collection["test"] = instruction


def test_experiment_settings(node_objects, grouped_edges):
    """Test the experiment settings property of the collection."""

    instruction = {"grouped_edges": grouped_edges}
    collection = ExperimentCollection(
        "test_collection_object",
        "Test collection description.",
        node_objects,
        {"test": instruction},
        {"doc": "Test experiment doc."},
    )

    assert collection["test"].doc == "Test experiment doc."


def test_experiment_settings_overwritten(node_objects, grouped_edges):
    """Test the experiment settings property of the collection overwritten."""

    instruction = {"grouped_edges": grouped_edges, "doc": "Test individual settings."}
    collection = ExperimentCollection(
        "test_collection_object",
        "Test collection description.",
        node_objects,
        {"test": instruction},
        {"doc": "Test experiment doc."},
    )

    assert collection["test"].doc == "Test individual settings."


def test_collection_str_representation(node_objects, grouped_edges):
    """Test the str representation of the collection."""

    collection_str = """\
    test_collection_object
    experiments: ['test']
    nodes: ['add', 'subtract', 'power', 'multiply', 'log']

    Test collection description."""

    instruction = {"grouped_edges": grouped_edges, "doc": "Test instruction."}
    collection = ExperimentCollection(
        "test_collection_object",
        "Test collection description.",
        node_objects,
        {"test": instruction},
    )

    assert str(collection) == dedent(collection_str)

    collection_str = """\
    test_collection
    experiments: None
    nodes: ['add', 'subtract', 'power', 'multiply', 'log']"""

    collection = ExperimentCollection("test_collection", "", node_objects)
    assert str(collection) == dedent(collection_str)


def test_experiment_str_representation(node_objects, grouped_edges):
    """Test the str representation of the experiment.

    Test the collection information is added to experiment object.
    """

    experiment_str = """\
    test(a, b, d, f, h)
    returns: (k, m)
    return_units: {'k': 'm^2'}
    collection: test_collection_object
    graph: test_graph
    handler: MemHandler
    
    Test instruction."""

    instruction = {"grouped_edges": grouped_edges, "doc": "Test instruction."}
    collection = ExperimentCollection(
        "test_collection_object",
        "Test collection description.",
        node_objects,
        {"test": instruction},
    )

    assert str(collection["test"]) == dedent(experiment_str)


def test_experiment_KeyError(node_objects, grouped_edges):
    """Test the experiment KeyError when the experiment does not exist."""

    instruction = {"grouped_edges": grouped_edges, "doc": "Test instruction."}
    collection = ExperimentCollection(
        "test_collection_object",
        "Test collection description.",
        node_objects,
        {"test": instruction},
    )

    with pytest.raises(KeyError, match="experiment 'test2' not found."):
        collection["test2"]


def test_node_error(node_objects, grouped_edges):
    """Test the KeyError when edges contain non-existing nodes."""

    grouped_edges.append(["test_node", "test_node"])

    instruction = {"grouped_edges": grouped_edges, "doc": "Test instruction."}

    with pytest.raises(KeyError, match="node 'test_node' not found"):
        ExperimentCollection(
            "test_collection_object",
            "Test collection description.",
            node_objects,
            {"test": instruction},
        )


def test_edit(node_objects, grouped_edges):
    """Test the edit method of the collection."""

    instruction = {"grouped_edges": grouped_edges}
    collection = ExperimentCollection(
        "Test_collection",
        description="Test collection description.",
        node_objects=node_objects,
        instructions={"test": instruction},
        settings={"doc": "Test experiment doc."},
    )

    new_collection = collection.edit(settings={"doc": "New collection doc."})
    assert new_collection["test"].doc == "New collection doc."
