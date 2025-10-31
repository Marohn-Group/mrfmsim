CERMIT time dependent offset
================================

Overview
----------------

The force-gradient detection protocol was used to detect magnetic resonance in samples with spin-lattice relaxation times longer than a cantilever period (of order 200 µs). Reference [#Moore2009dec]_ presented the CERMIT (Cantilever-Enabled Readout of Magnetization Inversion Transients) protocol used to detect electron spin resonance modulation with microwave (MW) pulses. Reference [#Boucher2023sep]_ introduced a signal model accounting for both adiabatic losses and :math:`T_2` relaxation from cantilever motion during the MW pulses. The signal model is valid in the limit of :math:`T_2 \ll T_1`, where the transverse magnetization reaches a pseudo-equilibrium with the slowly evolving longitudinal magnetization. 

Following the derivation from
:doc:`CermitSat`, the unitless time variable :math:`\tau` and relaxation time variables :math:`\alpha` and :math:`\beta` are defined as,

.. math::
    \tau = \gamma B_1 t,

.. math::
    \alpha = \frac{1}{\gamma B_1 T_1},

and

.. math::
    \beta = \frac{1}{\gamma B_1 T_2},

where :math:`\gamma` is the electron gyromagnetic ratio, and :math:`B_1` is the irradiation intensity in the rotating frame.
At low-:math:`B_1` region, we can determine numerically the final magnetization :math:`M_z^\mathrm{final}` during a cantilever sweep from :math:`\tau_i` to :math:`\tau_f`, and sweep time :math:`\tau_f - \tau_i \ll T_1` as follows,

.. math::
    :label: eq:Mz(tau0)

    M_z^\mathrm{final} 
    \approx e^{-R(\tau_i, \tau_f)} M_z^\mathrm{initial}
    

and

.. math::
    :label: eq:R(tau_f)

    R(\tau_i, \tau_f) 
    = \frac{\arctan{(\pi \alpha_1 \tau_f / \beta)} - \arctan{(\pi \alpha_1 \tau_i / \beta)}}{\pi \alpha_1},

where

.. math::
    \alpha_1 = \frac{1}{\pi \gamma B_1^2}\frac{d\Delta B_0}{dt}

is a unitless sweep-rate parameter, assuming the resonance offset changes linearly in time.

At the time :math:`\tau = 0`, the system is at the resonance condition. The argument of the arctan function can be written as

.. math::
    :label: eq:a/b

    \frac{\pi \alpha_1 \tau}{\beta} 
    = \gamma T_2 \frac{d \Delta B_0}{d t} t = \gamma T_2 \Delta B_0 (t).
    

Additionally, since we assume that the cantilever velocity remains the same during the sweep,

.. math::
    \pi \alpha_1 =\frac{1}{\gamma B_1^2}\frac{d \Delta B_0}{d t} = \frac{1}{\gamma B_1^2} \frac{\partial \Delta B_0}{\partial x} \frac{\partial x}{\partial t} = \frac{1}{\gamma B_1^2} \frac{\partial \Delta B_0}{\partial x} v_\mathrm{tip} = \frac{B_{zx}v_\mathrm{tip}}{\gamma B_1^2}.

Finally,

.. math::
    :label: eq:mzf/mzi

    \frac{M_z^\mathrm{final}}{M_z^\mathrm{initial}} \approx e^{-R(\tau_i, \tau_f)},

where 

.. math::
    R(\tau_i, \tau_f) = \frac{\gamma B_1^2}{B_{zx}v_\mathrm{tip}} (\arctan{(\gamma T_2 \Delta B_0(\tau_f)}) - \arctan{(\gamma T_2 \Delta B_0(\tau_i))}).

The above derivation accounts for the magnetization change after a single pulse. For the multi-pulse CERMIT experiment, we account for the :math:`T_1` relaxation between pulses. Given the system is at equilibrium, we use the simplified notation that before and after the pulse :math:`p`, the magnetization is :math:`M^{-} = M_z^\mathrm{eq}(\tau_p^-)` and :math:`M^{+} = M_z^\mathrm{eq}(\tau_p^+)`; and the magnetization ratio :math:`r` is :math:`r = M^{+}/M^{-} =e^{-R(\tau_p^+, \tau_p^-)}`.
The magnetization relaxes towards the initial magnetization :math:`M_0`,

.. math::
    M^{-} - M_0 = (M^{+}- M_0)e^{-\frac{t}{T_1}}

where :math:`t` is the time between pulses.
The microwave pulse occurs at the same position during the cantilever cycle, and :math:`R` remains the same regardless of the system magnetization state. With the pulse interval :math:`\Delta t`, the change in magnetization before the relaxation is

.. math::
    \Delta M^{+} = M^{+} - M_0 = \frac{r - 1}{1 - r e^{-\frac{\Delta t}{T_1}}} M_0.

Therefore, the average change in magnetization :math:`\Delta M_z^\mathrm{avg}` is

.. math::
    :label: eq:dMz_avg

    \Delta M_z^\mathrm{avg} =  \frac{\int_{0}^{\Delta t}{\Delta M^{+}e^{-\frac{t}{T_1}}} \,dt}{\Delta t} = \frac{(r - 1) (1 - e^{-\frac{t}{T_1}})}{1-re^{-\frac{t}{T_1}}}\frac{T_1}{\Delta t}.

The final signal sums over spin at location :math:`\boldsymbol{r_j}`

.. math::
    :label: eq:moore-final

    \delta f = \
    \frac{\sqrt{2}f_\mathrm{c}}{2\pi k_\mathrm{c}}\sum_j \Delta M_z^\mathrm{avg}(\boldsymbol{r_j}) \frac{\partial ^2 B^\mathrm{tip}_z (\boldsymbol{r_j})}{\partial x^2}

where :math:`f_\mathrm{c}` is the cantilever frequency, and :math:`k_\mathrm{c}` is the cantilever spring constant.

.. [#Moore2009dec] Moore, E. W.; Lee, S.-G.; Hickman, S. A.; Wright, S. J.; 
    Harrell, L. E.; Borbat, P. P.; Freed, J. H. & Marohn, J. A. "Scanned-Probe 
    Detection of Electron Spin Resonance from a Nitroxide Spin Probe", *Proc. 
    Natl. Acad. Sci. U.S.A.*, **2009**, *106*, 22251 - 22256 
    [`10.1073/pnas.0908120106 <http://doi.org/10.1073/pnas.0908120106>`__].

.. [#Boucher2023sep] Boucher, E.; Sun, P.; Keresztes, I.; Harrell, H. L.;  
    Marohn, J. A. "The Landau–Zener–Stückelberg–Majorana transition in the T2
    :math:`\ll` T1 limit", *J. Magn. Reson.*, **2023**, *354*, 107523
    [`10.1016/j.jmr.2023.107523 <http://doi.org/10.1016/j.jmr.2023.107523>`__].


Experiment Summary
------------------------

.. autosummary:: 

    mrfmsim.experiment.CermitTDGroup
    mrfmsim.formula.polarization.rel_dpol_sat_td
    mrfmsim.formula.polarization.rel_dpol_sat_td_smallsteps

.. autodata:: mrfmsim.experiment.CermitTDGroup
.. group:: mrfmsim.experiment.CermitTDGroup
