Sample
======

Summary
-------

Use the nucleus type, experimental temperature, relaxation time and spin density
to determine the sample for simulation. The gyromagnetic ratio and angular 
momentum are determined based on pre-defined dictionary.

Example Usage
^^^^^^^^^^^^^

Create a electron spin sample

.. code:: python

    esr_sample = Sample(
        nucleus='electron',
        temperature=4.2,
        T1=1e-3,
        T2=250e-9,
        spin_density=2.41e-2)

Print out the summery of the sample::

    print(esr_sample)

:mod:`sample` module
--------------------

.. automodule:: mrfmsim.component.sample
    :members:
    :undoc-members:
    :show-inheritance:
