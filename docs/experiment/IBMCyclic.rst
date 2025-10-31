IBM cyclic
=====================

Overview
---------------------


A number of methods have been devised for detecting spin magnetic resonance 
using a cantilever. The methods are different enough that numerically 
calculating the effect of the spins on the cantilever requires a distinct 
approach for each method. We are most interested in simulating the signal from 
Degen *et al.* [#Degen2009jan]_ and Longenecker *et al.* [#Longenecker2012oct]_
experiments.

In these experiments, adiabatic rapid passages were used to repeatedly invert 
the sample's spin magnetization in time with the natural oscillation period of 
the cantilever. The modulated spin magnetization interacted with a magnetic 
field gradient to produce a resonant force that excited the cantilever. The 
cantilever position was observed with a lock-in detector; spin resonance was 
registered as a change in the *amplitude* of the cantilever oscillation. In 
the experiments cited above, the number of spins in resonance was so small 
that the spin fluctuations exceeded the average thermal spin polarization. In 
this small-ensemble limit, nuclear magnetic resonance (NMR) was detected as a 
change in the *variance* of the cantilever position fluctuations observed in 
the in-phase channel of the lock-in detector.

The net polarization between spin-up and spin-down fluctuates on the same time
scale as the random spin-flip rate. For a random ensemble of spin-1/2 nuclei with
a small mean polarization, the variance of the net polarization :math:`\Delta N`
is :math:`\sigma^2_{\Delta N} = N`, where :math:`N` is the total number of spins.
The standard deviation of such statistical polarization far exceeds the Boltzmann
polarization in a small detection volume. In this limit, the variance can be used
as the MRFM signal. For :math:`n` independent configurations of the spin ensemble,
the sample variance :math:`s^2_{\Delta N}` is

.. math::
    s^2_{\Delta N} = \frac{1}{n-1} \sum^n_{j=1} (\Delta N_j - \overline{\Delta N})^2


where :math:`\overline{\Delta N}` is the Boltzmann polarization.
The standard error of the variance is 

.. math::
    \sigma_{s^2_{\Delta N}} = \sqrt{\frac{2}{n-1}} \sigma^2_{\Delta N}
    \approx \sqrt{\frac{2}{n-1}} N.

The signal-to-noise ratio of the variance signal, in the approximation that no
other noise is present, is

.. math::
    \mathrm{SNR} = \frac{s^2_{\Delta N}}{\sigma_{s^2_{\Delta N}}} = \sqrt{\frac{n-1}{2}}.

Numerically, we can simulate the signal from the three-dimensional convolution integral,

.. math::
    \sigma^2_\mathrm{spin}(\boldsymbol{r}_s) = \int_\mathrm{sv} d^3(\boldsymbol{r})K(\boldsymbol{r}_s - 
    \boldsymbol{r})\rho(\boldsymbol{r})

.. math::

    K(\boldsymbol{r}) = A \mu_\mathrm{p}^2\left(\frac{\partial B_z^\mathrm{tip}}{\partial x}\right)^2\eta
    (\Delta B_0(\boldsymbol{r}))

.. math::
    \Delta B_0(\boldsymbol{r}) = B_0 + B^\mathrm{tip}(\boldsymbol{r}) - 2\pi
    \frac{f_\mathrm{rf}}{\gamma_\mathrm{p}}

where :math:`\sigma^2_\mathrm{spin}` is the force variance, :math:`\boldsymbol{r}_s`
is the tip position, :math:`K` is the point spread function related to the resonance
slice, :math:`A` is a scaling factor, :math:`\rho` is the proton density of the sample,
:math:`\mu_\mathrm{p} = 1.4 \times 10^{26}` J/T is the proton magnetic moment,
:math:`\eta (\Delta B_0(\boldsymbol{r}))` is a function that characterizes the off-resonance
spin response, :math:`\gamma_\mathrm{p}/2 \pi = 42.56` MHz/T is the proton gyromagnetic ratio,
:math:`B_0` is an external magnetic field, and :math:`B^\mathrm{tip}(\boldsymbol{r})` is the tip field. 
For the cyclic inversion protocol with the triangle-wave frequency, the off-resonance response
is well approximated by [#Longenecker2012oct]_

.. math::


    \eta (\Delta B_0(\boldsymbol{r}))=
    \begin{cases} 
      \cos^2{\left(\dfrac{\gamma_\mathrm{p}\Delta B_0(\boldsymbol{r})}{2\Delta f_\mathrm{FM}}\right)}
      & \mathrm{for}\; \Delta B_0(\boldsymbol{r}) \leq \pi \Delta f_\mathrm{FM}/\gamma_\mathrm{p}\\
      0 & \mathrm{otherwise}. \\
   \end{cases}

where :math:`\Delta f_\mathrm{FM}` is the peak-to-peak frequency modulation deviation.

**Reference**

.. [#Degen2009jan] Degen, C. L.; Poggio, M.; Mamin, H. J.; Rettner, C. T. & 
    Rugar, D. "Nanoscale Magnetic Resonance Imaging", *Proc. Natl. Acad. Sci. 
    U.S.A.*, **2009**, *106*, 1313 - 1317
    [`10.1073/pnas.0812068106 <http://dx.doi.org/10.1073/pnas.0812068106>`__].

.. [#Longenecker2012oct] Longenecker, J. G.; Mamin, H. J.; Senko, A. W.; Chen, 
    L.; Rettner, C. T.; Rugar, D. & Marohn, J. A. "High-Gradient Nanomagnets 
    on Cantilevers for Sensitive Detection of Nuclear Magnetic Resonance", 
    *ACS Nano*, **2012**, *6*, 9637 - 9645 
    [`10.1021/nn3030628 <http://dx.doi.org/10.1021/nn3030628>`__].

Experiment Summary
----------------------

.. autosummary::

    mrfmsim.experiment.IBMCyclic
    mrfmsim.formula.polarization.rel_dpol_ibm_cyclic

.. autodata:: mrfmsim.experiment.IBMCyclic
.. experiment:: mrfmsim.experiment.IBMCyclic
