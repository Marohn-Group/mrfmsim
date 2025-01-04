Grid
====

Create grid objects based on the length of the grid, step size, and origin.
The grid point is at the center of each voxel.

Example Usage
-------------

To create a grid object:

.. code-block:: python

    grid = Grid(grid_shape=[21, 11, 101], grid_step=[20.0, 4.0, 20.0], grid_origin=[0.0, 0.0, 0.0])

The resulting grid is rectangular with the shape of (21, 11, 101), the distance between
two edge grid points in each direction are (200, 40, 2000) nm, and the full grid size
is (220 :math:`\times` 44 :math:`\times` 2020) nm. 
The returned grid points are numpy "ogrid" points: 
`np.ogrid <https://numpy.org/devdocs/reference/generated/numpy.ogrid.html>`__.

To print out a summary of the grid properties:

.. code-block:: python

    >>> print(grid)
    Grid
      grid_shape = (21, 11, 101)
      grid_step = [20.0, 4.0, 20.0] nm
      grid_origin = [0.0, 0.0, 0.0] nm
      grid_voxel = 1600.000 nm^3
      grid_range = [400.0, 40.0, 2000.0] nm
      grid_length = [420.0, 44.0, 2020.0] nm

:mod:`grid` module
------------------

.. automodule:: mrfmsim.component.grid
    :members:
    :undoc-members:
    :show-inheritance:
