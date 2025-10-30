CERMIT steady-state saturation
==============================

Overview
--------

Spins are subjected to a static magnetic field
:math:`\boldsymbol{B}_0 = B_0 \hat{\boldsymbol{z}}`
and irradiated with an oscillating magnetic field 

.. math::
    B(t) = B_1 \left(\hat{\boldsymbol{x}} \, \cos{\omega t}  
    + \hat{\boldsymbol{y}} \, \sin{\omega t}\right). 
    
In a frame of reference rotating about the :math:`z` axis at angular
frequency :math:`\omega`, the rotating-frame components of spin magnetization
will evolve according to the Bloch equation

.. math::
    \frac{d}{d t} \boldsymbol{M}_\text{R} = \gamma \boldsymbol{M}_{\text{R}}
    \times \boldsymbol{B}_{\text{eff}} + \text{relaxation terms}

with :math:`\times` the vector cross product, :math:`\gamma` the spins's gyromagnetic ratio, and 

.. math::
    \boldsymbol{B}_{\text{eff}} = \underbrace{\left( B_0 - \frac{\omega}{\gamma} 
    \right)}_{\Delta B}  \hat{\boldsymbol{z}} + B_1 \, \hat{\boldsymbol{x}}_{\text{R}}

an effective magnetic field in the rotating frame. Dropping the subscript "R" and adding in
relaxation terms, the Bloch equations in the rotating frame are

.. math::
    \begin{align}
    \dot{M_x}
        & = + \gamma \Delta B \, M_y
        - \frac{M_x}{T_2} \\
    \dot{M_y}
        & = - \gamma \Delta B \, M_x
        + \gamma B_1 \, M_z 
        - \frac{M_y}{T_2} \\
    \dot{M_z}
    & = - \gamma B_1 \, M_y
    + \frac{M_0 - M_z}{T_1}
    \end{align}

with :math:`M_0` the equilibrium magnetization, :math:`T_1` the spin-lattice relaxation time,
:math:`T_2` the spin dephasing time. These equations can be written as a set of three coupled
differential equations of the form


.. math:: 
    :label: eq:x

    \dot{x} = A x + b 
    
with

.. math::
    :label: eq:x-vars

    x = \begin{pmatrix} M_x \\ M_y \\ M_z \end{pmatrix}, \: 
        A = \begin{pmatrix}
    - r_2 & + \Delta & 0 \\
    - \Delta & -r_2 & + \omega_1 \\
    0 & - \omega_1 & -r_1 
    \end{pmatrix}, \text{ and }
    b = \begin{pmatrix} 0 \\ 0 \\ r_1 M_0 \end{pmatrix}.

  
Here :math:`x` is a vector describing the magnetization in the rotating frame.
The magnetic field :math:`B_0` is applied along the :math:`z` axis and so the
equilibrium magnetization :math:`M_0` is also along the :math:`z` axis:
:math:`M_{\mathrm{eq}} = (0, 0, M_0)^{\text{T}}`. We will assume the initial
condition to be 

.. math:: 
    x(0) = \begin{pmatrix} 0 \\ 0 \\ M_{z}(0) \end{pmatrix}.

That is, the magnetization is initially assumed to lie parallel to
the :math:`z` axis. The variables in the above equations are summarized
in the Table below.


======================================== =================================================
 variable                                 description                                     
======================================== =================================================
:math:`x`                                magnetization vector in the rotating frame      
:math:`r_2`                              spin dephasing rate                            
:math:`r_1`                              spin-lattice relaxation rate                    
:math:`B_0`                              longitudinal magnetic field intensity           
:math:`M_0`                              longitudinal equilibrium magnetization          
:math:`B_1`                              transverse oscillating magnetic field intensity 
:math:`\omega`                           transverse oscillating magnetic field frequency 
:math:`\gamma`                           electron spin gyromagnetic ratio                
:math:`T_2 = 1/r_2`                      spin dephasing time                             
:math:`T_1 = 1/r_1`                      spin-lattice relaxation time                    
:math:`\omega_0 = \gamma B_0`            Larmor frequency                                
:math:`\omega_1 = \gamma B_1`            Rabi frequency                                  
:math:`\Delta B = B_0 - \omega/\gamma`   resonance offset in field units                 
:math:`\Delta = \omega_0 - \omega`       resonance offset in frequency units             
======================================== =================================================

