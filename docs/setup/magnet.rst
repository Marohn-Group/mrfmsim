Magnet
======

In *mrfmsim*, we assume the magnets are:

- uniformly magnetized
- magnetized in the :math:`z`-direction

Currently, the two types of magnets supported are

.. autosummary::

    mrfmsim.component.magnet.SphereMagnet
    mrfmsim.component.magnet.RectangularMagnet

Example Usage
-------------

To create a nickel spherical magnet (:math:`\mu_0 M_s = 1800 \: \mathrm{mT}`)
with a radius of :math:`r = 50 \: \mathrm{nm}`:

.. code-block:: python
    
    from mrfmsim.component import SphereMagnet
    magnet = SphereMagnet(magnet_radius=50.0, mu0_Ms=800.0, magnet_origin=[0.0, 0.0, 0.0])

To display the magnet information:

.. code-block:: python

    >>> print(magnet)
    SphereMagnet
      magnet_radius = 50.0 nm
      magnet_origin = [0.0, 0.0, 0.0] nm
      mu0_Ms = 800.000 mT

:mod:`magnet` module
--------------------

.. automodule:: mrfmsim.component.magnet
    :members:
    :undoc-members:
    :show-inheritance:
