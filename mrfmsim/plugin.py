"""The scripts handler loading plugin information into mrfmsim main package.


Mrfmsim plugin modules should have the starting string 'mrfmsim_'.
The architecture is only a pesudo plugin because the subsequent packages
depends on the main mrfmsim package. Therefore the plugin cannot be loaded
during mrfmsim import. The load_plugin function needs to be called.

"""


import importlib
import pkgutil
from types import ModuleType
import sys
from collections import defaultdict


PLUGINS = defaultdict(list)


def iter_namespace(ns_pkg):
    """Iterate through all modules in a namespace package.

    Specifying the second argument (prefix) to iter_modules makes the
    returned name an absolute name instead of a relative one. This allows
    import_module to work without having to do additional modifications to
    the name.

    The function is based on Python packaging user guide:
    https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/
    """
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def create_modules(module_name, attr_list):
    """Create submodules in the main package named base_name."""

    main_submodule_dict = {}
    for attr in attr_list:
        module_name = f"{module_name}.{attr}"
        m = ModuleType(module_name)
        main_submodule_dict[attr] = m
        sys.modules[module_name] = m

    return main_submodule_dict


def import_plugin(plugin: ModuleType, main_submodule_dict):
    """Load plugins into mrfmsim main package.

    The function creates and loads three submodules:
    - experiments
    - shortcuts
    - modifiers

    The submodules should be named as the plugin module name.
    The "__all__" attribute should be defined for the imported modules
    to be loaded into the submodules.

    If __all__ is not defined, the submodules will not be loaded.

    TODO:
        Load the submodules without __all__ defined.
        This can be achieved by inspecting the members of the module.
        getmembers(module, isfunction) will return a list of functions
        in the module. and
        getmembers(module, isclass) will return a list of classes
        in the module.
    """

    for _, plugin_submodule_name, _ in iter_namespace(plugin):

        # Get the submodule name base (after the ".").
        plugin_attr_name = plugin_submodule_name.split(".")[-1]

        if plugin_attr_name in main_submodule_dict:
            plugin_submodule = importlib.import_module(plugin_submodule_name)

            members = getattr(plugin_submodule, "__all__", [])

            for member in members:

                PLUGINS[plugin_attr_name].append(f"{member} ({plugin.__name__})")
                setattr(
                    main_submodule_dict[plugin_attr_name],
                    member,
                    getattr(plugin_submodule, member),
                )


def load_plugin(
    module_name="mrfmsim",
    plugin_name_list: list = None,
    attr_list: list = ["experiments", "shortcuts", "modifiers"],
):
    """Load plugins into mrfmsim main package.

    :param list module_list: list of plugin module names.
        If None, all modules starting with "mrfmsim_" will be loaded.
    """
    PLUGINS.clear()  # reset the dictionary from the global variable
    module_dict = create_modules(module_name, attr_list)

    plugin_name_list = plugin_name_list or [
        name
        for _, name, ispkg in pkgutil.iter_modules()
        if name.startswith(f"{module_name}_") and ispkg
    ]

    for name in plugin_name_list:
        plugin = importlib.import_module(name)
        import_plugin(plugin, module_dict)


def list_plugins(attr_name):
    """List all plugins loaded into mrfmsim main package."""

    print(f"List of {attr_name} loaded:")
    print("\n".join(PLUGINS[attr_name]))
