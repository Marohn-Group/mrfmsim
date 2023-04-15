"""Experiment Class

The class inherits from mmodel.Model class to add certain functionality and defaults.
"""
from mmodel import MemHandler, Model
from mrfmsim.modifier import replace_component


class Experiment(Model):
    """Experiment class for mrfmsim.

    The class inherits from mmodel.Model with minor modifications.
    The handler defaults to MemHandler, and in plotting, the method defaults
    to draw_graph.
    """

    def __init__(
        self,
        name,
        graph,
        handler=MemHandler,
        modifiers: list = None,
        description: str = "",
        returns: list = None,
        replace_inputs: dict = {},
        **kwargs,
    ):

        modifiers = modifiers or list()  # change non to list
        if replace_inputs:
            # Add the component modification to modifiers.
            component_mod = replace_component(replace_inputs)
            modifiers = modifiers + [component_mod]

        super().__init__(
            name, graph, handler, modifiers, description, returns, **kwargs
        )


class Job:
    """Create Experiment execution job.

    :param str name: name of the job
    :param dict inputs: input needed for model
    :param list shortcuts: additional shortcut modification of the model
    """

    def __init__(self, name, inputs, shortcuts: list = []):
        self.name = name
        self.shortcuts = shortcuts
        self.inputs = inputs


def job_execution(experiment, job: Job):
    """Execute experiment based on the job."""

    for shortcut, kwargs in job.shortcuts:
        experiment = shortcut(experiment, **kwargs)

    return experiment(**job.inputs)
