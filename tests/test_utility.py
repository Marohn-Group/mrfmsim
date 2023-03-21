from mrfmsim.experiment import Job
from mrfmsim.utility import job_execution
from mrfmsim.shortcut import loop_shortcut


def test_job_execution(model, experiment):
    """Test the job execution."""

    job = Job(
        "test",
        {"a": [0, 2], "b": 2, "d": 1, "f": 3},
        [(loop_shortcut, {"parameter": "a"})],
    )

    assert job_execution(model, job) == [(8, 1), (192, 2)]
    assert job_execution(experiment, job) == [(8, 1), (192, 2)]
