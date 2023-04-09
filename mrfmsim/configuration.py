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


def import_constructor(loader, node):
    """Parse the "!import" tag into a callable object."""

    dotpath = str(loader.construct_scalar(node))
    return load_func(dotpath)


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


def func_representer(dumper: yaml.Dumper, func: types.FunctionType):
    """Represent function scalar."""
    module = sys.modules[func.__module__]
    dotpath = f"{module.__name__}.{func.__name__}"

    return dumper.represent_scalar("!import", dotpath)


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


def job_representer(dumper: yaml.SafeDumper, job: Job):
    """Represent a Job instance."""

    return dumper.represent_mapping(
        "!job", {"name": job.name, "inputs": job.inputs, "shortcuts": job.shortcuts}
    )

def yaml_loader(constructor_dict):
    """Create a yaml loader with special constructors.
    
    :param dict constructor_dict: dictionary of constructors
    :returns: yaml loader class
    """

    class Loader(yaml.SafeLoader):
        """Yaml loader class."""

    for key, value in constructor_dict.items():
        Loader.add_constructor(key, value)
    
    return Loader

default_constructors = {
    "!module": module_constructor,
    "!import": import_constructor,
    "!func": func_constructor,
    "!execute": execute_constructor,
    "!graph": graph_constructor,
    "!experiment": experiment_constructor,
    "!dataobj": dataobj_constructor,
    "!job": job_constructor,
}

MrfmSimLoader = yaml_loader(default_constructors)



def yaml_dumper(representer_dict):
    """Create a yaml dumper with special representer.

    :param dict representer_dict: dictionary of representer
    :returns: yaml dumper class
    """

    class Dumper(yaml.SafeDumper):
        """Yaml dumper class."""

    for key, value in representer_dict.items():
        Dumper.add_representer(key, value)
    
    return Dumper 


default_representers = {
    types.FunctionType: func_representer,
    Job: job_representer,
}

MrfmSimDumper = yaml_dumper(default_representers)
