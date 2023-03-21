from mrfmsim.experiment import Experiment, Job


def job_execution(experiment: Experiment, job: Job):
    """Execute experiment based on job."""

    for shortcut, kwargs in job.shortcuts:
        experiment = shortcut(experiment, **kwargs)

    return experiment(**job.inputs)
