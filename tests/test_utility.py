from mrfmsim.experiment import Job
from mrfmsim.utility import job_execution
from mrfmsim.shortcut import loop_shortcut


def test_job_execution(model, expt_plain):
    """Test the job execution"""

    job = Job(
        "test",
        {"a": [0, 2], "b": 2, "d": 1, "f": 3},
        [(loop_shortcut, {"parameter": "a"})],
    )

    assert job_execution(model, job) == [(8, 1, 9), (192, 2, 81)]
    assert job_execution(expt_plain, job) == [(8, 1, 9), (192, 2, 81)]
