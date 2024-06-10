from mrfmsim.plugin import (
    register_plugins,
    assign_plugins,
    create_module,
    Plugins,
    UnloadedPlugin,
    LazyModule,
    PluginRegistry,
)
from mrfmsim import get_plugins, load_plugins
import mrfmsim
import pytest
from types import ModuleType
import sys
from importlib.metadata import EntryPoint, EntryPoints
import warnings
import dataclasses


class TestUnloadedPlugin:
    """Test the UnloadedPlugin."""

    @pytest.fixture
    def plugin(self):
        return UnloadedPlugin(endpoint="test.function", module="pm.subm", attr="func")

    def test_UnloadedPlugin(self, plugin):
        """Test the UnloadedPlugin class attributes."""

        plugin = UnloadedPlugin(endpoint="test.function", module="pm.subm", attr="func")
        assert plugin.endpoint == "test.function"
        assert plugin.module == "pm.subm"
        assert plugin.attr == "func"
        assert plugin.ep_attr == "function"
        assert plugin.ep_module == "test"

    def test_UnloadedPlugin_repr(self, plugin):
        """Test the UnloadedPlugin class repr."""

        assert (
            repr(plugin)
            == "UnloadedPlugin(endpoint='test.function', module='pm.subm', attr='func', "
            "ep_module='test', ep_attr='function', plugin_path='pm.subm.func')"
        )

    def test_UnloadedPlugin_immutable(self, plugin):
        """Test the UnloadedPlugin class is immutable."""

        with pytest.raises(AttributeError, match="cannot assign to field 'attr'"):
            plugin.attr = "test"


