from mrfmsim.plugin import (
    assign_plugins,
    register_plugins,
    PluginRegistry,
)
from mrfmsim.model import Experiment
from mrfmsim.node import Node
from mrfmsim.graph import Graph
from mrfmsim.collection import ExperimentCollection

# from mmodel import Graph
import sys

# load the plugins at startup
HOST_MODULE = sys.modules[__name__]
PLUGINS = PluginRegistry()
LOADED_PLUGINS = PluginRegistry()


def get_plugins():
    """Get the plugins."""
    global PLUGINS
    if not PLUGINS:
        register_plugins(group="mrfmsim_plugin", registry=PLUGINS)


def load_plugins(**kwargs):
    """Load plugins that are based on the plugin tuple."""
    get_plugins()
    if not kwargs:
        plugins = PLUGINS.to_plugins()
    else:
        plugins = PLUGINS.to_plugins().select(**kwargs)
    assign_plugins(HOST_MODULE, plugins, LOADED_PLUGINS)
