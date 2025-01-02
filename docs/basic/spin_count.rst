Sample spin distribution
=============================

In the *mrfmsim* package, we can simulate the response of a single spin or an ensemble of spins to an external magnetic field. Use the "spin_density" parameter in the ``Sample`` object to adjust the target spins for a given grid. See `mrfmsim.Sample <https://marohn-group.github.io/mrfmsim-docs/sample.html>`_ for more details.

Uniformly distributed sample
----------------------------

For a uniformly distributed spin sample, input the per :math:`\mu m^3` value for "spin_density".

.. code-block:: python

    from mrfmsim.component import Sample
    sample = Sample(
        spin='e',
        temperature=4.2,
        T1=1e-3,
        T2=250e-9,
        spin_density=2.41e-2)

Non-uniformly distributed sample
--------------------------------

For a non-uniformly distributed spin sample, input the spin distribution array for "spin_density". The array should have the same shape as the grid. For example, for a (10, 10, 10) shaped grid and an array of (4 :math:`\times` 4 :math:`\times` 4) single spins in the center, the input should be:

.. code-block:: python

    from mrfmsim.component import Sample

    # for a (10, 10, 10) shaped grid
    import numpy as np
    spin_density = np.zeros([10, 10, 10])
    spin_density[3:7, 3:7, 3:7] = 1
    sample = Sample(
        spin='e',
        temperature=4.2,
        T1=1e-3,
        T2=250e-9,
        spin_density=spin_density)

.. Note::

    The ``Grid`` object does not handle spin locations that are not on the 
    grid points. The *mrfmsim* system is capable of handling a non-uniform
    grid system. A custom ``Grid`` class can be implemented to handle this. 
    (The feature is currently unimplemented, but it is on the roadmap.)
    For a small number of spins, we can manually input the spin locations,
    shape, and origin to the experiment object by removing the 
    "component_replacement" in the ``Experiment`` object.

Single spin directly under a spherical magnet
---------------------------------------------

For a single spin directly under a spherical magnet, the signal can be
calculate directly.

.. autosummary::

    mrfmsim.experiment.CermitSingleSpinGroup


