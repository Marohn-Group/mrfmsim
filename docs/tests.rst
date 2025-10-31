Tests
=====

Overview
--------

This module is a collection of files that test the functions in the **MrfmSim** package.
To run the unit tests, open up a terminal in the ``MrfmSim`` directory and 
run the following command::

    python -m pytest

Signal verification
-------------------

We can test the signal-calculation modules by computing the signal from a single spin.
Consider a magnet-tipped cantilever operated in the hangdown geometry: 

- a magnetic field is applied along the :math:`z` direction to polarize the
  cantilever's magnet and to define the quantization axis of the sample's spins; 
- the cantilever oscillates in the :math:`x` direction;
- the long axis of the cantilever is parallel to the :math:`z` direction;
- the magnet at the tip of the cantilever is a sphere of radius :math:`r`, polarized
  along the :math:`z` direction, with saturation magnetization :math:`M_s` 
  and saturation field :math:`\mu_0 M_s`; 
- the center of the spherical magnet lies at the origin, :math:`(0,0,0)`;
- the sample lies in the :math:`xy` plane; for simplicity, we further assume 
  that the spin lies along the :math:`y = 0` line; 
- the distance between the *center* of the magnet and the sample plane is :math:`z`.

Some notes on the additional tests

Magnet Test
-----------

The RectMagnet is tested through its symmetry factors: it is symmetric in the :math:`z` direction
when x and y are 0. The gradient functions are tested against a numerical derivative calculation
from the field. :math:`B_z` is an even function in the :math:`x` direction,
:math:`B_{zx}` is an odd function in the :math:`x` direction, and
:math:`B_{zxx}` is an even function in the :math:`x` direction.


Polarization Test
-----------------

The polarization test for ``irrad_periodic`` function is taken from John's notebook 

.. _tests_experimental_section:

Experiment Test
---------------

Some of the tests are calculated against some of the old notebook examples from John and Corinne. 
Note to see the notebook and examples go to the
`MrfmSim-archived <https://github.com/peterhs73/MrfmSim-archived>`__ package's git commit (c74d504).

- ``IBMCyclic`` dF_spin -> test_experiment from John Marohn.
- ``IBMCyclic`` dF2_spin -> value taken from test-ibmexpt-1.ipynb simulation 1, #4 - 9, 
  matching with relative 5e-5 precision.
- ``CermitARP`` is taken from "test_cornellexptobject.py"
- ``CermitESR`` is tested against value from "test-cornellexpt-4.ipynb"
  (Moore experiment - local peak, # 0 - 5, Issac Experiment, # 24 - 28) 
  the difference in value is expected because the min_abs_offset
  function fixed a previous issue.
- ``CermitARP_SmallTip`` is tested against "test-cornellexpt-8-Hickman_nanomagnet_simulations.ipynb", first simulation.
- CermitARP_SmallTip is compared with CermitARP, in two cases using a rectangular magnet,
  one is when the amplitude is small, they should be the same, and when tip_sep is large,
  the effect of amplitude is also small
  (There is a comparison in "test-micrometertip_smallampapprox_vs_exactsol.ipynb"
  on small amplitude, however, the result is unchecked).
- CermitSingleSpinESR_Approx is compared with CermitARP_SmallTip.
- SingleSpinESR
    - The approximation is tested against both SPAM and hangdown geometry of the analytical solution

..  ``CermitNut`` are taken from "test_cornellexptobject.py"
..     (note for CermitNut, tp unit is s instead of micro seconds).

Force detection
^^^^^^^^^^^^^^^

The force produced by a single spin is

.. math::

    \delta F_{\mathrm{spin}} = \mu_{\mathrm{spin}} \: 
        G_{zx}(r_{\mathrm{spin}})

with :math:`\mu_{\mathrm{spin}}` the spin magnetic moment and
:math:`G_{zx} = \partial B_z / \partial x` and :math:`r_{\mathrm{spin}}`
the location of the spin.
The gradient experienced by a spin located in the :math:`y = 0` plane is 

.. math::

    G_{zx}(x,0,z) = 4 \mu_0 M_s r^3 \: 
        \frac{x \: (x^2 - 4 z^2)}{(x^2 + z^2)^{7/2}}

We see that the gradient :math:`G_{zx}` is zero for a spin directly below the
tip at :math:`(0,0,z)`.  For the single-spin force experiment, we must therefore
place the spin "off to the side", at a location :math:`(x,0,z)`.
The gradient is maximized at (approximately) :math:`x_{\mathrm{opt}} = \pm 0.389295 \: z`. 
For a spin placed at this optimal location,

.. math::
    
    G_{zx}(x_{\mathrm{opt}}, 0, z)  
        \approx 0.914269 \: \frac{\mu_0 M_s}{r}
        \left( \frac{r}{z} \right)^{4}
    
In the hangdown-geometry experiment delineated above, the force acting on a magnet-tipped
cantilever from a single spin placed at an optimal location "off to the side" of the cantilever tip is

.. math::

    \delta F_{\mathrm{spin}} 
        \approx 0.914269 \: \mu_{\mathrm{spin}} \: 
        \frac{\mu_0 M_s}{r}
        \left( \frac{r}{z} \right)^{4}

With

* tip magnetization :math:`\mu_0 M_s = 1800 \: \mathrm{mT}` (cobalt)
* tip radius :math:`r = 50 \: \mathrm{nm}`
* tip-sample separation :math:`20 \: \mathrm{nm}`, that is, :math:`z = 70 \: \mathrm{nm}`
* a single (fully polarized) electron spin placed at :math:`(27.2507, 0.0000, 70.0000) \: \mathrm{nm}`

the force is

.. math::

    \delta F_{\mathrm{spin}} = -79.231 \: \mathrm{aN}

Force-gradient detection
^^^^^^^^^^^^^^^^^^^^^^^^

The force-gradient produced by a single spin is 

.. math::

    \delta k_{\mathrm{spin}} = \mu_{\mathrm{spin}} \: 
        G_{zxx}(r_{\mathrm{spin}})

with :math:`G_{zxx} = \partial^2 B_z / \partial x^2`.
For a single spin directly below the tip at :math:`(0,0,z)`, 

.. math::

    G_{zxx}(0,0,z) = - \frac{4 \mu_0 M_s r^3}{z^5}
     = - \frac{4 \mu_0 M_s}{r^2} \left( \frac{r}{z} \right)^{5}

In the hangdown-geometry experiment delineated above, the force gradient
acting on a magnet-tipped cantilever from a single spin placed directly below the cantilever tip is

.. math::

    \delta k_{\mathrm{spin}} 
        = - \mu_{\mathrm{spin}} \: \frac{4 \mu_0 M_s}{r^2}
            \left( \frac{r}{z} \right)^{5}

With

* tip magnetization :math:`\mu_0 M_s = 1800 \: \mathrm{mT}` (cobalt)
* tip radius :math:`r = 50 \: \mathrm{nm}`
* tip-sample separation :math:`20 \: \mathrm{nm}`, that is, :math:`z = 70 \: \mathrm{nm}`
* a single (fully polarized) electron spin placed at :math:`(0.0, 0.0, 70.0) \: \mathrm{nm}`

the force gradient is

.. math::

    \delta k_{\mathrm{spin}} = 4.95203 \: \mathrm{aN} \: \mathrm{nm}^{-1}
     = 4.95203 \: \mathrm{nN} \: \mathrm{m}^{-1}
    

Testing Lists
-------------

.. automodule:: tests.test_experiment.test_cermitesr
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: tests.test_experiment.test_cermitarp
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: tests.test_experiment.test_cermitsinglespin
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: tests.test_experiment.test_ibmcyclic
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: tests.test_formula.test_field
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: tests.test_formula.test_math
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: tests.test_formula.test_magnetization
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: tests.test_formula.test_misc
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: tests.test_formula.test_polarization
    :members:
    :undoc-members:
    :show-inheritance:
