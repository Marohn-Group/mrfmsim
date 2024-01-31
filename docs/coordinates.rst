Coordinates
===========

*mrfmsim* is flexible in setting up the coordinates for the simulation.
Currently, the components that involve coordinates are the grid and the magnet.

.. image:: _static/mrfmsim_coordinates.pdf
    :width: 800px
    :align: center

As shown in the figure above, the setup is determined by the origin of the magnet
(``magnet.origin``), the origin of the grid (``grid.origin``), and the tip-sample
separation (``h``). Although only the relative position of the magnet and the grid is
important, the convention is to set the face of the grid and the magnet flush with a
origin plane --- the :math:`xy` plane for the left figure and the :math:`xz` plane for
the right figure. 

For example, with the left figure setup,

.. code-block:: python

    from mrfmsim.component import Grid, SphereMagnet

    grid = Grid(shape=[11, 11, 11], step=[20.0, 20.0, 20.0], origin=[0.0, 0.0, -110])
    magnet = SphereMagnet(radius=50.0, mu0_Ms=1800.0, origin=[0.0, 0.0, 50.0])

The grid has a height of 220 nm in :math:`z`-direction, and the magnet has a radius of 50 nm.
The grid origin is set to be 110 nm below the :math:`xy`-plane, and the magnet origin is set 
to be 50 nm above the :math:`xy`-plane. The magnet and the grid are flush, and the
tip-sample separation is 0 nm.

With the right figure setup,

.. code-block:: python

    from mrfmsim.component import Grid, RectangularMagnet

    grid = Grid(shape=[11, 11, 11], step=[20.0, 20.0, 20.0], origin=[0.0, -110, 0.0])
    magnet = RectangularMagnet([70, 70, 1500], mu0_Ms=1800.0, origin=[0.0, 750.0, 0.0])

The grid has a width of 220 nm in :math:`y`-direction, and the magnet has a height of
1500 nm. The grid origin is set to be 110 nm below left of the :math:`xz`-plane,
and the magnet origin is set to be 750 nm right to the :math:`xz`-plane. The magnet and the 
grid are flush, and the tip-sample separation is 0 nm.

.. note::

    The magnet calculation assumes the magnet is magnetized in the :math:`z`-direction,
    and the external field is applied in the :math:`z`-direction.
