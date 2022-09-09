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
        graph,
        handler=(MemHandler, {}),
        description: str = "",
        component_substitutes: dict = {},
        modifiers: list = [],
    ):
        # add component modification to modifiers
        component_mod = (
            component_modifier,
            {"component_substitutes": component_substitutes},
        )
        modifiers = [component_mod] + modifiers

        super().__init__(graph, handler, description, modifiers)

    def draw(self, method: callable = draw_graph):
        """Add the default drawing method to experiment"""
        return super().draw(method)
