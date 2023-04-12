"""Load and dump configuration files for experiment and jobs."""

import importlib
import yaml
from mmodel import ModelGraph
from mrfmsim.experiment import Job


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
    """Parse the "!graph" tag into ModelGraph object."""

    param_dict = loader.construct_mapping(node, deep=True)

    graph = ModelGraph(name=param_dict["name"])
    graph.add_grouped_edges_from(param_dict["grouped_edges"])

    for node_name, node_info in param_dict["node_objects"].items():

        func = node_info["func"]
        output = node_info["output"]
        inputs = node_info.get("inputs", None)
        modifiers = node_info.get("modifiers", None)
        graph.set_node_object(
            node_name, func, output=output, inputs=inputs, modifiers=modifiers
        )

    return graph


def execute_constructor(loader: yaml.BaseLoader, node):
    """Prase the "!execute" tag into a lambda function.

    The constructor is to simple function type:

    def outerfunc(func, **kwargs):
        return func(**kwargs)

    The argument is a string that details the function and the arguments.
    For example to use func on a and b, "!execute func(a, b)" is used.
    """

    func_expression = loader.construct_scalar(node)
    params_str = func_expression.replace("(", ",").replace(")", "")

    # dynamically create lambda function
    return eval(f"lambda {params_str}: {func_expression}")


def func_constructor(loader: yaml.BaseLoader, node):
    """Load function from yaml string."""

    return eval(loader.construct_scalar(node))


def yaml_loader(constructor):
    """Create a yaml loader with special constructors.

    :param dict constructor_dict: dictionary of constructors
    :returns: yaml loader class
    """

    class Loader(yaml.SafeLoader):
        """Yaml loader class."""

    for key, value in constructor["constructor"].items():
        Loader.add_constructor(key, value)
    for key, value in constructor["multi_constructor"].items():
        Loader.add_multi_constructor(key, value)
    return Loader


default_constructors = {
    "constructor": {
        "!import": import_constructor,
        "!func": func_constructor,
        "!execute": execute_constructor,
        "!graph": graph_constructor,
    },
    "multi_constructor": {"!import:": import_multi_constructor},
}

MrfmSimLoader = yaml_loader(default_constructors)


def yaml_dumper(representer_dict):
    """Create a yaml dumper with custom representers.

    :param dict representer_dict: dictionary of representer
    :returns: yaml dumper class
    """

    class Dumper(yaml.SafeDumper):
        """Yaml dumper class."""

    for key, value in representer_dict.items():
        Dumper.add_representer(key, value)

    return Dumper


def job_representer(dumper: yaml.SafeDumper, job: Job):
    """Represent a Job instance."""

    return dumper.represent_mapping(
        "!import:mrfmsim.experiment.Job",
        {"name": job.name, "inputs": job.inputs, "shortcuts": job.shortcuts},
    )


default_representers = {
    Job: job_representer,
}

MrfmSimDumper = yaml_dumper(default_representers)
