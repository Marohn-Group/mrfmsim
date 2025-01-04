Sample
======

``Sample`` is a class that stores and calculates sample-related parameters in a
MRFM experiment. Use the spin type, experimental temperature, relaxation time,
and spin density to determine the sample for simulation. The 
gyromagnetic ratio and angular momentum are calculated based on a 
pre-defined dictionary. The computed parameters include the homogenous linewidth 
and saturation linewidth.

Example Usage
^^^^^^^^^^^^^

To create an electron spin sample:

.. code:: python

    from mrfmsim.component import Sample
    sample = Sample(
        spin='e',
        temperature=4.2,
        T1=1e-3,
        T2=250e-9,
        spin_density=2.41e-2)

Print out the summary of the sample:

.. code:: python

    >>> print(sample)
    Sample
      spin = 'e'
      T1 = 1.000e-03 s
      T2 = 2.500e-07 s
      temperature = 4.200 K
      spin_density = 0.024 1/nm^3
      Gamma = 1.761e+08 rad/(s.mT)
      J = 0.5
      dB_hom = 0.023 mT
      dB_sat = 0.000 mT

:mod:`sample` module
--------------------

.. automodule:: mrfmsim.component.sample
    :members:
    :undoc-members:
    :show-inheritance:
