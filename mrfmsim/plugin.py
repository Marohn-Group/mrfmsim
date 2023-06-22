import importlib
import pkgutil
from types import ModuleType
import sys
from collections import defaultdict
import warnings


PLUGINS = defaultdict(list)
SUBMODULES = ["experiment", "shortcut", "modifier", "component"]
MODULE_NAME = "mrfmsim"
DEFUALT_MODULES = ("mmodel",)


def iter_namespace(ns_pkg):
    """Iterate through all modules in a namespace package.

    Specifying the second argument (prefix) to iter_modules makes the
    returned name an absolute name instead of a relative one. This allows
    import_module to work without having to do additional modifications to
    the name.

    The function is based on the Python packaging user guide:
    https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/
    """
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def create_modules(module_name, submodule_name_list):
    """Create submodules in the main package named base_name.

    The function will import all submodules first to avoid circular import.
    issue created by the plugins. If the submodule does not exist, a
    ModuleType object is created.
    """
    module = importlib.import_module(module_name)
    full_submodule_name_list = [
        module_name.split(".", maxsplit=1)[-1]
        for _, module_name, _ in iter_namespace(module)
    ]

    combined_list = set(full_submodule_name_list + list(submodule_name_list))

    main_submodule_dict = {}
    for submodule in combined_list:
        fullname = f"{module_name}.{submodule}"

        if submodule in full_submodule_name_list:
            m = importlib.import_module(fullname)
        else:
            m = ModuleType(fullname)
        # do not reset sys module cache
        # this step is necessary to allow testing to run smoothly
        if fullname not in sys.modules:
            sys.modules[fullname] = m
        main_submodule_dict[submodule] = m

    return main_submodule_dict


def import_plugin(module_name, plugin: ModuleType, main_submodule_dict):
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

                if f"{member} ({plugin.__name__})" in PLUGINS[plugin_attr_name]:
                    # remove the module name and append to beginning of the name
                    prefix = plugin.__name__.replace(f"{module_name}_", "")
                    member_new = f"{prefix}_{member}"
                    warnings.warn(
                        f"Duplicated plugin name: {member} in {plugin_attr_name}, "
                        f"import as {member_new}."
                    )

                    PLUGINS[plugin_attr_name].append(
                        f"{member_new} ({plugin.__name__})"
                    )

                else:
                    PLUGINS[plugin_attr_name].append(f"{member} ({plugin.__name__})")
                    member_new = member
                setattr(
                    main_submodule_dict[plugin_attr_name],
                    member,
                    getattr(plugin_submodule, member),
                )


def load_plugin(plugin_name_list: list = None, submodule_name_list: list = None):
    """Load plugins into mrfmsim main package.

    :param list module_list: list of plugin module names.
        If None, all modules starting with "mrfmsim_" will be loaded.
    """
    PLUGINS.clear()  # reset the dictionary from the global variable

    submodule_name_list = submodule_name_list or SUBMODULES
    module_dict = create_modules(MODULE_NAME, submodule_name_list)

    plugin_name_list = plugin_name_list or [
        name
        for _, name, ispkg in pkgutil.iter_modules()
        if name in DEFUALT_MODULES or name.startswith(f"{MODULE_NAME}_") and ispkg
    ]

    for name in plugin_name_list:
        plugin = importlib.import_module(name)
        import_plugin(MODULE_NAME, plugin, module_dict)

    print(f"Loaded plugins from: {', '.join(plugin_name_list)}".rstrip())


def list_plugins(attr_name):
    """List all plugins loaded into mrfmsim main package."""

    print(f"List of {attr_name} loaded:")
    print("\n".join(PLUGINS[attr_name]))
