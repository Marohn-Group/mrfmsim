Plugins
=================

Ancillary features are added to the mrfmsim ecosystem through plugin packages.
The separation of the core functionality and the plugins allows for an easy mantainance
of the mrfmsim package. The core functionalities do not depend on the plugins.

Command line interface plugin
------------------------------

The command line interface is provided by the `mrfmsim-cli
<https://github.com/Marohn-Group/mrfmsim-cli>`__ plugin. See readme of the
mrfmsim-cli project for more examples.

To view the CLI options::

    mrfmsim --help

To show the experiment metadata::

    mrfmsim metadata --expt name_of_exp

To draw the experiment graph::

    mrfmsim visualize --expt name_of_exp

Unit Plugin
----------------------

`mrfmsim-unit <https://github.com/Marohn-Group/mrfmsim-unit>`_ 
plugin is a package that handles units and unit conversions for
the *mrfmsim* base unit system. The plugin is installed by default.

The plugin is based on the `pint
<https://pint.readthedocs.io/en/stable/>`_ package, and provides
a registry with *mrfmsim* base units pre-defined. The quantity also
has quick conversion method ``to_base_units()`` to convert to the
base units.

.. code:: python

    from mrfmsim_unit.unit import MRFMUnitRegistry

    mureg = MRFMUnitRegistry()
    a = 0.1 * mureg.micrometer
    b = 1.0 * mureg.nanometer

    >>> a * b
    0.1 nm µm

    >>> (a * b).to_base_units()
    100.0 nm^2

    >>> # (a * b).to_base_units().magnitude
    >>> # (a * b).base_magnitude
    >>> (a * b).bm
    100.0

The *mrfmsim* components do not accept ``pint.Quantity``. Only the magnitude
should be supplied to the components. The plugin provides a ``getattr`` method
to access the quantity with units.

.. code:: python

    magnet = SphereMagnet(radius=50.0, mu0_Ms=1800.0, origin=[0.0, 0.0, 50.0])
    r = mureg.getattr(magnet, "radius")
    
    >>> r
    50.0 nm
    >>> r ** 2
    2500.0 nm^2

Three-dimensional plot plugin
------------------------------

To facilitate the visualization of three-dimensional experiment results, for example,
the magnetic field, polarization, and signal distribution, we created the
`mrfmsim-plot <https://github.com/Marohn-Group/mrfmsim-plot>`_ plugin that provides
conversion from the experiment data to the 
`mayavi mlab <http://docs.enthought.com/mayavi/mayavi/mlab.html>`_ and 
`PyVista <https://docs.pyvista.org/version/stable/>`_ data objects.
