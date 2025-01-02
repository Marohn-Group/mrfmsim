Tip size: small tip vs. large tip
==================================

Currently, we have two different sizes of magnets --- the large tips
are micron-sized spherical magnets (1 - 4 µm in diameter);
the small tips are nanometer-sized rectangular prism 
(~100 nm in cross-section length).

For large tips, the cantilever amplitude (100 - 300 nm) is small compared to the
tip size, and for small tips, the cantilever amplitude is comparable to
the tip size. They result in different approximations for the **CERMIT protocol**.

Large tip - small amplitude limit
--------------------------------------

In the small-amplitude limit, we can calculate the spin-dependent frequency 
shift experienced by the cantilever using

.. math::
    :label: Eq:LargeTipDf

    \Delta f = - \frac{f}{2 k} \sum_j \mu_z(\vec{r}_j) 
        \frac{\partial^{\, 2} B_z^{\mathrm{tip}}( \vec{r}_j )}{\partial x^2}

where :math:`f \: [\mathrm{Hz}]` is the cantilever resonance frequency and 
:math:`k \: [\mathrm{N} \: \mathrm{m}^{-1}]` is the cantilever spring 
constant. The direction of the applied magnetic field is the :math:`z` and the 
direction of the cantilever motion is :math:`x`. In equation :eq:`Eq:LargeTipDf`, 
:math:`\mu_z \: [\mathrm{N} \: \mathrm{m} \: \mathrm{T}^{-1}]` is the :math:`z`
component of the spin magnetic moment, and :math:`B_z^{\mathrm{tip}} \:
[\mathrm{T}]` is the :math:`z` component of the magnetic field produced by the 
cantilever's magnetic tip. The sum represents a sum over all spins in 
resonance (discussed below). The frequency shift arises from a spring constant 
shift of

.. math::
    :label: Eq:LargeTipDk

    \Delta k = - \sum_j \mu_z(\vec{r}_j) 
        \frac{\partial^{\, 2} B_z^{\mathrm{tip}}( \vec{r}_j )}{\partial x^2}

Equations :eq:`Eq:LargeTipDf` and :eq:`Eq:LargeTipDk` are valid when the 
zero-to-peak amplitude of the cantilever oscillation is much smaller than the 
distance between the center of the (spherical) magnet and the sample spins.
[#Lee2012apra]_

In the ESR-CERMIT experiment of Moore *et al.*, the magnetization distribution 
:math:`\mu_z (\vec{r})` depends, according to the steady-state Bloch 
equations, on the frequency :math:`f_{\mathrm{rf}}` and strength :math:`B_1` 
of the microwave field, the sample relaxation times :math:`T_1` and :math:`T_2`
, the sample spin density, the applied magnetic field :math:`B_0`, the tip 
magnetic field :math:`B_z^{\mathrm{tip}}`, and cantilever position.  In the 
Moore experiment, the cantilever sweeps out a region of saturated 
magnetization as it moves.

In the NMR-CERMIT experiment of Garner *et al.*, [#Garner2004jun]_ 
the frequency of the applied radio frequency field :math:`f_{\mathrm{rf}}` is 
swept. The initial magnetization follows the effective field at each location 
in the sample, resulting in a region of inverted magnetization below the tip.


Small tip - large amplitude limit
----------------------------------

The small-amplitude approximation used to derive the above equations may not 
be valid in a small-tip ESR-CERMIT experiment.[#Lee2012apra]_ In this case, we 
must calculate the signal using Equation 20: [#Lee2012apra]_ [#Lee2012note]_

.. math::
    :label: Eq:SmallTipDf

    \Delta f = \frac{f}{2 \pi k x_{\mathrm{pk}}^2} 
        \sum_j \int_{-\pi}^{\pi} \mu_z(\vec{r}_j,\theta)
            \frac{\partial B_z^{\mathrm{tip}}(x - x_{\mathrm{pk}} 
            \cos{\theta},y,z)}{\partial x}
            x_{\mathrm{pk}} \cos{\theta} d\theta 

where :math:`x_{\mathrm{pk}}` is the zero-to-peak amplitude of the cantilever 
oscillation. We write :math:`\mu_z(\vec{r}_j,\theta)` to indicate that if the 
microwaves are left on during cantilever motion, then the magnetization may 
vary in synchrony with the cantilever oscillation. In the i-OSCAR experiment of 
Rugar and coworkers, [#Rugar2004jul]_ the resulting position-dependent change 
in magnetization led to a measurable frequency shift.

Equation :eq:`Eq:SmallTipDf` is exact.  To understand the nature of the 
large-tip approximation, Eq. :eq:`Eq:LargeTipDf`, let us expand the Eq. 
:eq:`Eq:SmallTipDf` gradient in the :math:`x` variable:

.. math::
    :label: Eq:expansion
    
    \frac{\partial B_z^{\mathrm{tip}}(x - x_{\mathrm{pk}} \cos{\theta},y,z)}
    {\partial x} \approx \frac{\partial B_z^{\mathrm{tip}}(x,y,z)}{\partial x}
    - x_{\mathrm{pk}} \cos{\theta} \frac{\partial^2 B_z^{\mathrm{tip}}(x,y,z)}
    {\partial x^2} + {\cal O}(x_{\mathrm{pk}}^2)

In calculating the signal from our ESR-CERMIT experiment, we will assume for 
simplicity that the spin distribution :math:`\mu_z(\vec{r}_j)` has reached 
steady-state; we neglect any change in the magnetization during the cantilever 
motion. In this approximation

.. math::
    :label: Eq:SmallTipDf2

    \Delta f = \frac{f}{2 \pi k x_{\mathrm{pk}}^2} \sum_j
    \int_{-\pi}^{\pi} 
        \mu_z(\vec{r}_j)
            \left( 
                \frac{\partial B_z^{\mathrm{tip}}(x,y,z)}{\partial x}
                - x_{\mathrm{pk}}                         
                \cos{\theta} \: \frac{\partial^2 
                B_z^{\mathrm{tip}}(x,y,z)}{\partial x^2}         
            \right)
        \: x_{\mathrm{pk}} \cos{\theta}
    \: d\theta

There are two terms. The first term is

.. math::
    \Delta f^{(1)} = \frac{f}{2 \pi k x_{\mathrm{pk}}} \sum_j \mu_z(\vec{r}_j) 
    \frac{\partial B_z^{\mathrm{tip}}(x,y,z)}{\partial x}
    \int_{-\pi}^{\pi} \cos{\theta} \: d\theta 

We are interested in experiments in the SPAM geometry and the 
"hangdown" geometry. The geometries are shown in doc :doc:`geometry`.
In both cases, the first term vanishes: the sum 
over sample spins is zero since the gradient is positive and negative 
over the sensitive slice. Moreover, the integral over :math:`\theta` is zero. 
The second term in Eq. :eq:`Eq:SmallTipDf2` is

.. math::
    \Delta f^{(2)} = - \frac{f}{2 k} \sum_j \mu_z(\vec{r}_j)
    \frac{\partial^2 B_z^{\mathrm{tip}}(x,y,z)}{\partial x^2}
    \underbrace{\frac{1}{\pi} \int_{-\pi}^{\pi} \cos^2{\theta} \:
    d\theta}_{= 1}  

which simplifies to the large-tip result, Eq. :eq:`Eq:LargeTipDf`, 

.. math::
    \Delta f^{(2)} = - \frac{f}{2 k}
    \sum_j \mu_z(\vec{r}_j) \frac{\partial^2 
    B_z^{\mathrm{tip}}(x,y,z)}{\partial x^2}

We see from this derivation that the validity of Eq. :eq:`Eq:LargeTipDf` rests 
on the validity of the approximation in Eq. :eq:`Eq:expansion`.  According to 
Eq. :eq:`Eq:expansion`, for Eq. :eq:`Eq:LargeTipDf` to be valid, the change in 
the gradient experienced by any spin in the sample should be strictly linear 
in the cantilever amplitude.  This is not true for a large-amplitude 
motion of the cantilever.

Let us rewrite Eq. :eq:`Eq:SmallTipDf` by 

1. assuming that the magnetization distribution is in steady-state, 
2. writing the frequency shift in terms of an equivalent spring constant shift,
3. expressing the result in terms of an equivalent force.  

We showed in Ref. [#Lee2012apra]_ that maximizing this equivalent force 
will maximize the signal-to-noise ratio in a frequency-shift experiment. In 
terms of a force, the ESR-CERMIT signal is

.. math::
    :label: Eq:SmallTipD_F
    
    \Delta F = \Delta k \: x_{\mathrm{pk}} = \frac{2}{\pi} \sum_j
    \int_{0}^{\pi} 
        \mu_z(\vec{r}_j)
        \: \frac{\partial B_z^{\mathrm{tip}}(x - x_{\mathrm{pk}}
             \cos{\theta},y,z)}{\partial x}
        \: \cos{\theta}
    \: d\theta

In writing Eq. :eq:`Eq:SmallTipD_F` we have condensed the integral to a half 
cycle of the cantilever oscillation. In the integrand, the position variable 
:math:`x(\theta) = x - x_{\mathrm{pk}} \cos{\theta}` runs from :math:`x - 
x_{\mathrm{pk}}` to :math:`x + x_{\mathrm{pk}}` as :math:`\theta` runs from 
:math:`0` to :math:`\pi`.  In the steady-state approximation, the spin 
distribution :math:`\mu_z(\vec{r}_j)` in Eq. :eq:`Eq:SmallTipD_F` is 
determined in the same way as in the large-tip experiment.

Eric Moore and co-workers previously implemented Eqs. :eq:`Eq:SmallTipDf` and 
:eq:`Eq:SmallTipD_F` to calculate the ESR-MRFM signal from a single spin 
[#Lee2012apra]_ [#Moore2009]_

And to simulate the amplitude dependence of the 
signal from a single slice whose magnetization has been inverted *via* an 
adiabatic rapid passage.[#Moore2009dec]_

Reference
----------

.. [#Moore2009dec] Moore, E. W.; Lee, S.-G.; Hickman, S. A.; Wright, S. J.; 
    Harrell, L. E.; Borbat, P. P.; Freed, J. H. & Marohn, J. A. "Scanned-Probe 
    Detection of Electron Spin Resonance from a Nitroxide Spin Probe", *Proc. 
    Natl. Acad. Sci. U.S.A.*, **2009**, *106*, 22251 - 22256 
    [`10.1073/pnas.0908120106 <http://doi.org/10.1073/pnas.0908120106>`__].

.. [#Moore2009] Moore, E. W. & Marohn, J. A. *Unpublished calculation*, 
    **2009**.

.. [#Lee2012apra] Lee, S.-G.; Moore, E. W. & Marohn, J. A. "A Unified Picture 
    of Cantilever Frequency-Shift Measurements of Magnetic Resonance", 
    *Phys. Rev. B*, **2012**, *85*, 165447 
    [`10.1103/PhysRevB.85.165447 <http://doi.org/10.1103/PhysRevB.85.165447>`__].  

.. [#Lee2012note] Equation 20 in Lee *et al.* **2012** is off by a factor of 
    :math:`-1`.  We give the correct equation above.

.. [#Rugar2004jul] Rugar, D.; Budakian, R.; Mamin, H. J. & Chui, B. W. "Single 
    Spin Detection by Magnetic Resonance Force Microscopy", *Nature*, **2004**
    , *430*, 329 - 332 
    [`10.1038/nature02658 <http://dx.doi.org/10.1038/nature02658>`__].

.. [#Garner2004jun] Garner, S. R.; Kuehn, S.; Dawlaty, J. M.; Jenkins, N. E. &
    Marohn, J. A.  "Force-Gradient Detected Nuclear Magnetic Resonance" *Appl. 
    Phys. Lett.*, **2004**, *84*, 5091 - 5093
    [`10.1063/1.1762700 <http://dx.doi.org/10.1063/1.1762700>`__].
