Grid
====

Summary
-------

Create grid objects based on the length of the grid, step size, and origin.
The supported Grid types are

Example Usage
^^^^^^^^^^^^^

Create the grid object given the values::

    grid = Grid(shape=[21, 11, 101], step=[20.0, 4.0, 20.0], origin=[0.0, 0.0, 0.0])

The resulting grid is rectangular with shape of (21, 11, 101), the distance between
two corner points in each direction is (200, 40, 2000) nm, and the effective grid size
is 220 x 44 x 2020 :math: `\nm^3`. The returned grid points are numpy "ogrid" points: 
`np.ogrid <https://numpy.org/devdocs/reference/generated/numpy.ogrid.html>`__.

Print out a summary of the RectGrid properties ::

    print(grid)

:mod:`grid` module
------------------

.. automodule:: mrfmsim.component.grid
    :members:
    :undoc-members:
    :show-inheritance:
