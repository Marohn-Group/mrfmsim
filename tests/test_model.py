"""Test Experiment Class."""

from types import SimpleNamespace
from textwrap import dedent
from mmodel.shortcut import loop_shortcut
import pytest
from inspect import getclosurevars


def test_experiment_str(experiment_mod, experiment):
    """Test if the experiment has the correct output."""

    ext_str_plain = """\
    test_experiment_plain(a, b, d, f, h=2)
    returns: (k, m)
    return_units: {'k': 'm^2'}
    graph: test_graph
    handler: MemHandler"""

    expt_str = """\
    test_experiment(d_loop, f, replace_obj, h=2)
    returns: (k, m)
    return_units: {'k': 'm^2'}
    graph: test_graph
    handler: MemHandler
    modifiers:
    - loop_input(parameter='d')

    Test experiment with components."""

    assert str(experiment) == dedent(ext_str_plain)
    assert str(experiment_mod) == dedent(expt_str)


def test_experiment_execution(experiment_mod, experiment):
    """Test the experiment execute correctly."""

    assert experiment(0, 2, 1, 3, 2) == (8, 1)

    replace_obj = SimpleNamespace(a=0, b=2)
    assert experiment_mod(d_loop=[1, 2], f=3, replace_obj=replace_obj) == [
        (8, 1),
        (0, 1),
    ]


def test_experiment_component_deepcopy(experiment_mod):
    """Test the experiment components are deepcopied."""

    components = experiment_mod.components
    components["replace_obj"].append("c")

    assert components["replace_obj"] == ["a", "b", "c"]
    assert experiment_mod.components["replace_obj"] == ["a", "b"]


def test_experiment_param_replacements(experiment_mod):
    """Test the experiment param_replacements are the subset of the components.

    The param_replacements should be the actual replacement dictionary.
    """

    components = experiment_mod.components
    components["replace_obj"].append("c")

    assert components["replace_obj"] == ["a", "b", "c"]

    new_expt = experiment_mod.edit(components=components)

    assert new_expt.param_replacements["replace_obj"] == ["a", "b"]

    # make sure it works after the execution
    new_expt(d_loop=[1, 2], f=3, replace_obj=SimpleNamespace(a=0, b=2))

    assert new_expt.param_replacements["replace_obj"] == ["a", "b"]


def test_experiment_param_replacements_deepcopy(experiment_mod):
    """Test the experiment param_replacements are deepcopied."""

    param_replacements = experiment_mod.param_replacements
    param_replacements["replace_obj"] = ["replaced"]

    assert param_replacements["replace_obj"] == ["replaced"]
    assert experiment_mod.param_replacements["replace_obj"] == ["a", "b"]


class TestLoopShortcut:
    """Test that loop_shortcut also works on the experiments."""

    def test_loop_shortcut_raises(self, experiment):
        """Test loop_shortcut raises an exception if parameter not in signature."""

        with pytest.raises(Exception, match="'c' is not a graph model parameter"):
            loop_shortcut(experiment, "c")

    def test_loop_shortcut_signature_exception(self, experiment_mod):
        """Test loop_shortcut with signature level parameters raises an exception."""
        with pytest.raises(
            Exception, match="'replace_obj' is not a graph model parameter"
        ):
            loop_shortcut(experiment_mod, "replace_obj")

    def test_loop_shortcut_graph(self, experiment):
        """Test loop_shortcut with graph level parameters.

        The whole graph depends on the parameter.
        """
        loop_model = loop_shortcut(experiment, "a")
        loop_mod = loop_model.modifiers[-1]

        assert loop_mod.metadata == "loop_input(parameter='a')"
        # assert getclosurevars(loop_mod).nonlocals == {"parameter": "a"}
        assert loop_model(a_loop=[0, 2], b=2, d=2, f=3, h=2) == [(0, 1.0), (128, 2.0)]

    def test_loop_shortcut_single(self, experiment):
        """Test loop_shortcut on single node dependency."""

        loop_model = loop_shortcut(experiment, "b")
        # b dependency is in the node log
        b_node_modifier = loop_model.get_node_object("log").modifiers[-1]

        assert b_node_modifier.metadata == "loop_input(parameter='b')"
        assert getclosurevars(b_node_modifier).nonlocals == {"parameter": "b"}
        assert loop_model(a=0, b_loop=[2, 4], d=2, f=3, h=2) == (0, [1, 0.5])

    def test_loop_shortcut_middle(self, experiment):
        """Test loop_shortcut on subgraph."""

        loop_model = loop_shortcut(experiment, "d", "loop_model")

        # make sure subgraph exists
        assert loop_model.name == "loop_model"
        assert "subnode_d" in loop_model.graph.nodes
        subnode = loop_model.get_node_object("subnode_d")

        mod = subnode.modifiers[-1]

        assert mod.metadata == "loop_input(parameter='d')"
        assert getclosurevars(mod).nonlocals == {"parameter": "d"}
        assert subnode.output == "k"

    def test_loop_shortcut_middle_submodel(self, experiment):
        """Test submodel created by loop_shortcut."""

        loop_model = loop_shortcut(experiment, "d", "loop_model")
        subnode = loop_model.get_node_object("subnode_d")
        # check that the node class is from mrfmsim not mmodel
        assert subnode.__class__.__module__ == "mrfmsim.node"

        assert subnode.node_func is not subnode.func
        assert subnode.doc == "Submodel generated by loop_shortcut for parameter 'd'."
        assert sorted(list(subnode.func.graph.nodes)) == ["multiply", "subtract"]

    def test_loop_shortcut_middle_execution(self, experiment):
        """Test loop_shorcut submodel execution."""
        loop_model = loop_shortcut(experiment, "d", "loop_model")

        assert loop_model(a=0, b=2, d_loop=[1, 2], f=3, h=2) == ([8, 0], 1.0)
