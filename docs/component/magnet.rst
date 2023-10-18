Magnet
======

Summary
-------

Here we are assuming the magnets are:

- uniformly magnetized
- magnetized in the z direction

Currently the two types of magnets supported

.. autosummary::

    mrfmsim.component.magnet.SphereMagnet
    mrfmsim.component.magnet.RectangularMagnet

Example Usage
^^^^^^^^^^^^^

Create a radius :math:`r = 50 \: \mathrm{nm}` sphere of cobalt
(:math:`\mu_0 M_s = 1800 \: \mathrm{mT}`) ::
    
    magnet = SphereMagnet(radius=50., mu0_Ms=1800., origin=[0., 0., 0.])

Print the magnet information::
    
    print(magnet)

:mod:`magnet` module
--------------------

.. automodule:: mrfmsim.component.magnet
    :members:
    :undoc-members:
    :show-inheritance:
