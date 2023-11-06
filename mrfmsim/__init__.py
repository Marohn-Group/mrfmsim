from mrfmsim.plugin import load_plugins
from mrfmsim.experiment import Experiment
from mrfmsim.node import Node
from mmodel import Graph
import sys

# load the plugins at startup
mrfmsim_module = sys.modules[__name__]
PLUGINS = load_plugins(mrfmsim_module, "mrfmsim_plugin")
