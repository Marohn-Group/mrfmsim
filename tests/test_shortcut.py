"""Test the shortcut on both Model and Experiment instances"""

from types import SimpleNamespace
from mrfmsim.shortcut import print_shortcut, loop_shortcut
import pytest
from inspect import getclosurevars


class TestStdoutShortcut:
    """Test stdout_shortcut."""

    def test_stdout_input(self, experiment):
        """Test stdout_shortcut with inputs.

        The model should have the modifier added.
        """

        stdout_model = print_shortcut(experiment, ["a", "d"])

        mod = stdout_model.modifiers[-1]
        assert getclosurevars(mod).nonlocals == {
            "inputs": ["a", "d"],
            "units": {},
            "end": "\n",
        }

        assert mod.metadata == "print_inputs(['a', 'd'])"

    def test_stdout_output(self, experiment):
        """Test stdout_shortcut with inputs.

        The model should have the modifier added.
        """

        stdout_model = print_shortcut(experiment, ["k", "m"])
        m_node = stdout_model.get_node("multiply")

        m_node_mod = m_node["modifiers"][-1]
        assert m_node_mod.metadata == "print_output('k')"
        assert getclosurevars(m_node_mod).nonlocals == {
            "output": "k",
            "units": {},
            "end": "\n",
        }

        l_node = stdout_model.get_node("log")
        l_node_mod = l_node["modifiers"][-1]

        assert l_node_mod.metadata == "print_output('m')"
        assert getclosurevars(l_node_mod).nonlocals == {
            "output": "m",
            "units": {},
            "end": "\n",
        }

    def test_stdout_shortcut(self, capsys, experiment):
        """Test stdout shortcut."""

        stdout_model = print_shortcut(experiment, ["d", "c", "k"])
        stdout_model(a=0, b=2, d=2, f=3)
        captured = capsys.readouterr()
        assert captured.out == "d 2\nc 2\nk 0.0\n"


class TestLoopShortcut:
    """Test loop_shortcut."""

    def test_loop_shortcut_raises(self, experiment):
        """Test loop_shortcut raises an exception if parameter not in signature."""

        with pytest.raises(
            Exception, match="Invalid shortcut: 'c' is not a model input."
        ):
            loop_shortcut(experiment, "c")

    def test_loop_shortcut_top(self, experiment_mod):
        """Test loop_shortcut with signature level parameters.

        In some cases, the signature is replaced. The modifier is added to the model.
        """
        loop_model = loop_shortcut(experiment_mod, "component")

        loop_mod = loop_model.modifiers[-1]
        assert loop_mod.metadata == "loop_modifier('component')"
        assert getclosurevars(loop_mod).nonlocals == {"parameter": "component"}


        comps = [SimpleNamespace(a=0, b=2), SimpleNamespace(a=2, b=16)]
        assert loop_model(comps, d=[1, 2, 3], f=3)[0] == [(8, 1), (0, 1), (-8, 1)]
        assert loop_model(comps, d=[1, 2, 3], f=3)[1] == [
            (192, 0.5),
            (128, 0.5),
            (64, 0.5),
        ]

    def test_loop_shortcut_graph(self, experiment):
        """Test loop_shortcut with graph level parameters.

        The whole graph depends on the parameter.
        """
        loop_model = loop_shortcut(experiment, "a")
        loop_mod = loop_model.modifiers[-1]
        assert loop_mod.metadata == "loop_modifier('a')"
        assert getclosurevars(loop_mod).nonlocals == {"parameter": "a"}
        assert loop_model(a=[0, 2], b=2, d=2, f=3) == [(0, 1.0), (128, 2.0)]

    def test_loop_shortcut_single(self, experiment):
        """Test loop_shortcut on single node dependency."""

        loop_model = loop_shortcut(experiment, "b")
        # b dependency is in the node log
        b_node_modifier = loop_model.get_node("log")["modifiers"][-1]

        assert b_node_modifier.metadata == "loop_modifier('b')"
        assert getclosurevars(b_node_modifier).nonlocals == {"parameter": "b"}

        assert loop_model(a=0, b=[2, 4], d=2, f=3) == (0, [1, 0.5])

    def test_loop_shortcut_middle(self, experiment):
        """Test loop_shortcut on subgraph."""

        loop_model = loop_shortcut(experiment, "d", "loop_model")

        # make sure subgraph exists
        assert loop_model.name == "loop_model"
        assert "subnode_d" in loop_model.graph.nodes
        subnode = loop_model.get_node("subnode_d")

        mod = subnode["modifiers"][-1]
        assert mod.metadata == "loop_modifier('d')"
        assert getclosurevars(mod).nonlocals == {"parameter": "d"}
        assert subnode["output"] == "k"

    def test_loop_shortcut_middle_submodel(self, experiment):
        """Test submodel created by loop_shortcut."""

        loop_model = loop_shortcut(experiment, "d", "loop_model")
        subnode = loop_model.get_node("subnode_d")
        submodel = subnode["_func"]
        # make sure the function is decorated
        assert submodel is not subnode["func"]

        assert (
            submodel.description
            == "Submodel generated by loop_shortcut for parameter 'd'."
        )
        assert sorted(list(submodel.graph.nodes)) == ["multiply", "subtract"]

    def test_loop_shortcut_middle_execution(self, experiment):
        """Test loop_shorcut submodel execution."""
        loop_model = loop_shortcut(experiment, "d", "loop_model")
        assert loop_model(a=0, b=2, d=[1, 2], f=3) == ([8, 0], 1.0)
