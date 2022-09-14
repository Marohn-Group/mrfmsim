from mrfmsim.experiment import Job
from mrfmsim.utility import job_execution
from mrfmsim.shortcut import loop_shortcut


def test_job_execution(model):
    """Test the job execution"""

    job = Job(
        "test",
        {"a": [0, 2], "b": 2, "d": 2, "f": 2},
        [(loop_shortcut, {"parameter": "a"})],
    )
    result = job_execution(model, job)

    assert result == [(0, 1.0), (16, 2.0)]