class TestPlugins:
    """Test the Plugins class, getting and loading plugins."""

    @pytest.fixture
    def entry_points(self):
        return EntryPoints(
            [
                EntryPoint(name="test1.func1", value="pm1.subm:func1", group="group"),
                EntryPoint(name="test2.pm2", value="pm2", group="group"),
                EntryPoint(name="test2", value="pm3 [func1, func2]", group="group"),
                EntryPoint(name="test3.pm3", value="pm3", group="group"),
            ]
        )

    @pytest.fixture
    def plugins_instance(self):
        """Create a plugin instance."""
        return Plugins(
            [
                UnloadedPlugin(endpoint="test1.func1", module="pm1.subm", attr="func1"),
                UnloadedPlugin(endpoint="test2.pm2", module="pm2", attr=None),
            ]
        )

    @pytest.fixture
    def plugin_dup(self):
        """Create a plugin with duplicated dst name."""
        return Plugins(
            [UnloadedPlugin(endpoint="test1.func1", module="pm2.subm", attr="func1")]
        )

    @pytest.fixture
    def plugin_comb(self, plugins_instance, plugin_dup):
        return Plugins(list(plugins_instance) + list(plugin_dup))

    @pytest.fixture
    def modules(self):
        """Create a preset module dictionary."""

        pm1 = ModuleType("pm1")
        pm1.subm = ModuleType("pm1.subm")
        pm1.subm.func1 = lambda x: x

        pm2 = ModuleType("pm2")
        pm2.subm = ModuleType("pm2.subm")
        pm2.subm.func1 = lambda x: x**2
        pm2.func2 = lambda x: x**3

        host_module = ModuleType("host")

        return {
            "pm1": pm1,
            "pm1.subm": pm1.subm,
            "pm2": pm2,
            "pm2.subm": pm2.subm,
            "warnings": warnings,
            "host": host_module,
        }

    def test_Plugins_formation(self, plugin_comb):
        """Test the Plugins class formation."""

        # entry points are expanded
        assert len(plugin_comb) == 3
        assert plugin_comb[0] == UnloadedPlugin(
            endpoint="test1.func1", module="pm1.subm", attr="func1"
        )

    def test_Plugins_select(self, plugin_comb):
        """Test the select method of the Plugins class."""
        assert plugin_comb.select(endpoint="test1.func1") == Plugins(
            [plugin_comb[0], plugin_comb[2]]
        )

        assert plugin_comb.select(attr="func1") == Plugins(
            [plugin_comb[0], plugin_comb[2]]
        )

        assert plugin_comb.select(ep_attr="func1") == Plugins(
            [plugin_comb[0], plugin_comb[2]]
        )

    def test_Plugins_unique(self, plugin_comb):
        """Test the unique method of the Plugins class."""

        ep_modules = sorted(list(plugin_comb.unique("ep_module")))
        assert ep_modules == ["test1", "test2"]

        modules = sorted(list(plugin_comb.unique("module")))
        assert modules == ["pm1.subm", "pm2", "pm2.subm"]

    def test_get_plugins(self, mocker, entry_points):
        """Test the get_plugin function.

        The test that the entry_points function returns a
        EntryPoints object.
        """

        def new_entry_points(group):
            return entry_points

        mocker.patch(f"mrfmsim.plugin.entry_points", new=new_entry_points)
        registry = PluginRegistry()
        # in get_plugins, duplicated names are not checked
        register_plugins("group", registry)
        assert isinstance(registry, PluginRegistry)

        plugins = registry.to_plugins()
        assert len(plugins) == 5

        # check the first entry point
        plugin = plugins[0]
        assert plugin.endpoint == "test1.func1"
        assert plugin.attr == "func1"
        assert plugin.module == "pm1.subm"
        assert plugin.ep_attr == "func1"
        assert plugin.ep_module == "test1"
        assert plugin.plugin_path == "pm1.subm.func1"

        # check the second entry point
        plugin = plugins[1]
        assert plugin.endpoint == "test2.pm2"

        plugin = plugins[2]
        assert plugin.endpoint == "test2.func1"

        plugin = plugins[3]
        assert plugin.endpoint == "test2.func2"

        plugin = plugins[4]
        assert plugin.endpoint == "test3.pm3"
        assert plugin.plugin_path == "pm3"

    def test_get_plugin_incorrect_name(self, mocker):
        """Test the get_plugin function with incorrect name."""

        eps = EntryPoints([EntryPoint(name="test1", value="pm1", group="group")])

        def new_entry_points(group):
            return eps

        mocker.patch(f"mrfmsim.plugin.entry_points", new=new_entry_points)

        with pytest.warns(
            UserWarning,
            match="skip plugin, invalid entry point 'test1=pm1'",
        ):
            registry = PluginRegistry()
            register_plugins(group="group", registry=registry)

        assert len(registry) == 0

    def test_assign_plugins(self, mocker, plugins_instance, modules):
        """Test the assign_plugins function."""
        mocker.patch("sys.modules", modules)
        registry = PluginRegistry()

        host_module, pm1, pm2 = modules["host"], modules["pm1"], modules["pm2"]

        assign_plugins(host_module, plugins_instance, registry)

        # test the loaded functions
        assert host_module.test1.func1 == pm1.subm.func1
        assert host_module.test1.func1(1) == 1
        assert host_module.test2.pm2 == pm2
        assert host_module.test2.pm2.func2(3) == 27
        assert registry[plugins_instance[0]] == "host.test1.func1"

    def test_duplicated_name(self, mocker, plugin_comb, modules):
        """Test the duplicated named plugin warning."""

        mocker.patch("sys.modules", modules)
        registry = PluginRegistry()

        host_module, pm2 = modules["host"], modules["pm2"]
        with pytest.warns(
            UserWarning,
            match="endpoint exists, import pm2.subm.func1 as host.test1.func1_pm2",
        ):
            assign_plugins(host_module, plugin_comb, registry)

        assert host_module.test1.func1_pm2 == pm2.subm.func1
        assert host_module.test1.func1_pm2(2) == 4

    def test_duplicated_plugin(self, mocker, modules, plugins_instance):
        """Test the that if the same plugin is added, the loading skips it."""

        mocker.patch("sys.modules", modules)
        registry = PluginRegistry()

        host_module = modules["host"]
        assign_plugins(host_module, plugins_instance, registry)
        assert registry[plugins_instance[0]] == "host.test1.func1"

        assign_plugins(host_module, plugins_instance, registry)
        # make sure the name does not change
        assert registry[plugins_instance[0]] == "host.test1.func1"
        assert not hasattr(host_module, "test1.func1_pm2")


def test_LazyModule(mocker):
    """Test the LazyModule class."""

    pm = ModuleType("pm")
    pm.subm = ModuleType("pm.subm")
    pm.subm.func = lambda x: x

    mocker.patch("sys.modules", {"pm": pm, "pm.subm": pm.subm})

    plugin = UnloadedPlugin(endpoint="test.func", module="pm.subm", attr="func")

    host_module = ModuleType("host")
    sys.modules["host"] = host_module
    host_module.plugin = plugin
    host_module.__class__ = LazyModule
    # unloaded
    assert host_module.__dict__["plugin"] == plugin
    # loaded
    assert host_module.plugin == pm.subm.func
    assert host_module.plugin(1) == 1
    assert host_module.__dict__["plugin"] == pm.subm.func