Variables appearing in eqs. :eq:`eq:x`, :eq:`eq:x-vars`, and subsequent equations. 
The magnetic field :math:`B_0` is applied along the :math:`z` axis,
and the equilibrium magnetization :math:`M_0` also lies along the :math:`z` axis.

Steady-state solution
---------------------

The steady-state solution to eq. :eq:`eq:x` is obtained by setting :math:`\dot{x} = 0` and solving for :math:`x`. The result is :math:`x_{\mathrm{ss}} = - A^{-1} \, b` Computing the :math:`A^{-1}` matrix analytically, substituting this result and :math:`b` into the above equation, and writing the result in terms of the variables :math:`T_1 = 1/r_1` and :math:`T_2 = 1/r_2`, we obtain the following three components of the steady-state magnetization. Let us write the components in a number of equivalent, useful forms. 

.. math::
    :label: eq:Mzss-closed-form

    \begin{aligned}
    \frac{M_x^{\mathrm{ss}}}{M_0}  & = 
    \frac{r_1 \omega_1 \Delta}{r_1 r_2^2 + r_2 \omega_1^2 + r_1 \Delta^2}  
    = \frac{T_2^2 \, \omega_1 \Delta}{1 + T_1 T_2 \, \omega_1^2 + T_2^2 \Delta^2}  
    = \sqrt{\frac{T_2}{T_1}} \frac{S \, \Omega}{1 + S^2 + \Omega^2} \\
    \frac{M_y^{\mathrm{ss}}}{M_0} &= \frac{r_1 r_2 \omega_1}{r_1 r_2^2 + r_2 \omega_1^2 
        + r_1 \Delta^2}  
    = \frac{T_2 \, \omega_1}{1 + T_1 T_2 \, \omega_1^2  + T_2^2\Delta^2} 
    = \sqrt{\frac{T_2}{T_1}} \frac{S}{1 + S^2 + \Omega^2} \\
    \frac{M_z^{\mathrm{ss}}}{M_0} &= \frac{r_1 r_2^2 + r_1 \Delta^2}{r_1 r_2^2 + r_2 \omega_1^2 
        + r_1 \Delta^2}  
    = \frac{1 + T_2^2 \, \Delta^2}{1 + T_1 T_2 \, \omega_1^2 + T_2^2 \, \Delta^2}
    = \frac{1 + \Omega^2}{1 + S^2 + \Omega^2}
    \end{aligned}

These equations are exact and valid both on and off-resonance. In the last form, we have written the magnetization
in terms of a unitless saturation parameter
 
.. math::
    S \equiv \omega_1 \sqrt{T_1 T_2} = \gamma B_1 \sqrt{T_1 T_2}
    
and unitless resonance offset 

.. math::
    :label: eq:Omega-defn

    \Omega \equiv T_2 \Delta = T_2 (\gamma B_0 - \omega).


Our laboratory's magnetic resonance force microscope (MRFM) experiments detect :math:`M_z`. The expression for the :math:`z` component of the steady-state magnetization is especially simple on-resonance:

.. math::
    
    M_z^{\mathrm{ss}}(\Omega = 0) = \frac{1}{1 + S^2} M_0.

In our experiments we detect the change in the :math:`z` magnetization :math:`\Delta M_z = M_z(\text{final}) - M_z(\text{initial})` with :math:`M_z(\text{initial}) = M_0` the thermal-equilibrium magnetization and :math:`M_z(\text{final}) = M_z^{\mathrm{ss}}` the steady-state magnetization in the presence of irradiation. Using the above expressions, we compute 

.. math::
    \Delta M_z 
    = - M_0 \frac{S^2}{1 + S^2 + \Omega^2}
    = - M_0 \frac{S^2}{1 + S^2}
    \frac{1}{1 + \left( 
            \Omega \big/ \sqrt{1+S^2} 
    \right)^2}

The signal on resonance approaches :math:`-M_0` for :math:`S \gg 1`, *i.e.*, in the saturation limit. The signal is largest on resonance and has a Lorentzian dependence on the resonance offset parameter :math:`\Omega`. Expressed in terms of the magnetic field, the width of this Lorentzian is

.. math::
    \Delta B = \frac{1}{\gamma T_2} \sqrt{1+S^2}
    \approx \frac{S}{\gamma T_2}
  
with the approximation valid when :math:`S \gg 1`. When the irradiation intensity is low, :math:`S \ll 1` and :math:`\Delta B \approx 1/(\gamma T_2) = B_{\mathrm{homog}}`, the homogeneous linewidth. When the irradiation intensity is high, then the signal linewidth becomes :math:`\Delta B \approx S/(\gamma T_2)`, :math:`S` times larger than the homogenous linewidth. To see an appreciable signal requires :math:`S > 1`, which necessarily broadens the linewidth.

