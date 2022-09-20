from click.testing import CliRunner
from mrfmsim.cli import cli
import pytest
import os

MODULE_STR = """
# Test python script

import math

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

"""

EXPT_YAML = """
!Experiment
user_module:
    !Module
    user_m: {user_module_path}
name: test_experiment
graph:
    !Graph
    name: test
    grouped_edges:
        - [add, [subtract, multiply, log]]
        - [[subtract, multiply], poly]
    node_objects:
        add:
            func: !Func user_m.addition
            returns: [c]
        subtract:
            func: !Func user_m.subtraction
            returns: [e]
        multiply:
            func: !Func user_m.multiplication
            returns: [g]
        poly:
            func: !Func user_m.polynomial
            returns: [k]
        log:
            func: !Func user_m.logarithm
            returns: [m]
component_substitutes: {{}}
description: yaml test experiment
modifiers: []
"""


JOB_YAML = """
- !Job
  name: test
  inputs:
    a: 0
    b: 2
    d: 2
    f: 1
  shortcuts: []
"""


@pytest.fixture
def user_module(tmp_path):
    """Create a custom module for testing"""
    module_path = tmp_path / "user_module.py"
    module_path.write_text(MODULE_STR)
    return module_path


@pytest.fixture
def expt_file(user_module, tmp_path):
    """Create a custom module for testing"""

    expt_yaml = EXPT_YAML.format(user_module_path=user_module)

    module_path = tmp_path / "expt.yaml"
    module_path.write_text(expt_yaml)
    return module_path


@pytest.fixture
def job_file(tmp_path):
    """Create a job yaml file"""

    module_path = tmp_path / "job.yaml"
    module_path.write_text(JOB_YAML)
    return module_path


dot_source = """digraph test {
graph [label="\
test_experiment(a, d, f, b=2)\
   returns: k, m\
   handler: MemHandler, {}\
   modifiers: [component_modifier, {'component_substitutes': {}}] 
yaml test experiment " 
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


def test_cli_show(expt_file):
    """Test the show command has the correct output

    The render to browser is turned off
    """
    runner = CliRunner()
    with runner.isolated_filesystem():

        result = runner.invoke(cli, ["--expt", str(expt_file), "show", "--no-view"])
        assert result.exit_code == 0
        assert result.output == ""  # output to the console

        with open("test.gv", "r") as f:
            dot_graph = f.read()
            dot_graph_source = (
                dot_graph.replace("\t", "").replace("\l", " ").replace("\n", "")
            )

        assert dot_graph_source == dot_source.replace("\n", "")
        assert os.path.exists("test.gv.pdf")


JOB_TEMPLATE = """\
- !Job
  name: ''
  inputs:
    a: ''
    d: ''
    f: ''
    b: ''
  shortcuts: []

"""


def test_cli_template(expt_file):
    """Test the template command outputs the value correctly"""

    runner = CliRunner()
    result = runner.invoke(cli, ["--expt", str(expt_file), "template"])

    assert result.exit_code == 0
    assert result.output == JOB_TEMPLATE


def test_cli_execute(expt_file, job_file):
    """Test the execute command executes the job correctly"""

    runner = CliRunner()

    result = runner.invoke(
        cli, ["--expt", str(expt_file), "execute", "--job", str(job_file)]
    )

    assert result.exit_code == 0
    assert result.output.strip() == "(0, 1.0)"  # echo to console