class TestRegistry:
    """Test the PluginRegistry class."""

    def test_PluginRegistry(self):
        """Test the register method of the PluginRegistry class."""

        registry = PluginRegistry()
        plugin = UnloadedPlugin(endpoint="test.func", module="pm.subm", attr="func")
        registry.register(plugin, "func1")

        with pytest.raises(
            TypeError, match="'PluginRegistry' object does not support item assignment"
        ):
            registry[plugin] = "func"

        assert registry[plugin] == "func1"
        assert len(registry) == 1
        assert list(registry.keys()) == [plugin]

    def test_list_plugins(self):
        """Test the list_plugins function."""

        registry = PluginRegistry()
        plugin1 = UnloadedPlugin(
            endpoint="test1.func1", module="pm1.subm", attr="func1"
        )
        registry.register(plugin1, f"host.{plugin1.endpoint}")
        plugin2 = UnloadedPlugin(endpoint="test2.func2", module="pm2.subm", attr=None)
        registry.register(plugin2, None)
        std_out = registry.list_plugins(param="ep_module")

        assert (
            std_out == f"test1:\n\tpm1.subm.func1 -> host.test1.func1\n"
            f"test2:\n\tpm2.subm"
        )

        std_out = registry.list_plugins(param="module")
        assert (
            std_out == f"pm1.subm:\n\tpm1.subm.func1 -> host.test1.func1\n"
            f"pm2.subm:\n\tpm2.subm"
        )

        assert repr(registry) == std_out


def test_create_module(mocker):
    """Test the create_module function."""

    mocker.patch("sys.modules", {})

    module = create_module("host.ep_module")
    assert isinstance(module, ModuleType)
    assert module.__name__ == "host.ep_module"
    assert "host.ep_module" in sys.modules

    mocker.patch("sys.modules", {"host.ep_module": module})
    module_created = create_module("host.ep_module")
    assert module_created is module  # the module is already loaded


class TestInitProcedure:
    """Test the plugin loading procedure in __init__.py."""

    @pytest.fixture
    def entry_points(self):
        return EntryPoints(
            [
                EntryPoint(name="test1.func1", value="pm1.subm:func1", group="group"),
                EntryPoint(name="test2.pm2", value="pm2", group="group"),
            ]
        )

    def test_get_plugins(self, mocker, entry_points):
        """Test the get_plugins function."""

        mocker.patch("mrfmsim.PLUGINS", PluginRegistry())
        mocker.patch("mrfmsim.plugin.entry_points", new=lambda group: entry_points)

        get_plugins()
        available_plugins = list(mrfmsim.PLUGINS.keys())
        assert available_plugins == [
            UnloadedPlugin(endpoint="test1.func1", module="pm1.subm", attr="func1"),
            UnloadedPlugin(endpoint="test2.pm2", module="pm2", attr=None),
        ]

    def test_load_plugins(self, mocker, entry_points):
        """Test the load_plugins function, with no keyword input.

        When calling the function without the keyword input, all
        available plugins are loaded.
        """

        mocker.patch("mrfmsim.PLUGINS", PluginRegistry())
        mocker.patch("mrfmsim.LOADED_PLUGINS", PluginRegistry())
        mocker.patch("mrfmsim.plugin.entry_points", new=lambda group: entry_points)
        # patch an empty module
        mock_module = ModuleType("mrfmsim")
        mocker.patch("sys.modules", {"mrfmsim": mock_module})

        load_plugins()
        available_plugins = list(mrfmsim.PLUGINS.keys())
        loaded_plugins = list(mrfmsim.LOADED_PLUGINS.keys())
        assert available_plugins == loaded_plugins
        assert loaded_plugins == [
            UnloadedPlugin(endpoint="test1.func1", module="pm1.subm", attr="func1"),
            UnloadedPlugin(endpoint="test2.pm2", module="pm2", attr=None),
        ]

    def test_load_plugins_select(self, mocker, entry_points):
        """Test the load_plugins function, with selection.

        When calling the function without the keyword input, all
        available plugins are loaded.
        """

        mocker.patch("mrfmsim.PLUGINS", PluginRegistry())
        mocker.patch("mrfmsim.LOADED_PLUGINS", PluginRegistry())
        mocker.patch("mrfmsim.plugin.entry_points", new=lambda group: entry_points)
        # patch an empty module
        mock_module = ModuleType("mrfmsim")
        mocker.patch("sys.modules", {"mrfmsim": mock_module})

        load_plugins(module="pm2")
        available_plugins = list(mrfmsim.PLUGINS.keys())
        loaded_plugins = list(mrfmsim.LOADED_PLUGINS.keys())
        assert available_plugins == [
            UnloadedPlugin(endpoint="test1.func1", module="pm1.subm", attr="func1"),
            UnloadedPlugin(endpoint="test2.pm2", module="pm2", attr=None),
        ]
        # only pm2 module is loaded
        assert loaded_plugins == [
            UnloadedPlugin(endpoint="test2.pm2", module="pm2", attr=None)
        ]
