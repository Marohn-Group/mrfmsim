from mrfmsim.model import Experiment
from mmodel.graph import Graph
from mmodel.utility import construction_dict
from mmodel.metadata import (
    MetaDataFormatter,
    modelformatter,
    format_dictargs,
    format_value,
)


def format_dictkeys(key, value):
    """Formating function that only shows dictionary keys.

    If the value dictionary is empty return None.
    """

    if value:
        return [f"{key}: {list(value.keys())}"]
    else:
        return [f"{key}: None"]


# adjust model formatter for metadata output
_format_dict = modelformatter.format_dict.copy()
_format_dict.update(
    {
        "name": format_value,
        "nodes": format_dictkeys,
        "experiments": format_dictkeys,
        "settings": format_dictargs,
        "description": format_value,
    }
)
_meta_order = ["name", "nodes", "experiments", "settings", "_", "description"]
collectionformatter = MetaDataFormatter(
    _format_dict,
    _meta_order,
    modelformatter.text_wrapper,
    ["settings"],
)


class ExperimentCollection:
    """Create a collection of experiments.

    The class is used to avoid redefining experiment nodes. The experiment
    settings are kept the same. The different experiments are accessed as
    dictionary values.
    """

    def __init__(
        self,
        name,
        description="",
        node_objects=None,
        instructions=None,
        settings=None,
    ):
        """Create a collection of experiments.

        :param list nodes: list of nodes
        :param dict instructions: dictionary of experiment information
            The setting contains the grouped edges and optional experiment kwargs.
        :param dict settings: default experiment settings. They can
            be overwritten by the individual experiment settings provided in the
            instructions.
        """

        self.description = description
        self.name = name

        node_objects = node_objects or []
        self._nodes = {}
        self.add_node_objects_from(node_objects)

        self._experiments = {}
        self._settings = settings or {}

        # create the experiments
        # the _instructions dict is updated during setting experiments
        instructions = instructions or {}
        self._instructions = {}
        for experiment, instruction in instructions.items():
            self[experiment] = instruction

    def __getitem__(self, experiment):
        """Return the experiment with the given key."""

        if experiment not in self._experiments:
            raise KeyError(f"experiment {repr(experiment)} not found")
        return self._experiments[experiment]

    def __setitem__(self, experiment, instruction):
        """Set the experiment with the given key.

        The collection name is copied to the experiment.
        """

        if experiment in self._experiments:
            raise KeyError(f"experiment {repr(experiment)} already exists")

        instruction_copy = instruction.copy()

        edges = instruction_copy.pop("grouped_edges")

        G = Graph(name=f"{experiment}_graph")
        G.add_grouped_edges_from(edges)

        node_obj_list = []

        for node in G.nodes:
            if node not in self._nodes:
                raise KeyError(f"node {repr(node)} not found")
            node_obj_list.append(self._nodes[node])
        G.set_node_objects_from(node_obj_list)

        info = {"collection": self.name, "name": experiment}
        kwargs = {**info, **self._settings, **instruction_copy}
        expt_obj = Experiment(graph=G, **kwargs)
        self._instructions[experiment] = instruction
        self._experiments[experiment] = expt_obj

    def add_node_object(self, node_object):
        """Add node to the collection.

        Raises KeyError if node name already exists.
        """
        if node_object.name in self._nodes:
            raise KeyError(f"node {repr(node_object.name)} already exists")
        self._nodes[node_object.name] = node_object

    def add_node_objects_from(self, node_objects):
        """Add nodes to the collection."""
        for node_object in node_objects:
            self.add_node_object(node_object)

    @property
    def nodes(self):
        """Return the node dictionary."""
        return self._nodes.copy()

    @property
    def node_objects(self):
        """Return a list of node objects."""
        return list(self._nodes.values())

    @property
    def instructions(self):
        """Return the experiment experiment_instructions dictionary."""
        return self._instructions.copy()

    @property
    def settings(self):
        """Return the experiment dictionary."""
        return self._settings.copy()

    @property
    def experiments(self):
        """Return the experiment dictionary."""
        return self._experiments.copy()

    def edit(self, **kwargs):
        """Create a new experiment collection based on new global settings.

        A new collection is created with nodes and experiment_instructions copied.
        """

        con_dict = construction_dict(self, ["node_objects", "instructions", "settings"])
        con_dict.update(kwargs)
        return self.__class__(**con_dict)

    def __str__(self):
        return collectionformatter(self)
