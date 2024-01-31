from types import ModuleType
import sys
from collections import defaultdict
import warnings
from importlib.metadata import entry_points


def load_plugins(host_module, entry_point_group):
    """Load plugins into mrfmsim main package.

    The plugin is loaded at startup. The loading is done by
    searching for the entry point of installed packages. The name of
    the entry point is the attribute in mrfmsim to access the plugin.
    If the plugin with the same name is already loaded, the plugin will
    be renamed by the name of the plugin and the module name.

    ..Note::
        Currently, there is no option to block certain plugins.

    :param list mrfmsim_module: mrfmsim module
    """
    plugin_dict = defaultdict(list)
    eps = entry_points(group=entry_point_group)
    host_name = host_module.__name__

    for ep in eps:
        m = ep.load()  # load the module
        ep_dict = {
            "module": m,
            "name": ep.name,
            "plugins": getattr(m, f"__{host_name}_plugin__", []),
        }
        plugin_dict[ep.name].append(ep_dict)

    for submodule_name, module in plugin_dict.items():
        submodule = getattr(host_module, submodule_name, None)
        if submodule is None:
            path = f"{host_name}.{submodule_name}"
            submodule = ModuleType(path)
            sys.modules[path] = submodule
            setattr(host_module, submodule_name, submodule)

        for ep_dict in module:
            for plugin in ep_dict["plugins"]:
                plugin_object = getattr(ep_dict["module"], plugin)
                plugin_name = plugin

                if hasattr(submodule, plugin):
                    # use the affix of the plugin
                    name = ep_dict["name"]
                    affix = name.split("_")[1] if name.startswith(host_name) else name
                    plugin_name = f"{affix}_{plugin}"
                    warnings.warn(
                        f"Duplicated plugin name: {plugin} in {submodule_name}, "
                        f"import as {plugin_name}."
                    )
                # register the object
                setattr(submodule, plugin_name, plugin_object)

    return plugin_dict
