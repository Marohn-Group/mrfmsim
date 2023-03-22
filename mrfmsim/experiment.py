"""Experiment Class

The class inherits from mmodel.Model class to add certain functionality and defaults.
"""
from mmodel import MemHandler, Model
from mrfmsim.modifier import component_modifier


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
        handler=(MemHandler, {}),
        modifiers: list = None,
        description: str = "",
        returns: list = None,
        component_substitutes: dict = {},
    ):

        modifiers = modifiers or list()  # change non to list
        if component_substitutes:
            # add the component modification to modifiers
            component_mod = (
                component_modifier,
                {"component_substitutes": component_substitutes},
            )

            modifiers = modifiers + [component_mod]

        super().__init__(name, graph, handler, modifiers, description, returns)


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


def job_execution(experiment: Experiment, job: Job):
    """Execute experiment based on the job."""

    for shortcut, kwargs in job.shortcuts:
        experiment = shortcut(experiment, **kwargs)

    return experiment(**job.inputs)
