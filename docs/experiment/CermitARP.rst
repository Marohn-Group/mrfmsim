CERMIT adiabatic rapid passage
=========================================

Overview
--------

The Zeeman field :math:`B_z(\vec{r})` experienced by spins at location
:math:`\vec{r}` is a sum of the :math:`z` component of the tip field and the 
static field, which we take to be oriented along the :math:`z` axis,

.. math::
    :label: Eq:Bz

    B_z(\vec{r}) = B_0 + B_z^{\mathrm{tip}}(\vec{r})

Here we assume that  :math:`B_0 \gg B_z^{\mathrm{tip}}`, which requires us 
to consider only the :math:`z` component of the tip field and spin 
magnetization. 
The spin-dependent change in the spring constant is determined using

.. math::
    :label: Eq:DeltaK

    \delta k_{\mathrm{spin}} = - \sum_j 
        \delta M_z (\vec{r}_j) 
        \frac{\partial^2 B_{z}^{\mathrm{tip}}({\vec{r}}_j)}{\partial z^2}
        \Delta V_j  

where :math:`\delta M_z` is the change in magnetization density and
:math:`\Delta V_j` is the volume of each voxel (or volume element) in the 
sample. We have drawn equation :eq:`Eq:DeltaK` (with its leading minus sign) 
from reference [#Lee2012apra]_ (equation 8). We have taken care to implement 
the leading minus sign here.

Let us now derive the equations we will use to calculate the change in 
magnetization density :math:`\delta M_z (\vec{r})` resulting from the 
adiabatic rapid passage. In a frame of reference rotating counter-clockwise 
about the :math:`z` axis at frequency :math:`\omega`, the magnetization 
density evolves under the action of the effective field

.. math::
    :label: Eq:B_eff

    \vec{B}_{\mathrm{eff}} = 
        (B_z(\vec{r}) - \frac{\omega}{\gamma}) \hat{z} 
        + B_1 \hat{x}_{\mathrm{R}} 

with :math:`\hat{z}` a unit vector along :math:`z` axis,
:math:`\hat{x}_{\mathrm{R}}` a transverse rotating basis vector,
:math:`B_z(\vec{r})` given by equation :eq:`Eq:Bz`, :math:`\omega` the 
frequency of the applied oscillating field, :math:`\gamma` the gyromagnetic 
ratio, and :math:`2 B_1` the amplitude of the oscillating magnetic field, 
assumed to be linearly polarized. We are making the rotating wave 
approximation in using equation :eq:`Eq:B_eff` to describe the evolution of 
magnetization under linearly polarized irradiation. It is useful to write 
down a unit vector parallel to the effective field:

.. math::
    :label: Eq:beff

    \vec{b}_{\mathrm{eff}} =
        \frac{B_z(\vec{r}) - \omega/\gamma}
        {\sqrt{(B_z(\vec{r}) - \omega/\gamma)^2 + B_1^2}} \hat{z} 
        + \frac{B_1}
        {\sqrt{(B_z(\vec{r}) - \omega/\gamma)^2 + B_1^2}} \hat{x}_{\mathrm{R}} 

Dividing both the numerators and denominators in the equation :eq:`Eq:beff` by 
:math:`B_1`, this unit vector can be written as

.. math::
    :label: Eq:beff2

    \hat{b}_{\mathrm{eff}}(\Omega) =
        \frac{\Omega}{\sqrt{\Omega^2+1}} \hat{z} 
        + \frac{1}{\sqrt{\Omega^2+1}} \hat{x}_{\mathrm{R}} 

with 

.. math::
    :label: Eq:Omega
    
    \Omega = \frac{\gamma B_z(\vec{r}) - \omega}{\gamma B_1}  

the (unitless) ratio of the resonance offset to the Rabi frequency; 
:math:`\Omega > 0` and :math:`\hat{b}_{\mathrm{eff},z} > 0` for spins at
a field above the resonance field :math:`\omega/\gamma` while 
:math:`\Omega < 0` and :math:`\hat{b}_{\mathrm{eff},z} < 0` for spins at
a field below the resonance field :math:`\omega/\gamma`.

Now consider the evolution of sample magnetization during an adiabatic rapid 
passage through resonance. The magnetization is initially along the :math:`z`
axis. Just before time :math:`t = 0`,

.. math::
    :label: Eq:Mz0_minus
    
    \vec{M}(0^{-}) = M_{z}(0) \: \hat{z} 

At time :math:`t = 0` the irradiation is turned on with an initial offset 
frequency of :math:`\Omega_{\mathrm{i}}`. Since this effective field is not 
quite parallel to the :math:`z` axis in the rotating frame, the initial 
magnetization vector will precess around it. The component of the initial 
magnetization perpendicular to the initial effective field 
:math:`\hat{b}_{\mathrm{eff}}(\Omega_{\mathrm{i}})` will quickly dephase,
within in a time :math:`T_2 \sim 5 \: \mu\mathrm{s}`. The component of the
initial magnetization parallel to the initial effective field will survive 
this dephasing. 
The magnetization after this dephasing, at time :math:`t = 0^{+}`, 
is given by the projection of :math:`\vec{M}_{z}(0^{-})` onto 
:math:`\hat{b}_{\mathrm{eff}}`,

.. math::
    :label: Eq:Mz0_plus
    
    \vec{M}(0^{+}) = 
        M_{z}(0) \left( \hat{b}_{\mathrm{eff}}(\Omega_{\mathrm{i}}) 
        \cdot \vec{M}_{z}(0^{-}) \right) 
        \: \hat{b}_{\mathrm{eff}}(\Omega_{\mathrm{i}})

The prefactor in parenthesis may be positive or negative, depending on whether 
:math:`\vec{M}_{z}(0^{-})` and
:math:`\hat{b}_{\mathrm{eff}}(\Omega_{\mathrm{i}})` are parallel
(:math:`\Omega >0`) or antiparallel (:math:`\Omega <0`). Substituting
equations :eq:`Eq:beff2` and :eq:`Eq:Mz0_minus` into equation :eq:`Eq:Mz0_plus`

.. math::
    :label: Eq:Mz0+2 

    \begin{align}
    \vec{M}(0^{+}) & =
        M_{z}(0) \frac{\Omega_{\mathrm{i}}}{\sqrt{\Omega_{\mathrm{i}}^2+1}}
        \left( 
            \frac{\Omega_{\mathrm{i}}}{\sqrt{\Omega_{\mathrm{i}}^2+1}} \hat{z} 
            + \frac{1}{\sqrt{\Omega_{\mathrm{i}}^2+1}} \hat{x}_{\mathrm{R}} 
        \right) \\
    & = 
    M_{z}(0) 
        \left( 
            \frac{\Omega_{\mathrm{i}}^2}{\Omega_{\mathrm{i}}^2+1} \hat{z} 
            + \frac{\Omega_{\mathrm{i}}}{\Omega^2_{\mathrm{i}}+1} 
            \hat{x}_{\mathrm{R}}
        \right)
    \end{align} 

We can see that equation :eq:`Eq:Mz0+2` captures :math:`\vec{M}_{z}(0^{+})` 
correctly for spins initially above and below resonance when the irradiation 
is turned on.  For example, when :math:`\Omega = +10`, 
:math:`\vec{M}_{z}(0^{+}) = 0.99 \: \hat{z} + 0.01 \: \hat{x}_{\mathrm{R}}` 
while when :math:`\Omega = -10`, 
:math:`\vec{M}_{z}(0^{+}) = 0.99 \: \hat{z} - 0.01\: \hat{x}_{\mathrm{R}}`.
In both cases, :math:`\vec{M}_{z}(0^{+})` points 
up as it should. The magnitude of :math:`\vec{M}_{z}(0^{+})` is

.. math::
    :label: Eq:AbsMz0+

    \begin{align}
    \| \vec{M}(0^{+}) \| 
    & = M_{z}(0) 
    \left(
        \frac{\Omega_{\mathrm{i}}^4}{(\Omega_{\mathrm{i}}^2+1)^2} 
        + \frac{\Omega_{\mathrm{i}}^2}{(\Omega_{\mathrm{i}}^2+1)^2}
    \right)^{1/2} \\
    & = M_{z}(0) 
    \left(
        \frac{\Omega_{\mathrm{i}}^2 (\Omega_{\mathrm{i}}^2 + 1) }
        {(\Omega_{\mathrm{i}}^2+1)^2}
    \right)^{1/2} \\
    & = M_{z}(0) 
    \frac{\| \Omega_{\mathrm{i}} \|}{\sqrt{\Omega_{\mathrm{i}}^2 + 1}}
    \end{align}

At a time just *after* :math:`t = 0^+`, the adiabatic rapid passage is 
initiated and :math:`\Omega` is swept from the initial offset
:math:`\Omega_{\mathrm{i}}` to a final offset :math:`\Omega_{\mathrm{f}}`. At
the end of the sweep, at time :math:`t_{\mathrm{f}}`, the magnetization
density vector will have the same magnitude as it did at time 
:math:`t = 0^+`,
but will be oriented parallel or antiparallel to the final effective field,
:math:`\hat{b}_{\mathrm{eff}}(\Omega_{\mathrm{f}})`,

.. math::
    :label: Eq:vecMtf

    \vec{M}(t_{\mathrm{f}}) = 
    \| \vec{M}_{z}(0^{+}) \| \: \mathrm{sign}(\Omega_{\mathrm{i}})
    \left( 
        \frac{\Omega_{\mathrm{f}}}{\sqrt{\Omega_{\mathrm{f}}^2+1}} \hat{z} 
        + \frac{1}{\sqrt{\Omega_{\mathrm{f}}^2+1}} \hat{x}_{\mathrm{R}} 
    \right) 

Here :math:`\mathrm{sign}(\Omega_{\mathrm{i}})` accounts for the final 
magnetization being parallel (for positive initial offset,
:math:`\mathrm{sign}(\Omega_{\mathrm{i}}) = +1`) or antiparallel (for 
negative initial offset, :math:`\mathrm{sign}(\Omega_{\mathrm{i}}) = -1`) to 
the final effective field. We are interested in the :math:`z`-component of 
the final magnetic field vector. Substituting  equation :eq:`Eq:AbsMz0+` 
into equation :eq:`Eq:vecMtf` and using

.. math:: 

    \mathrm{sign}(\Omega_{\mathrm{i}}) \: \| 
    \Omega_{\mathrm{i}} \| = \Omega_{\mathrm{i}}

.. math::
    :label: Eq:Mzf

    M_{z}(t_{\mathrm{f}}) 
    =  M_{z}(0)
        \dfrac{\Omega_{\mathrm{i}}}{\sqrt{\Omega_{\mathrm{i}}^2+1}}
        \dfrac{\Omega_{\mathrm{f}}}{\sqrt{\Omega_{\mathrm{f}}^2+1}}

At each point in the sample, the change, final minus initial, in :math:`z`
component of magnetization following the adiabatic rapid passage is given by

.. math::
    :label: Eq:deltaMz

    \delta M_{z} = M_{z}(t_{\mathrm{f}}) - M_{z}(0) 
    =  M_{z}(0)
    \left(
        \dfrac{\Omega_{\mathrm{i}}}{\sqrt{\Omega_{\mathrm{i}}^2+1}}
        \dfrac{\Omega_{\mathrm{f}}}{\sqrt{\Omega_{\mathrm{f}}^2+1}} 
        -1
    \right)

If we sweep from :math:`\Omega_{\mathrm{i}} \rightarrow +\infty` (way above 
resonance) to :math:`\Omega_{\mathrm{f}} \rightarrow -\infty` (way below 
resonance), then :math:`\delta M_{z} = -2 M_{z}(0)`. This is what we expect 
to see. For a swept-field or swept-tip experiment, 

.. math::
    :label: Eq:omegas1
     
    \Omega_{\mathrm{i}} =
    \frac{B_z(\vec{r}_{\mathrm{i}}) - \omega/\gamma}{B_1}
    \: \: \: \mathrm{and} \: \: \:
    \Omega_{\mathrm{f}} = 
    \frac{B_z(\vec{r}_{\mathrm{f}}) - \omega/\gamma}{B_1}

while for a swept-frequency experiment, 

.. math::
    :label: Eq:omegas2
     
    \Omega_{\mathrm{i}} = 
    \frac{B_z(\vec{r}) - \omega_{\mathrm{i}}/\gamma}{B_1}
    \: \: \: \mathrm{and} \: \: \:
    \Omega_{\mathrm{f}} =
    \frac{B_z(\vec{r}) - \omega_{\mathrm{f}}/\gamma}{B_1}

To compute the change in magnetization contributing to signal at each 
position, we will use the equation :eq:`Eq:deltaMz` and either equation
:eq:`Eq:omegas1` (for a swept-tip experiment) or equation :eq:`Eq:omegas2`
(for a swept-frequency experiment). In the swept-frequency calculation we 
need to compute the field at each point. In the swept-tip calculation, we 
need to compute at each position :math:`\vec{r}` in the sample the :math:`z` 
component of the magnetic field *only* at the beginning
(:math:`\vec{r} = \vec{r}_{\mathrm{i}}`) and end
(:math:`\vec{r} = \vec{r}_{\mathrm{f}}`) of the tip sweep.

Adiabaticity
^^^^^^^^^^^^

We would also like to assess the adiabaticity of the sweep.  With 

.. math::

    M_{z}(t) = M_{z}(0) \: \cos{(\theta(t))},

the adiabaticity parameter is generally defined as

.. math::

    \alpha = \frac{\dot{\theta}}{\gamma B_1}.


In a cryogenic ESR-MRFM observing :math:`\mathrm{E}^{\prime}` centers in 
quartz *via* cyclic adiabatic inversion, Wago and coworkers observed a peaking 
of signal when :math:`\alpha \sim 0.1` (note that they define the adiabaticity 
parameter as :math:`1/\alpha`) [#Wago1998jan]_. In a room temperature NMR-MRFM 
experiment observing proton magnetization in an ammonium nitrate crystal *via* 
cyclic adiabatic inversion and force detection, Klein and coworkers observed 
lossless inversion of magnetization when
:math:`\alpha \leq 0.1` [#Klein2000aug]_. 
In both of these experiments, a linear frequency sweep was used. We note 
that more efficient sweeps have been devised. [#Baum1985dec]_ [#Kupce1996feb]_
For a linear sweep, the adiabaticity parameter is *largest* near resonance,
where

.. math::

    \alpha_{\mathrm{res}} 
        = \frac{1}{\gamma B_1^2} \frac{d B_{\mathrm{eff}}}{d t} 
        = \frac{1}{\omega_1} \frac{d \Omega}{d t} 

Here :math:`\Omega` is given by equation :eq:`Eq:Omega` and :math:`\omega_1 = 
\gamma B_1` is the Rabi frequency.  In a swept-tip experiment, the field at 
position :math:`\vec{r}` changes by an amount :math:`\delta B = 
B_{z}^{\mathrm{tip}}(\vec{r}_{\mathrm{f}}) - B_
{z}^{\mathrm{tip}}(\vec{r}_{\mathrm{i}})` in a time equal to half of a 
cantilever period, :math:`\delta t = 1/(2 f_c)`.  If we approximate the sweep 
as linear, then the adiabaticity parameter is given by

.. math::
    :label: Eq:alpha-swept-tip

    \alpha_{\mathrm{res}}(\vec{r}) 
        \approx \frac{1}{\gamma B_1^2} \frac{\delta B}{\delta t}
    = \frac{2 f_c}{\gamma B_1^2} 
    \| B_{z}^{\mathrm{tip}}(\vec{r}_{\mathrm{f}}) -
    B_{z}^{\mathrm{tip}}(\vec{r}_{\mathrm{i}}) \|

We have introduced an absolute value sign to guarantee that :math:`\alpha` is 
positive and independent of the sweep direction. We write :math:`
\alpha_{\mathrm{res}}(\vec{r})` to emphasize that the adiabaticity parameter 
should be evaluated at each position :math:`\vec{r}` in the sample. Equation 
:eq:`Eq:alpha-swept-tip` is only strictly valid at resonance and, moreover, 
does not account for the sinusoidal time dependence of :math:`\vec{r}(t)` 
during the cantilever motion. Nevertheless, we will use it to access the 
adiabaticity of the spin inversion in the swept-tip experiment. Since :math:`
\alpha` is smaller for sample spins that do not pass through resonance, 
equation :eq:`Eq:alpha-swept-tip` provides an upper-bound estimate for the 
adiabaticity parameter at any location. The spins that contribute most to 
the signal are those that pass through resonance; for these spins, equation :eq:`
Eq:alpha-swept-tip` should be reasonably accurate.

In the swept-frequency experiment, the irradiation frequency is ramped from 
:math:`\omega_{\mathrm{i}}` to :math:`\omega_{\mathrm{f}}` in a time :math:`
\Delta T_{\mathrm{sweep}}`; the period of the sweep :math:`\Delta T_
{\mathrm{sweep}}` is not restricted to be half a cantilever period. The 
adiabaticity parameter is independent of position :math:`\vec{r}` and, 
assuming a linear frequency sweep, equal to 

.. math::
    :label: Eq:alpha-swept-freq

    \alpha_{\mathrm{res}} = 
        \frac{1}{\gamma^2 B_1^2} 
        \frac{\| \omega_{\mathrm{f}} - \omega_{\mathrm{i}} \|}
        {\Delta T_{\mathrm{sweep}}}

As with equation :eq:`Eq:alpha-swept-tip`, equation  :eq:`Eq:alpha-swept-freq` 
is only strictly valid for spins that pass through resonance.  Spins far away 
from the resonant slice will experience an :math:`\alpha` even smaller and 
:math:`\alpha_{\mathrm{res}}`.  We can therefore regard equation :eq:`
Eq:alpha-swept-freq` as an upper bound for the adiabaticity parameter 
experienced by any spin in the sample.

.. [#Klein2000aug] Klein, O.; Naletov, V. & Alloul, H. "Mechanical Detection 
    of Nuclear Spin Relaxation in a Micron-size Crystal", *Eur. Phys. J. B*, 
    **2000**, *17*, 57 - 68 
    [`10.1007/s100510070160 <http://dx.doi.org/10.1007/s100510070160>`__].

.. [#Lee2012apra] Lee, S.-G.; Moore, E. W. & Marohn, J. A. "A Unified Picture 
    of Cantilever Frequency-Shift Measurements of Magnetic Resonance", 
    *Phys. Rev. B*, **2012**, *85*, 165447 
    [`10.1103/PhysRevB.85.165447 <http://dx.doi.org/10.1103/PhysRevB.85.165447>`__].  

.. [#Wago1998jan] Wago, K.; Botkin, D.; Yannoni, C. & Rugar, D. 
    "Force-detected Electron-spin Resonance: Adiabatic Inversion, Nutation, 
    and Spin Echo", *Phys. Rev. B*, **1998**, *57*, 1108 - 1114 
    [`10.1103/PhysRevB.57.1108 <http://doi.org/10.1103/PhysRevB.57.1108>`__].

.. [#Baum1985dec] Baum, J.; Tycko, R. & Pines, A. "Broadband and Adiabatic 
    Inversion of a Two-level System by Phase-modulated Pulses", *Phys. Rev. A*
    , **1985**, *32*, 3435 - 3447 
    [`10.1103/PhysRevA.32.3435 <http://dx.doi.org/10.1103/PhysRevA.32.3435>`__].

.. [#Kupce1996feb] Kupce, E. & Freeman, R. "Optimized Adiabatic Pulses for 
    Wideband Spin Inversion", *Journal of Magnetic Resonance, Series A*, 
    **1996**, *118*, 299 - 303
    [`10.1006/jmra.1996.0042 <http://dx.doi.org/10.1006/jmra.1996.0042>`__].

Experiment Summary
-------------------------

.. autosummary::

    mrfmsim.experiment.CermitARPGroup
    mrfmsim.formula.polarization.rel_dpol_arp

.. autodata:: mrfmsim.experiment.CermitARPGroup

.. group:: mrfmsim.experiment.cermitarp.CermitARPGroup

