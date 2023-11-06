"""Load and dump configuration files for experiment and jobs."""

import importlib
import yaml
from mrfmsim import Graph, Node, Experiment


def import_object(path):
    """Load object from the path.

    The path is split by the rightmost '.' and the module is imported.
    If the module is not found, the path is split by the next rightmost dot
    and the module is imported. This is repeated until the module is found.
    Otherwise, a ModuleNotFoundError is raised.

    :param str path: dotpath for importing
    """

    maxsplit = 1
    num_dots = path.count(".")
    while True:
        try:  # try split by the rightmost dot
            module, *obj_attrs = path.rsplit(".", maxsplit=maxsplit)
            obj = importlib.import_module(module)
            for attrs in obj_attrs:
                obj = getattr(obj, attrs)
            return obj
        except ModuleNotFoundError:
            maxsplit += 1

            if maxsplit > num_dots:
                raise ModuleNotFoundError(f"Cannot import {repr(path)}.")


def import_multi_constructor(loader, tag_suffix, node):
    """Parse the "!import:" multi tag into an object with parameters.

    The node is parsed as a dictionary.
    """
    obj = import_object(tag_suffix)
    params = loader.construct_mapping(node, deep=True)
    return obj(**params)


def import_constructor(loader, node):
    """Parse the "!import" tag into object."""

    path = loader.construct_scalar(node)
    return import_object(path)


def graph_constructor(loader, node):
    """Parse the "!Graph" tag into Graph object.

    The node are listed as a dictionary of node name and node object.
    The design is for a clearer view of nodes. To change this
    behavior, change the graph_constructor.
    """

    param_dict = loader.construct_mapping(node, deep=True)

    graph = Graph(name=param_dict["name"])
    graph.add_grouped_edges_from(param_dict["grouped_edges"])

    for node_name, node_info in param_dict["node_objects"].items():
        graph.set_node_object(Node(node_name, **node_info))

    return graph


def experiment_constructor(loader, node):
    """Parse the "!Experiment" tag into Experiment object."""

    param_dict = loader.construct_mapping(node, deep=True)

    return Experiment(**param_dict)


def func_multi_constructor(loader: yaml.BaseLoader, tag_suffix, node):
    """Load the "!func:" tag from yaml string.

    The constructor parses !func:function "lambda a, b: a + b".
    In the example, the name of the function is set to "function",
    the function is the lambda expression. The doc is None, set
    doc at the node level.
    """
    node = loader.construct_scalar(node)

    func = eval(node)
    func.__name__ = tag_suffix

    return func


def yaml_loader(constructor):
    """Create a yaml loader with special constructors.

    :param dict constructor_dict: dictionary of constructors
    :returns: yaml loader class
    """

    class Loader(yaml.SafeLoader):
        pass

    for key, value in constructor["constructor"].items():
        Loader.add_constructor(key, value)
    for key, value in constructor["multi_constructor"].items():
        Loader.add_multi_constructor(key, value)
    return Loader


default_constructors = {
    "constructor": {
        "!import": import_constructor,
        "!Graph": graph_constructor,
        "!Experiment": experiment_constructor,
    },
    "multi_constructor": {
        "!import:": import_multi_constructor,
        "!func:": func_multi_constructor,
    },
}

MrfmSimLoader = yaml_loader(default_constructors)
