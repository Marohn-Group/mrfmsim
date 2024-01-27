Plugin
======================

``mrfmsim`` is designed as a platform for different groups to build
and collaborate on different simulation experiments. The MRFM community
employs different experimental setups. The plugin system is designed to allow
different groups to build their sub-packages and share them with the community.
The plugin system also simplifies the user experience, by combining all
modules under one ``mrfmsim`` namespace. Once the packages are loaded, the user
can access all the components by import under ``mrfmsim``.

Load Plugin
----------------------

To automatically load plugins run:

.. code:: python

    import mrfmsim
    mrfmsim.load_plugin()

If no plugin is specified, the ``mmodel`` package and all 
packages with the name prefix of ``mrfmsim_`` will be loaded.
The default submodule attributes are "experiment", "modifier", "shortcut", and "component".

To specify the plugin directory and submodule attribute::

    import mrfmsim
    mrfmsim.load_plugin(
        plugin_name_list=['mmodel', 'mrfmsim_marohn'], submodule_name_list=['experiment', 'component']
    )

Create Plugin Package
----------------------

The package name must start with ``mrfmsim_``to create a plugin package. The submodule names should use the same convention "experiment", "modifier", "shortcut", and "component".

The way ``mrfmsim`` loads the variables (functions, classes, etc) is by tracking the ``__all__`` attribute of each submodule. The ``__all__`` attribute is a list of strings that are commonly used to define what symbols in a module will be exported when ``from <module> import *`` is used on the module.

:mod:`plugin` module
----------------------

.. automodule:: mrfmsim.plugin
    :members:
    :show-inheritance:
