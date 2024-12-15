"""Experiment Class

The class inherits from ``mmodel.Model`` class to add certain functionality and defaults.
"""

from mmodel import MemHandler, Model
from mrfmsim.modifier import replace_component
import networkx as nx
from mmodel.metadata import MetaDataFormatter, modelformatter, format_dictargs
from mrfmsim.utility import ConfigBase
import copy

# adjust model formatter for metadata output
_format_dict = modelformatter.format_dict.copy()
_format_dict.update({"components": format_dictargs})
_meta_order = [
    "self",
    "returns",
    "return_units",
    "collection",
    "graph",
    "handler",
    "handler_kwargs",
    "modifiers",
    "components",
    "_",
    "doc",
]
exptformatter = MetaDataFormatter(
    _format_dict,
    _meta_order,
    modelformatter.text_wrapper,
    ["modifiers", "components", "handler_kwargs"],
)


class Experiment(Model, ConfigBase):
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
        handler_kwargs: dict = None,
        modifiers: list = None,
        returns: list = None,
        defaults: dict = {},
        doc: str = "",
        components: dict = {},
        allow_duplicated_components: bool = False,
        **kwargs,
    ):

        super().__init__(
            name,
            graph,
            handler,
            handler_kwargs,
            modifiers,
            returns,
            defaults,
            doc,
            allow_duplicated_components=allow_duplicated_components,
            **kwargs,
        )

        # components need to be deepcopied
        self._components = components

        if components:
            # Add the component modification to modifiers.
            component_mod = replace_component(components, allow_duplicated_components)
            self.model_func = component_mod(self.model_func)

        # add units for return values
        self.return_units = {}
        for node, output in nx.get_node_attributes(self.graph, "output").items():
            if output in self.returns:
                unit = getattr(self.get_node_object(node), "output_unit", None)
                if unit:
                    self.return_units[output] = unit

    @property
    def components(self):
        """Return a deepcopy of the components.
        
        The values of the dictionary cotain lists.
        """
        return copy.deepcopy(self._components)

    def __str__(self):
        return exptformatter(self)