In a magnetic resonance force microscope (MRFM) experiment, the resonance offset is spatially dependent due to the presence of the magnetic field gradient provided by the cantilever's magnetic tip. Consider spins at a distance :math:`z_0` from the center of the magnetic tip. Expand the magnetic field in a Taylor series in :math:`z` about the point :math:`z_0` and plug the resulting expression into eq. :eq:`eq:Omega-defn` to obtain 

.. math::
    \Omega \approx\gamma T_2 \left(
        B_0(z_0) - \frac{\omega}{\gamma}
        + G_{zz} (z - z_0)
    \right)
    
with :math:`G_{zz} \equiv \frac{\partial B_z}{\partial z}(z_0)`. For simplicity, we are neglecting the dependence of the field :math:`B_0` on :math:`x` and :math:`y`. We are also implicitly assuming that the cantilever is not moving appreciably. Suppose that we have set the irradiation frequency so that spins at a distance :math:`z_0` are in resonance; then :math:`B_0(z_0) - \omega \big/ \gamma = 0` and :math:`\Omega \approx \gamma T_2 G_{zz} (z - z_0)`. With these assumptions, the change in magnetization is 

.. math::
    :label: eq:Mz-vs-z

    \Delta M_z = - M_0 \frac{S^2}{1 + S^2}
    \frac{1}{1 + \left( 
            z^{\prime} \big/ \Delta_z 
    \right)^2}

 
where we have introduced the variables :math:`z^{\prime} = z - z_0` and 

.. math::
    :label: eq:deltaz-defn

    \Delta_z = \frac{\sqrt{1+S^2}}
        {\gamma \, T_2 G_{zz}}
    \approx \frac{S}{\gamma \, T_2 G_{zz}},
  
with the approximation valid when :math:`S \gg 1`, *i.e.*, in the saturation limit. In this limit :math:`\Delta_z` can be written simply as :math:`S B_{\mathrm{homog}}/G_{zz}`. We can see from the above equations that the magnetization will vary over a resonant slice of width :math:`\Delta_z`. This width increases as the irradiation intensity increases and is :math:`\propto B_1` in the saturation limit.

To obtain the force-gradient magnetic resonance signal :math:`\Delta k_{\mathrm{spin}}` we should multiply :math:`\Delta M_z` by the tip field's second derivative :math:`G_{zxx}(\boldsymbol{r})` and the spin density :math:`\rho_{\mathrm{s}}` and integrate the result over space. For simplicity, let us treat the resonant slice as a cylinder of thickness :math:`\Delta_z` and cross-sectional area :math:`A` and let us assume that :math:`G_{zxx}(\boldsymbol{r})` is constant over the resonance slice. Making these approximations and integrating the signal over space gives 

.. math:: 
    \begin{align}
    \Delta k_{\mathrm{spin}} 
    & = -M_0 \frac{S^2}{1 + S^2} \,
    G_{zxx} \, \rho_{\mathrm{s}} \, A
    \int dz^{\prime} 
    \frac{1}
    {1 + (z^{\prime} \big/ \Delta_z)^2} \\
    & = -M_0 \frac{S^2}{1 + S^2} \,
    G_{zxx} \, \rho_{\mathrm{s}} \, A \, \pi \Delta_z  
    \end{align}

where in the second line we have substituted the value of the integral, :math:`\pi \, \Delta_z`. Substituting eq. :eq:`eq:deltaz-defn` for :math:`\Delta z` gives

.. math::
    \Delta k_{\mathrm{spin}} = - \frac{\pi M_0 A \rho_{\mathrm{s}}}{\gamma T_2}
    \frac{G_{zxx}}{G_{zz}} 
    \frac{S^2}{\sqrt{1 + S^2}}

This equation predicts that :math:`\Delta k_{\mathrm{spin}} \propto S` in the :math:`S \gg 1` limit. In this picture, the magnetization saturates yet the signal continues to grow because the width of the sensitive slice continues to increase due to power broadening.

Experiment Summary
-------------------


.. autosummary::

    mrfmsim.experiment.CermitESRGroup
    mrfmsim.formula.polarization.rel_dpol_sat_steadystate

.. autodata:: mrfmsim.experiment.CermitESRGroup
.. group:: mrfmsim.experiment.CermitESRGroup
