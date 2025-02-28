CERMIT protocol
========================

In Garner *et al.* [#Garner2004jun]_ and Moore *et al.* [#Moore2009dec]_ 
experiments spin magnetization, interacted with the second derivative of a 
magnetic field to produce a change in the cantilever's *frequency* of 
oscillation. This approach to detecting magnetic resonance was termed the 
CERMIT protocol, which stands for Cantilever-Enabled Readout of Magnetization 
Inversion Transients. 

In the Garner experiment, [#Garner2004jun]_ nuclear spin magnetization was 
inverted once using a swept-frequency adiabatic rapid passage, and the 
resulting step-change in the cantilever frequency indicated nuclear spin 
resonance (NMR). In the Moore experiment, [#Moore2009dec]_ electron spin 
magnetization was modulated slowly by switching the spin-saturating 
microwaves on and off periodically. The cantilever oscillation was digitized 
and sent to a (software) frequency demodulator. The resulting 
frequency-versus-time data was fed to a (software) lock-in detector, operated 
with the microwave modulation trigger as the reference signal. A change in the 
lock-in output indicated electron spin resonance (ESR).  

To observe a change in the cantilever frequency, the cantilever in these 
experiments were driven into self-oscillation. In the presence of the tip field 
gradient, the motion of the cantilever led to a dithering of the resonance 
frequency of the spins in the sample. In the Moore experiment, [#Moore2009dec]_
microwave irradiation was applied at a fixed frequency, and this dithering was 
used to sweep out a region of saturated electron spins below the tip. In the 
Garner experiment, [#Garner2004jun]_ in contrast, the region of inverted 
magnetization swept out by the dithering of the tip was much smaller than the 
region of inverted spin magnetization created by sweeping the frequency of the 
applied radio frequency field.

In experiments like these involving a driven cantilever, the observed 
frequency shift depends on the amplitude of the cantilever oscillation and 
different equations are needed to calculate the spin signal in small-amplitude 
and large-amplitude limits. A unified set of equations describing 
frequency-shift experiments were derived from first principles; [#Lee2012apra]_ 
those results are summarized below.

In this package, we implement in Python the protocol for calculating the 
dc-NMR-CERMIT signal outlined in the Garner *et al.* manuscript
[#Garner2004jun]_ and the protocol for calculating the ac-ESR-CERMIT signal 
outlined in the supporting information of the Moore *et al.* manuscript. 
[#Moore2009dec]_ 


.. [#Garner2004jun] Garner, S. R.; Kuehn, S.; Dawlaty, J. M.; Jenkins, N. E. &
    Marohn, J. A.  "Force-Gradient Detected Nuclear Magnetic Resonance" *Appl. 
    Phys. Lett.*, **2004**, *84*, 5091 - 5093
    [`10.1063/1.1762700 <http://dx.doi.org/10.1063/1.1762700>`__].

.. [#Moore2009dec] Moore, E. W.; Lee, S.-G.; Hickman, S. A.; Wright, S. J.; 
    Harrell, L. E.; Borbat, P. P.; Freed, J. H. & Marohn, J. A. "Scanned-Probe 
    Detection of Electron Spin Resonance from a Nitroxide Spin Probe", *Proc. 
    Natl. Acad. Sci. U.S.A.*, **2009**, *106*, 22251 - 22256 
    [`10.1073/pnas.0908120106 <http://doi.org/10.1073/pnas.0908120106>`__].

.. [#Lee2012apra] Lee, S.-G.; Moore, E. W. & Marohn, J. A. "A Unified Picture 
    of Cantilever Frequency-Shift Measurements of Magnetic Resonance", 
    *Phys. Rev. B*, **2012**, *85*, 165447 
    [`10.1103/PhysRevB.85.165447 <http://doi.org/10.1103/PhysRevB.85.165447>`__].  
