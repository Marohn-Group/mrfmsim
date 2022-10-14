"""Experiment Class

The class inherit from mmodel.Model class to add certain functionality and defaults
"""
from mmodel import MemHandler, Model, draw_graph
from mrfmsim.modifier import component_modifier


class Experiment(Model):
    """Experiment class for mrfmsim

    The class inherits from mmodel.Model with minor modifications.
    The handler is default to MemHandler, and in plotting, the method is default
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
            # add component modification to modifiers
            component_mod = (
                component_modifier,
                {"component_substitutes": component_substitutes},
            )

            modifiers = modifiers + [component_mod]

        super().__init__(name, graph, handler, modifiers, description, returns)

    def draw(self, method: callable = draw_graph):
        """Add the default drawing method to experiment"""
        return super().draw(method)


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
