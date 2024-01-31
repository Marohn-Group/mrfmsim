"""Test the shortcut on both Model and Experiment instances"""

from mrfmsim.shortcut import print_shortcut, loop_shortcut
import pytest
from inspect import getclosurevars


class TestModelPrintShortcut:
    """Test the print_shortcut."""

    def test_print_input(self, capsys, experiment):
        """Test print_shortcut to print input values."""

        print_model = print_shortcut(experiment, ["a={a:.2f}", "d={d:.3f}"])

        print_model(a=0, b=2, d=2, f=3)
        captured = capsys.readouterr()
        assert captured.out == "a=0.00\nd=2.000\n"

    def test_print_output(self, capsys, experiment):
        """Test print_shortcut to print output values."""

        print_model = print_shortcut(experiment, ["m={m:.2f}", "k={k:.3f}"], end=" | ")

        print_model(a=0, b=2, d=2, f=3)
        captured = capsys.readouterr()
        assert captured.out == "m=1.00 | k=0.000 | "

    def test_print_mixed(self, capsys, experiment):
        """Test print_shortcut to print input and output values in mixed order."""

        print_model = print_shortcut(
            experiment, ["m={m:.2f}", "a={a}", "k={k:.3f}", "d={d:.3f}"]
        )

        print_model(a=0, b=2, d=1, f=3)
        captured = capsys.readouterr()
        assert captured.out == "a=0\nd=1.000\nm=1.00\nk=8.000\n"


class TestLoopShortcut:
    """Test loop_shortcut."""

    def test_loop_shortcut_raises(self, experiment):
        """Test loop_shortcut raises an exception if parameter not in signature."""

        with pytest.raises(
            Exception, match="Invalid shortcut: 'c' is not a model input."
        ):
            loop_shortcut(experiment, "c")

    def test_loop_shortcut_signature_exception(self, experiment_mod):
        """Test loop_shortcut with signature level parameters raises an exception."""
        with pytest.raises(
            Exception, match="'component' is not included in the graph."
        ):
            loop_shortcut(experiment_mod, "component")

    def test_loop_shortcut_graph(self, experiment):
        """Test loop_shortcut with graph level parameters.

        The whole graph depends on the parameter.
        """
        loop_model = loop_shortcut(experiment, "a")
        loop_mod = loop_model.modifiers[-1]
        assert loop_mod.metadata == "loop_input('a')"
        assert getclosurevars(loop_mod).nonlocals == {"parameter": "a"}
        assert loop_model(a_loop=[0, 2], b=2, d=2, f=3, h=2) == [(0, 1.0), (128, 2.0)]

    def test_loop_shortcut_single(self, experiment):
        """Test loop_shortcut on single node dependency."""

        loop_model = loop_shortcut(experiment, "b")
        # b dependency is in the node log
        b_node_modifier = loop_model.get_node_object("log").modifiers[-1]

        assert b_node_modifier.metadata == "loop_input('b')"
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
        assert mod.metadata == "loop_input('d')"
        assert getclosurevars(mod).nonlocals == {"parameter": "d"}
        assert subnode.output == "k"

    def test_loop_shortcut_middle_submodel(self, experiment):
        """Test submodel created by loop_shortcut."""

        loop_model = loop_shortcut(experiment, "d", "loop_model")
        subnode = loop_model.get_node_object("subnode_d")

        assert subnode.node_func is not subnode.func
        assert subnode.doc == "Submodel generated by loop_shortcut for parameter 'd'."
        assert sorted(list(subnode.func.graph.nodes)) == ["multiply", "subtract"]

    def test_loop_shortcut_middle_execution(self, experiment):
        """Test loop_shorcut submodel execution."""
        loop_model = loop_shortcut(experiment, "d", "loop_model")
        assert loop_model(a=0, b=2, d_loop=[1, 2], f=3, h=2) == ([8, 0], 1.0)
