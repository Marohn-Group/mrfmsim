"""Test Experiment Class by creating the modifiers, shortcuts and component"""
import pytest
from mrfmsim.experiment import Experiment
from mmodel.modifier import loop_modifier
from mmodel import MemHandler
from types import SimpleNamespace


@pytest.fixture
def expt_a(model):
    return Experiment("test_experiment_a", model.graph)


@pytest.fixture
def expt_b(model):
    """The handler should default to MemHandler"""

    component_sub = {"component": ["a", "b"]}

    return Experiment(
        "test_experiment_b",
        model.graph,
        component_substitutes=component_sub,
        modifiers=[(loop_modifier, {"parameter": "d"})],
        description="test experiment",
    )


EXPT_A_STR = """test_experiment_a(a, d, f, b=2)
  returns: k, m
  handler: MemHandler, {}
  modifiers: [component_modifier, {'component_substitutes': {}}]"""

EXPT_B_STR = """test_experiment_b(component, d, f)
  returns: k, m
  handler: MemHandler, {}
  modifiers: [component_modifier, {'component_substitutes': \
{'component': ['a', 'b']}}, loop_modifier, {'parameter': 'd'}]
test experiment"""


def test_experiment_str(expt_a, expt_b):
    """Test if the experiment have the correct output"""

    assert str(expt_a) == EXPT_A_STR
    assert str(expt_b) == EXPT_B_STR


def test_experiment_execution(expt_a, expt_b):
    """Test the experiment execute correctly"""

    assert expt_a(0, 2, 2) == (0, 1)


def test_experiment_execution_modifier(expt_a, expt_b):
    """Test the experiment execute correctly"""

    component = SimpleNamespace(a=0, b=2)

    assert expt_b(component, d=[2, 4], f=2) == [(0, 1), (-8, 1)]


dot_source = """digraph test {
graph [label="\
test_experiment_a(a, d, f, b=2)\
   returns: k, m\
   handler: MemHandler, {}\
   modifiers: [component_modifier, {'component_substitutes': {}}] " 
labeljust=l labelloc=t ordering=out splines=ortho]
node [shape=box]
add [label="add addition(a, b=2) return c "]
subtract [label="subtract subtraction(c, d) return e "]
multiply [label="multiply multiplication(c, f) return g "]
log [label="log logarithm(c, b) return m "]
poly [label="poly polynomial(e, g) return k "]
add -> subtract [xlabel=c]
add -> multiply [xlabel=c]
add -> log [xlabel=c]
subtract -> poly [xlabel=e]
multiply -> poly [xlabel=g]
}"""


def test_experiment_default_draw(expt_a):
    """Test the default graph drawing method"""

    dot_graph = expt_a.draw()

    dot_graph_source = (
        dot_graph.source.replace("\t", "").replace("\l", " ").replace("\n", "")
    )

    assert dot_graph_source == dot_source.replace("\n", "")
