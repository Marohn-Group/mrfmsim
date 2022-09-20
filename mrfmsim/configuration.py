"""Load and dump configuration files for experiment and jobs"""

import importlib
import sys
import yaml
from mmodel import ModelGraph
from mrfmsim.experiment import Experiment, Job

import types


def load_module(name, path):
    """load custom module from path

    Using ``import name`` to import the module.

    :param str name: name of the package
        name should avoid overlap with existing python packages
    :param str path: python file path for importing
    """

    spec = importlib.util.spec_from_file_location(name, path)
    md = importlib.util.module_from_spec(spec)
    sys.modules[name] = md
    spec.loader.exec_module(md)


def load_func(path):
    """load function

    The path is split by the right most dot, and the
    module is imported.

    :param str path: path should be separated by dot
    :returns: loaded function
    """
    module, func = path.rsplit(".", maxsplit=1)
    m = importlib.import_module(module)
    return getattr(m, func)


def module_constructor(loader, node):
    """Load user module with !Module tag"""

    # In yaml the tagged objects are parsed first. In order to have
    # the modules imported first, a compromise is to have the module
    # loading also tagged. The tag can be used under experiment or
    # under graph. The alternative is to have a multipage yaml, however,
    # the return would not be a single object

    params = loader.construct_mapping(node)

    for name, path in params.items():
        load_module(name, path)


def graph_constructor(loader, node):
    """Parse !Graph tag into ModelGraph object"""

    param_dict = loader.construct_mapping(node)

    graph = ModelGraph(name=param_dict["name"])
    graph.add_grouped_edges_from(param_dict["grouped_edges"])

    for node_name, node_info in param_dict["node_objects"].items():

        func = node_info["func"]
        inputs = node_info.get("inputs", None)
        graph.set_node_object(node_name, func, node_info["returns"], inputs)

    return graph


# def graph_representer(dumper, graph: ModelGraph):
#     """Parse ModelGraph object into yaml string"""

#     graph_dict = {
#         "name": graph.name,
#         # "grouped_edges": graph.grouped_edges,
#         # "node_objects": graph.node_objects,
#         "grouped_edges": list(graph.edges()),
#         "node_objects": list(graph.nodes()),
#     }

#     return dumper.represent_mapping("!Graph", graph_dict)


def func_representer(dumper: yaml.Dumper, func: types.FunctionType):
    """Represent function scalar"""
    module = sys.modules[func.__module__]
    dotpath = f"{module.__name__}.{func.__name__}"

    return dumper.represent_scalar("!Func", dotpath)


def func_constructor(loader, node):
    """Parse !Func tag into callable object"""

    dotpath = str(loader.construct_scalar(node))
    return load_func(dotpath)


def experiment_constructor(loader, node):
    """Load experiment

    The handler, description, components parameters are optional
    """

    param_dict = loader.construct_mapping(node)

    expt_params = {}
    expt_params['name'] = param_dict['name']
    expt_params["graph"] = param_dict["graph"]


    for param in ["handler", "description", "component_substitutes", "modifiers"]:
        if param in param_dict:
            expt_params[param] = param_dict[param]

    return Experiment(**expt_params)


# def experiment_representer(dumper, experiment: Experiment):
#     """Parse experiment object to yaml string"""

#     experiment_dict = {
#         "graph": experiment.graph,
#         "description": experiment.description,
#         "modifiers": experiment.modifiers,
#     }

#     return dumper.represent_mapping("!Experiment", experiment_dict)


def job_constructor(loader: yaml.BaseLoader, node):
    """Load job yaml string to Job object"""
    param_dict = loader.construct_mapping(node)

    return Job(**param_dict)


def job_representer(dumper: yaml.SafeDumper, job: Job):
    """Represent an Job instance"""

    return dumper.represent_mapping(
        "!Job", {"name": job.name, "inputs": job.inputs, "shortcuts": job.shortcuts}
    )


MrfmsimLoader = yaml.BaseLoader
MrfmsimLoader.add_constructor("!Module", module_constructor)
MrfmsimLoader.add_constructor("!Func", func_constructor)
MrfmsimLoader.add_constructor("!Graph", graph_constructor)
MrfmsimLoader.add_constructor("!Experiment", experiment_constructor)

# base loader is unable to load numbers
MrfmsimJobLoader = yaml.SafeLoader
MrfmsimJobLoader.add_constructor("!Func", func_constructor)
MrfmsimJobLoader.add_constructor("!Job", job_constructor)

MrfmsimDumper = yaml.Dumper
MrfmsimDumper.add_representer(types.FunctionType, func_representer)
MrfmsimDumper.add_representer(Job, job_representer)


# Selective loader and dumper
# current favors a unified one

# def mrfmsim_loader(*tags) -> yaml.SafeLoader:
#     """Add loader based on tags specified"""

#     tag_dict = {
#         "!Module": module_constructor,
#         "!Func": func_constructor,
#         "!Graph": graph_constructor,
#         "!Experiment": experiment_constructor,
#         "!Job": job_constructor,
#     }

#     # The following line creates a new subclass
#     # add_constructor is a classmethod which modifies
#     # the original cls.__dict__
#     loader = type("MrfmsimLoader", (yaml.SafeLoader,), {})
#     for tag in tags:
#         loader.add_constructor(tag, tag_dict[tag])

#     return loader


# def mrfmsim_dumper(*tags) -> yaml.SafeLoader:
#     """Add dumper based on tags specified"""

#     tag_dict = {
#         "!Func": (types.FunctionType, func_representer),
#         # '!Graph': graph_representer,
#         # '!Experiment': experiment_representer,
#         "!Job": (Job, job_representer),
#     }

#     dumper = type("MrfmsimDumper", (yaml.Dumper,), {})
#     for tag in tags:
#         dumper.add_representer(tag, *tag_dict[tag])

#     return dumper
