from types import ModuleType
import sys
import warnings
from importlib.metadata import entry_points
from importlib import import_module
from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import reduce


@dataclass(frozen=True)
class UnloadedPlugin:
    """Delay the loading of the entry point module.

    The class is very similar to the importlib.metadata.EntryPoint
    class with an added format for mrfmsim plugin system.
    The entry points are converted into two parts:

    - Endpoint: The submodule and attribute used to load the plugin from
      the host module.

      - ep_module: The submodule name.
      - ep_attr: The attribute name.

    - Plugin: The module and attribute used to load the plugin from the
      plugin module.

      - module: The module name.
      - attr: The attribute name.
      - plugin_path: The full path of the plugin, if the attribute is None,
        the path is the module name.
    """

    endpoint: str
    module: str
    attr: str
    ep_module: str = field(init=False)
    ep_attr: str = field(init=False)
    plugin_path: str = field(init=False)

    def __post_init__(self):
        ep_module, ep_attr = self.endpoint.split(".")
        if self.attr:
            plugin_path = f"{self.module}.{self.attr}"
        else:
            plugin_path = self.module
        vars(self).update(
            {"ep_module": ep_module, "ep_attr": ep_attr, "plugin_path": plugin_path}
        )

    def matches(self, **params):
        """Check if the plugin matches the given parameters.

        :param params: The keyword parameters to check.
            Returns True if all the parameters match the plugin.
        """
        return all(getattr(self, key) == value for key, value in params.items())

    def load(self):
        """Load the plugin module."""
        module = import_module(self.module)
        attrs = filter(None, (self.attr or "").split("."))
        return reduce(getattr, attrs, module)


class Plugins(tuple):
    """Class for a collection of entry points.

    The class is very similar to the EntryPoints class with
    added __repr__ method.
    """

    __slots__ = ()

    def select(self, **params):
        """Select entry points from self that match the given parameters.

        Here we use Plugins to construct the result.
        """

        return self.__class__(plugin for plugin in self if plugin.matches(**params))

    def unique(self, param):
        """Select the unique entry points from self that match the given parameters.

        A generator is outputted. Here we do not use set to avoid entry
        order change.
        """

        value_list = []
        for plugin in self:
            value = getattr(plugin, param)
            if value not in value_list:
                value_list.append(value)
        return value_list


class LazyModule(ModuleType):
    """Transform a module to lazy load all its plugins.

    The delayed load is done by loading the attribute when the attribute
    is accessed.
    """

    def __getattribute__(self, attribute):

        value = super().__getattribute__(attribute)
        if isinstance(value, UnloadedPlugin):
            value = value.load()
            setattr(self, attribute, value)
        return value


class PluginRegistry(Mapping):
    """Store the plugin registry.

    The format of the registry is a dictionary of (plugin, dst_attr).
    The dst_attr represents the attribute name of the plugin in the submodule.
    Modification of the registry can only be achieved by the register method.
    Only add plugins are allowed, since there is no un-import functionality
    of the mrfmsim plugin system.
    """

    def __init__(self):
        self._registry = {}

    def register(self, plugin: UnloadedPlugin, endpoint: str | None):
        self._registry[plugin] = endpoint

    def to_plugins(self):
        return Plugins(self._registry.keys())

    def list_plugins(self, param: str):
        """List the plugins in the registry to a string output."""

        plugins = self.to_plugins()

        param_keys = plugins.unique(param)
        sorted_keys = sorted(list(param_keys))
        stdout = []
        for key in sorted_keys:
            stdout.append(f"{key}:")
            for plugin in plugins.select(**{param: key}):
                plugin_str = plugin.plugin_path
                if self._registry[plugin]:
                    plugin_str += f" -> {self._registry[plugin]}"
                stdout.append(f"\t{plugin_str}")

        return "\n".join(stdout)

    def __repr__(self) -> str:
        """Return the string representation of the registry.

        Defaults to listing by module. To view other listings
        use the list_plugins method.
        """
        return self.list_plugins(param="module")

    def __getitem__(self, key):
        return self._registry[key]

    def __len__(self):
        return len(self._registry)

    def __iter__(self):
        return iter(self._registry)


def register_plugins(group: str, registry: PluginRegistry) -> None:
    """Get the plugins from the entry points.

    The three allowed entry point formats are:

    ```Toml
    [proejct.entry_point."mrfmsim.plugin"]
    submodule_name = "plugin_module [plugin1, plugin2, ...]"
    submodule_name.plugin = "plugin_module:plugin"
    submodule_name.plugin_module = "plugin_module"
    ```
    For the entry point with the format submodule_name = "plugin_module
    [plugin1, plugin2, ...]", the endpoints are submodule_name.plugin1,
    submodule_name.plugin2, etc.

    :param group: The entry point group to search for.
    :param registry: The registry to store the plugins.
    """

    eps = entry_points(group=group)

    for ep in eps:
        # allow only three cases
        # 1. name.dst = module:dst
        # 2. name.dst = dst
        # 3. name = module [dst]

        ep_list = ep.name.split(".")
        if (
            (len(ep_list) < 2 and not ep.extras)
            or (len(ep_list) > 2)
            or (ep.extras and ep.attr)
        ):
            warnings.warn(f"skip plugin, invalid entry point '{ep.name}={ep.value}'")
            continue
        elif ep.extras:
            plugins = [
                UnloadedPlugin(f"{ep.name}.{attr}", ep.module, attr)
                for attr in ep.extras
            ]
            for p in plugins:
                registry.register(p, None)

        else:
            registry.register(UnloadedPlugin(ep.name, ep.module, ep.attr), None)

    # return registry


def create_module(module_path: str) -> ModuleType:
    """Create a module from the module path.

    If the module is already loaded, the module is returned.

    :param module_path: The module path to create or extract the module.
    """

    if module_path in sys.modules:
        return sys.modules[module_path]
    else:
        module = ModuleType(module_path)
        sys.modules[module_path] = module
        return module


def assign_plugins(
    host_module: ModuleType, plugins: Plugins, registry: PluginRegistry
) -> None:
    """Load plugins that are based on the plugin tuple.

    If a plugin name of the same submodule is duplicated,
    the plugin name is renamed by adding a suffix that is the plugin module name.

    :param host_module: The module to assign the plugins to.
    :param plugins: The plugins to assign.
    :param registry: The registry to store the plugins.
    """

    hostname = host_module.__name__

    for ep_module_name in plugins.unique("ep_module"):
        ep_module = create_module(f"{hostname}.{ep_module_name}")
        ep_module.__class__ = LazyModule

        for plugin in plugins.select(ep_module=ep_module_name):
            if plugin in registry:
                continue
            # hasattr calls the __getitem__ method, use dir instead
            if plugin.ep_attr in dir(ep_module):
                ep_attr = f"{plugin.ep_attr}_{plugin.module.split('.')[0]}"
                warnings.warn(
                    f"endpoint exists, import {plugin.plugin_path} "
                    f"as {hostname}.{ep_module_name}.{ep_attr}"
                )
            else:
                ep_attr = plugin.ep_attr
            registry.register(plugin, f"{hostname}.{ep_module_name}.{ep_attr}")
            setattr(ep_module, ep_attr, plugin)

        setattr(host_module, ep_module_name, ep_module)
