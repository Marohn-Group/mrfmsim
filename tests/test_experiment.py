"""Test Experiment Class"""

from types import SimpleNamespace
from textwrap import dedent
from mrfmsim.experiment import Job, job_execution
from mrfmsim.shortcut import loop_shortcut


def test_experiment_str(experiment_mod, experiment):
    """Test if the experiment has the correct output."""

    expt_str = """\
    test_experiment(component, d, f)
    returns: (k, m)
    handler: MemHandler()
    modifiers:
      - loop_modifier('d')
      - component_modifier({'component': ['a', 'b']})

    Test experiment with components."""

    ext_str_plain = """\
    test_experiment_plain(a, b, d, f)
    returns: (k, m)
    handler: MemHandler()"""

    assert str(experiment_mod) == dedent(expt_str)
    assert str(experiment) == dedent(ext_str_plain)


def test_experiment_execution(experiment_mod, experiment):
    """Test the experiment execute correctly."""

    assert experiment(0, 2, 1, 3) == (8, 1)

    comp = SimpleNamespace(a=0, b=2)
    assert experiment_mod(comp, d=[1, 2], f=3) == [(8, 1), (0, 1)]


def test_job_execution(experiment):
    """Test the job execution."""

    job = Job(
        "test",
        {"a": [0, 2], "b": 2, "d": 1, "f": 3},
        [(loop_shortcut, {"parameter": "a"})],
    )

    assert job_execution(experiment, job) == [(8, 1), (192, 2)]
