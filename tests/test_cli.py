from click.testing import CliRunner
from mrfmsim.cli import cli
import pytest
import os
from textwrap import dedent


@pytest.fixture
def job_file(tmp_path):
    """Create a job yaml file."""

    job_yaml = """
    - !Job
      name: test
      inputs:
        component:
          !Dataobj
          a: 0
          b: 2
        d: [2, 3]
        f: 1
      shortcuts: []
    """

    module_path = tmp_path / "job.yaml"
    module_path.write_text(dedent(job_yaml))
    return module_path


def test_cli_show(expt_file):
    """Test the show command has the correct output.

    The render to the browser is turned off.
    """

    dot_source = """digraph test_graph {
    graph [label="test_experiment(component, d, f)
    returns: (k, m)
    graph: test_graph
    handler: MemHandler()
    modifiers:
      - loop_modifier('d')
      - component_modifier({'component': ['a', 'b']})
    Test experiment with components." 
    labeljust=l labelloc=t ordering=out splines=ortho]
    node [shape=box]
    add [label="add
    addition(a, constant=2)
    return: c
    functype: callable
    Add a constant to the value a."]
    subtract [label="subtract
    subtraction(c, d)
    return: e
    functype: callable
    Subtraction operation."]
    power [label="power
    power(c, f)
    return: g
    functype: callable
    The value of c raise to the power of f."]
    log [label="log
    logarithm(c, b)
    return: m
    functype: callable
    Logarithm operation."]
    multiply [label="multiply
    multiplication(e, g)
    return: k
    functype: callable
    Multiply e and g."]
    add -> subtract [xlabel=c]
    add -> power [xlabel=c]
    add -> log [xlabel=c]
    subtract -> multiply [xlabel=e]
    power -> multiply [xlabel=g]
    }"""

    runner = CliRunner()
    with runner.isolated_filesystem():

        result = runner.invoke(cli, ["--expt", str(expt_file), "show", "--no-view"])
        assert result.exit_code == 0
        assert result.output == ""  # output to the console

        # The name of the file is the name of the graph.
        with open("test_graph.gv", "r") as f:
            dot_graph = f.read()
            dot_graph_source = (
                dot_graph.replace("\t", "").replace("\l", "\n").replace("\n", "")
            )
        assert dot_graph_source == dedent(dot_source).replace("\n", "").replace(
            "    ", ""
        )
        assert os.path.exists("test_graph.gv.pdf")


def test_cli_template(expt_file):
    """Test the template command outputs the value correctly."""

    job_template = """\
    - !Job
      name: ''
      inputs:
        component: ''
        d: ''
        f: ''
      shortcuts: []

    """

    runner = CliRunner()
    result = runner.invoke(cli, ["--expt", str(expt_file), "template"])

    assert result.exit_code == 0
    assert result.output == dedent(job_template)


def test_cli_execute(expt_file, job_file):
    """Test the execute command executes the job correctly."""

    runner = CliRunner()

    result = runner.invoke(
        cli, ["--expt", str(expt_file), "execute", "--job", str(job_file)]
    )

    assert result.exit_code == 0
    assert result.output.strip() == "[(0, 1.0), (-2, 1.0)]"  # echo to console
