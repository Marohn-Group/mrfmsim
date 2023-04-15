from mrfmsim.plugin import load_plugin, import_plugin, create_modules, list_plugins
import mrfmsim.plugin
import pytest
from types import ModuleType
import importlib
import sys
from textwrap import dedent
import pkgutil


def test_create_module():
    """Test create_module.

    Test the module can be created and imported and the module object attribute
    also changes the module object in the sys.modules dictionary.
    """

    module_dict = create_modules("mock_module", ["module_name"])

    module = importlib.import_module(f"mock_module.module_name")
    module_dict["module_name"].test = True
    assert isinstance(module, ModuleType)
    assert module.test


class TestImport:
    """Test plugin imports.

    Create a mock plugin module and add testing and utils submodules.
    One of the submodules has the __all__ attribute defined.
    The other does not.
    """

    @pytest.fixture
    def mock_import_module(self):
        """Mock import_module."""

        plugin = ModuleType("mock_module_plugin")
        plugin.__path__ = [""]

        plugin_submodule1 = ModuleType("mock_module_plugin.testing")
        plugin_submodule2 = ModuleType("mock_module_plugin.utils")

        plugin_submodule1.__all__ = ["testing_func"]
        plugin_submodule1.testing_func = lambda: True

        plugin_submodule2.__all__ = []
        plugin_submodule2.testing_func = lambda: True

        main_submodule1 = ModuleType("mock_module.testing")
        main_submodule2 = ModuleType("mock_module.utils")

        sys.modules["mock_module_plugin"] = plugin
        sys.modules["mock_module_plugin.testing"] = plugin_submodule1
        sys.modules["mock_module_plugin.utils"] = plugin_submodule2
        sys.modules["mock_module.testing"] = main_submodule1
        sys.modules["mock_module.utils"] = main_submodule2

        return plugin, {"testing": main_submodule1, "utils": main_submodule2}

    @pytest.fixture(autouse=True)
    def mock_pkgutils(self, monkeypatch):
        """Mock pkgutil.

        If path is None, return the plugin module. (For load_plugin testing.)
        If path is not None, return the submodules. (For import_plugin testing.)
        """

        def mockreturn(path=None, prefix=""):
            if prefix == "mmodel":  # skip mmodel submodules for testing
                pass
            if path is None:
                yield (None, "mock_module_plugin", True)
            for attr in ["testing", "utils"]:
                yield (None, f"{prefix}{attr}", False)

        monkeypatch.setattr(pkgutil, "iter_modules", mockreturn)
        monkeypatch.setattr(mrfmsim.plugin, "MODULE_NAME", "mock_module")
        monkeypatch.setattr(mrfmsim.plugin, "DEFUALT_MODULES", ())

    def test_import_plugin(self, mock_import_module):
        """Test import_plugin.

        Test that the plugin module can be imported and the submodules can be loaded.
        Test the attributes of the main module.
        """

        plugin, module_dict = mock_import_module

        import_plugin("module_name", plugin, module_dict)

        test = importlib.import_module("mock_module.testing")
        assert hasattr(test, "testing_func")

        utils = importlib.import_module("mock_module.utils")
        assert not hasattr(utils, "testing_func")

    def test_load_plugin(self, capsys):
        """Test load_plugin."""

        load_plugin(attr_list=["testing", "utils"])

        test = importlib.import_module("mock_module.testing")
        utils = importlib.import_module("mock_module.utils")
        assert hasattr(test, "testing_func")
        assert not hasattr(utils, "testing_func")

        captured = capsys.readouterr()
        output = "Loaded plugins from: mock_module_plugin\n"
        assert output == captured.out

    def test_load_plugin_manual(self):
        """Test load_plugin manual plugin inputs."""
        load_plugin(
            plugin_name_list=["mock_module_plugin"],
            attr_list=["testing", "utils"],
        )

        test = importlib.import_module("mock_module.testing")
        utils = importlib.import_module("mock_module.utils")
        assert hasattr(test, "testing_func")
        assert not hasattr(utils, "testing_func")

    def test_list_plugin(self, capsys):
        """Test list_plugin."""

        load_plugin(
            plugin_name_list=["mock_module_plugin"],
            attr_list=["testing", "utils"],
        )

        list_plugins("testing")
        captured = capsys.readouterr()

        output = dedent(
            """\
        List of testing loaded:
        testing_func (mock_module_plugin)
        """
        )

        assert output in captured.out

    def test_object_collision(self, capsys):
        """Test object name collision when loading plugins."""

        with pytest.warns(
            UserWarning,
            match=(
                "Duplicated plugin name: testing_func in testing"
                ", import as plugin_testing_func."
            ),
        ):
            load_plugin(
                plugin_name_list=["mock_module_plugin", "mock_module_plugin"],
                attr_list=["testing"],
            )
            list_plugins("testing")
            captured = capsys.readouterr()

            output = dedent(
                """\
            List of testing loaded:
            testing_func (mock_module_plugin)
            plugin_testing_func (mock_module_plugin)
            """
            )
            assert output in captured.out
