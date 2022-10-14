"""Test Experiment Class"""

from types import SimpleNamespace


EXPT_STR = """test_experiment(component, d, f)
  returns: k, m
  handler: MemHandler, {}
  modifiers: [loop_modifier, {'parameter': 'd'}, \
component_modifier, {'component_substitutes': {'component': ['a', 'b']}}]
test experiment with components"""


EXPT_PLAIN_STR = """test_experiment_plain(a, d, f, b=2)
  returns: k, m
  handler: MemHandler, {}
  modifiers: []"""


def test_experiment_str(expt, expt_plain):
    """Test if the experiment have the correct output"""

    assert str(expt) == EXPT_STR
    assert str(expt_plain) == EXPT_PLAIN_STR


def test_experiment_execution(expt, expt_plain):
    """Test the experiment execute correctly"""

    assert expt_plain(0, 1, 3, 2) == (8, 1)

    comp = SimpleNamespace(a=0, b=2)
    assert expt(comp, d=[1, 2], f=3) == [(8, 1), (0, 1)]


dot_source = """digraph test {
graph [label="\
test_experiment_plain(a, d, f, b=2)\
   returns: k, m
   handler: MemHandler, {}\
   modifiers: [] " 
labeljust=l labelloc=t ordering=out splines=ortho]
node [shape=box]
add [label="add addition(a, b=2) return c "]
subtract [label="subtract subtraction(c, d) return e "]
poly [label="poly polynomial(c, f) return g "]
log [label="log logarithm(c, b) return m "]
multiply [label="multiply multiplication(e, g) return k "]
add -> subtract [xlabel=c]
add -> poly [xlabel=c]
add -> log [xlabel=c]
subtract -> multiply [xlabel=e]
poly -> multiply [xlabel=g]
}"""


def test_experiment_default_draw(expt_plain):
    """Test the default graph drawing method"""

    dot_graph = expt_plain.draw()

    dot_graph_source = (
        dot_graph.source.replace("\t", "").replace("\l", " ").replace("\n", "")
    )

    assert dot_graph_source == dot_source.replace("\n", "")
