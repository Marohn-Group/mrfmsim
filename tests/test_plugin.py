from mrfmsim.plugin import load_plugins
import pytest
from types import ModuleType
import sys
from textwrap import dedent
from importlib.metadata import (
    DistributionFinder,
    PathDistribution,
    EntryPoint,
    entry_points,
)
from pathlib import PosixPath


class TestImport:
    """Test plugin imports.

    In this test we create two modules, one is the host module with
    some functions predefined. Another is the plugin module with the
    correct entry_point and additional functions defined.

    The goal is to test whether the core module can load the plugin
    correctly. In the ``pkg_resources`` module we can add additional
    metadata to the system. However, the package is deprecated in favor of
    importlib.metadata. The new module does not seem to have a to
    directly link custom module to the entry points.
    Here the workaround is to recreate a custom DistributionFinder and
    a custom PathDistribution class.
    """

    def Finder(self, distributions):
        """Custom define finder."""

        class MockDistributionFinder(DistributionFinder):
            """DistributionFinder that returns target distributions."""

            @classmethod
            def find_distributions(cls, context=None):
                return distributions

        return MockDistributionFinder

    def Distribution(self, metadata, entry_points):
        """metadata is a dictionary that contains version and name.

        The above information is limited to working for entry points,
        it is unclear if other functionalities work here.
        """

        class MockPathDistribution(PathDistribution):
            """PathDistribution that returns target distributions."""

            @property
            def metadata(self):
                return metadata

            @property
            def entry_points(self):
                return entry_points

        return MockPathDistribution

    @pytest.fixture(autouse=True)
    def mock_module(self):
        """Mock a host and a plugin module.

        The host module contain one submodule - "test".
        The submodule has one function - "test_func1".
        The host module has name "host".

        The plugin module contain one submodules - "test".
        The submodule "test" has two functions - "test_func1", "test_func2".
        The plugin module has name "host_test".
        """

        # host module
        host_module = ModuleType("host")
        host_submodule = ModuleType("host.test")
        setattr(host_module, "test", host_submodule)
        host_submodule.test_func1 = lambda: "host_func1"
        # main_module.__path__ = [""]
        sys.modules["host"] = host_module
        sys.modules["host.test1"] = host_submodule

        # plugin module
        plugin_module = ModuleType("host_test")
        plugin_submodule = ModuleType("host_test.test")
        setattr(plugin_module, "test", plugin_submodule)
        plugin_submodule.__host_plugin__ = ["test_func1", "test_func2"]
        plugin_submodule.test_func1 = lambda: "plugin_func1"
        plugin_submodule.test_func2 = lambda: "plugin_func2"

        sys.modules["host_test"] = plugin_module
        sys.modules["host_test.test"] = plugin_submodule

        return host_module

    def register_entry_point(self, plugin_name, entry_name):
        # register to finder
        metadata = {"Name": "host_test", "Version": "0.0.1"}
        entry_points = [EntryPoint(plugin_name, "host_test.test", entry_name)]
        dist = self.Distribution(metadata, entry_points)(PosixPath("host_test"))
        finder = self.Finder([dist])
        sys.meta_path.append(finder)

        return finder

    def test_plugin_registered(self, mock_module):
        """Test plugin is correctly added to the host module."""

        # register to finder
        finder = self.register_entry_point("test_plugin", "host_plugin")
        load_plugins(mock_module, "host_plugin")
        assert mock_module.test_plugin.test_func1() == "plugin_func1"
        assert mock_module.test_plugin.test_func2() == "plugin_func2"

        # remove the finder
        sys.meta_path.remove(finder)

    def test_plugin_duplicate(self, mock_module):
        """Test when the plugin already exist in the system."""

        # register to finder
        finder = self.register_entry_point("test", "host_plugin")
        
        with pytest.warns(
            UserWarning,
            match=(
                "Duplicated plugin name: test_func1 in test, "
                "import as test_test_func1."
            ),
        ):
            load_plugins(mock_module, "host_plugin")

        assert mock_module.test.test_func1() == "host_func1"
        # duplication behavior
        assert mock_module.test.test_test_func1() == "plugin_func1"
        assert mock_module.test.test_func2() == "plugin_func2"

        # remove the finder
        sys.meta_path.remove(finder)

    def test_plugin_dict(self, mock_module, capsys):
        """Test the plugin dictionary is correctly created."""

        # register to finder
        finder = self.register_entry_point("test_plugin", "host_plugin")

        plugin_dict = load_plugins(mock_module, "host_plugin")
        assert "test_plugin" in plugin_dict.keys()

        # remove the finder
        sys.meta_path.remove(finder)


    def test_plugin_not_registered(self, mock_module):
        """Test plugin is not registered."""

        # register to finder
        finder = self.register_entry_point("test", "client_plugin")

        load_plugins(mock_module, "host_plugin")
        assert not hasattr(mock_module.test, "test_func2")

        # remove the finder
        sys.meta_path.remove(finder)
