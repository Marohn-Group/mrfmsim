Plugin
======================

*mrfmsim* is designed as a platform for different groups to build
and collaborate on simulation experiments. The MRFM community
employs different experimental setups. The plugin system is designed to allow
other groups to develop their sub-packages and share them with the community.
These plugin packages can contain experiments or additional features to add
to the *mrfmsim* platform.
The plugin system also simplifies the user experience by combining all
modules under one *mrfmsim* namespace.


Metadata
---------

*mrfmsim* searches the directory for packages with 
`plugin metadata <https://packaging.python.org/en/latest/
guides/creating-and-discovering-plugins/#using-package-metadata>`_
specified as "mrfmsim-plugin". This can be achieved in the ``pyproject.toml``::

    [project.entry-points.'mrfmsim-plugin']
    test = 'mrfmsim-test'

Or in the poetry ``pyproject.toml``::

    [tool.poetry.plugins."mrfmsim-plugin"]
    "test" = "mrfmsim_test"

Different namespaces can be added to the ``mrfmsim-plugin`` group. For example,

    [project.entry-points.'mrfmsim-plugin']
    experiment = 'mrfmsim_marohn.experiment'
    modifier = 'mrfmsim_marohn.modifier'

.. note::

    For packages that upload to PYPI, set the platform to "mrfmsim" to help users
    discover the available plugins.

Naming
-------

It is recommended to use the name prefix ``mrfmsim_`` for the plugin package, with a
unique name.
For plugins that contain duplicated object names, the object name will be
prefixed with the plugin name. For example, if the plugin package name is
``mrfmsim_marohn``, a duplicated object name ``experiment`` will be renamed to
``marohn_experiment``.

Register object
----------------

Not all objects in a module need to be loaded by *mrfmsim*. To register objects,
add the objects to the list ``__mrfmsim_plugin__`` in the module.

For example, to register the ``experiment`` object in the module ``mrfmsim_marohn``::

    __mrfmsim_plugin__ = ['experiment']

:mod:`plugin` module
----------------------

.. automodule:: mrfmsim.plugin
    :members:
    :show-inheritance:
