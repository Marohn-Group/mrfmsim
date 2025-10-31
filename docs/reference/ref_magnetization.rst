Equilibrium magnetization and variance
========================================

Equilibrium magnetization
^^^^^^^^^^^^^^^^^^^^^^^^^

:py:func:`formula.magnetization.mz_eq`: equilibrium magnetization per 
spin [#Brill]_

From the sample properties, we compute the magnetic moment
:math:`\mu` of the state with the largest :math:`m_J` quantum number,

.. math::
    \mu = \hbar\gamma J [\mathrm{aN}\:\mathrm{nm}\:\mathrm{mT}^{-1}]

We calculate the ratio of the energy level splitting of spin states to
the thermal energy,

.. math::
    x = \dfrac{\mu B_0}{k_b T} \: [\mathrm{unitless}],

and define the following two unitless numbers:

.. math::
    a &= \dfrac{2 \: J + 1}{2 \: J} \\
    b &= \dfrac{1}{2 \: J}

In terms of these intermediate quantities, the thermal-equilibrium
polarization is given by

.. math::
    p_{\text{eq}} = a \coth{(a x)} - b \coth{(b x)}
        \: [\mathrm{unitless}].

The equilibrium magnetization is given by

.. math::
    \mu_z^{\text{eq}} = p_{\text{eq}} \: \mu \:
        [\mathrm{aN} \: \mathrm{nm} \: \mathrm{mT}^{-1}].

In the limit of low field or high temperature,
the equilibrium magnetization
tends towards the Curie-Weiss law,

.. math::
    \mu_z^{\text{eq}}
    \approx \dfrac{\hbar^2 \gamma^2 \: J (J + 1)}{3 \: k_b T} B_0


Equilibrium variance
^^^^^^^^^^^^^^^^^^^^

:py:func:`formula.magnetization.mz2_eq`: magnetization variance per 
spin, magnetization variance density [#Xue2011nov]_

Compute the magnetization variance per spin and the magnetization
variance density for spins fluctuating at thermal equilibrium.

Mz2_eq: magnetization variance per spin [aN^2 nm^2/mT^2] times
gradient

The variance in a single spin's magnetization in the low-polarization
limit is given by [#Xue2011nov]_

.. math::
    \sigma_{{\cal M}_{z}}^{2} = \hbar^2
    \gamma^2 \dfrac{J \: (J + 1)}{3}

The magnetization variance density is obtained from
:math:`\sigma_{{\cal M}_{z}}^{2}` by multiplying by the sample's spin
density :math:`\rho`.

.. note::
    We assume for simplicity that the root mean square
    polarization fluctuations are much larger than the equilibrium
    polarization.  In this limit, the polarization fluctuations are
    independent of applied field :math:`B_0` and temperature :math:`T`.
    This approximation will *not* be valid for :math:`p \sim 1`
    electrons.


.. [#Brill] `"Brillouin and Langevin functions" 
    <http://en.wikipedia.org/wiki/Brillouin_and_Langevin_functions>`__

.. [#Xue2011nov] Equations 1 and 2 in Xue, F.; Weber, D.; Peddibhotla, P. & 
    Poggio, M. "Measurement of statistical nuclear spin polarization in a 
    nanoscale GaAs samples", *Phys. Rev. B*, **2011**, *84*, 205328
    [`10.1103/PhysRevB.84.205328 
    <http://dx.doi.org/10.1103/PhysRevB.84.205328>`__].


:py:mod:`formula.magnetization` module
----------------------------------------------------

.. automodule:: mrfmsim.formula.magnetization
    :members:
    :undoc-members:
    :show-inheritance:
