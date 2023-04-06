"""Load and dump configuration files for experiment and jobs."""

import importlib
import sys
import yaml
from mmodel import ModelGraph
from mrfmsim.experiment import Experiment, Job
from inspect import getsource

import types


def load_module(name, path):
    """Load custom module from the path.

    Using ``import name`` to import the module.

    :param str name: name of the package
        The name should avoid overlapping with existing python packages.
    :param str path: python file path for importing
    """

    spec = importlib.util.spec_from_file_location(name, path)
    md = importlib.util.module_from_spec(spec)
    sys.modules[name] = md
    spec.loader.exec_module(md)


def load_func(path):
    """Load functions based on the module path.

    The path is split by the rightmost dot and the
    the module is imported.

    :param str path: path should be separated by a dot
    :returns: loaded function
    """
    module, func = path.rsplit(".", maxsplit=1)
    m = importlib.import_module(module)
    return getattr(m, func)


def module_constructor(loader, node):
    """Load user module with the "!module" tag."""

    # In yaml the tagged objects are parsed first. To have
    # the modules imported first, a compromise is to have the module
    # loading also tagged. The tag can be used under experiment or
    # under the graph. The alternative is to have a multi-page yaml, however,
    # the return would not be a single object

    params = loader.construct_mapping(node, deep=True)

    for name, path in params.items():
        load_module(name, path)


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


def func_representer(dumper: yaml.Dumper, func: types.FunctionType):
    """Represent function scalar."""
    module = sys.modules[func.__module__]
    dotpath = f"{module.__name__}.{func.__name__}"

    return dumper.represent_scalar("!import", dotpath)


def func_constructor(loader, node):
    """Parse the "!import" tag into a callable object."""

    dotpath = str(loader.construct_scalar(node))
    return load_func(dotpath)


def dataobj_constructor(loader, node):
    """Parse the "!dataobj" tag into a SimpleNamespace object."""

    param_dict = loader.construct_mapping(node, deep=True)

    return types.SimpleNamespace(**param_dict)


def experiment_constructor(loader, node):
    """Load experiment.

    The handler, description, and components parameters are optional.
    """

    param_dict = loader.construct_mapping(node, deep=True)

    expt_params = {}
    expt_params["name"] = param_dict["name"]
    expt_params["graph"] = param_dict["graph"]

    for param in ["handler", "description", "replace_inputs", "modifiers"]:
        if param in param_dict:
            expt_params[param] = param_dict[param]

    return Experiment(**expt_params)


def job_constructor(loader: yaml.BaseLoader, node):
    """Load job yaml string to a Job object."""
    param_dict = loader.construct_mapping(node, deep=True)

    return Job(**param_dict)


def lambda_constructor(loader: yaml.BaseLoader, node):
    """Load lambda function from yaml string."""

    return eval(loader.construct_scalar(node))


def job_representer(dumper: yaml.SafeDumper, job: Job):
    """Represent a Job instance."""

    return dumper.represent_mapping(
        "!job", {"name": job.name, "inputs": job.inputs, "shortcuts": job.shortcuts}
    )


class MrfmSimLoader(yaml.SafeLoader):
    """Yaml loader with special constructors."""


MrfmSimLoader.add_constructor("!module", module_constructor)
MrfmSimLoader.add_constructor("!import", func_constructor)
MrfmSimLoader.add_constructor("!lambda", lambda_constructor)
MrfmSimLoader.add_constructor("!graph", graph_constructor)
MrfmSimLoader.add_constructor("!experiment", experiment_constructor)
MrfmSimLoader.add_constructor("!dataobj", dataobj_constructor)
MrfmSimLoader.add_constructor("!job", job_constructor)


class MrfmSimDumper(yaml.Dumper):
    """Yaml dumper with special constructors."""


MrfmSimDumper.add_representer(types.FunctionType, func_representer)
MrfmSimDumper.add_representer(Job, job_representer)
