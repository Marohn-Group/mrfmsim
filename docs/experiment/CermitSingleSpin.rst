CERMIT single spin
==================

Overview
--------

The experiments calculate the effective force on a cantilever from a single electron spin located directly below a magnet-tipped cantilever in the "hangdown" and SPAM geometries. 
There are two experiments in the group: cantilever spring constant shift calculated using the Trapezoid rule ("CermitSingleSpinApprox"), and cantilever spring constant shift calculated directly using elliptic integrals ("CermitSingleSpin"). 
The exact solution only works for spin directly under a **spherical** magnet. The experiments are adopted from Section 3.5 of Eric Moore's dissertation. [#Moore2011Sep]_


.. [#Moore2011Sep] Moore, E. W, and Marohn, J. A. "1. Mechanical Detection Of Electron Spin Resonance From Nitroxide Spin Probes, 2. Ultrasensitive Cantilever Torque Magnetometry Of Magnetization Switching In Individual Nickel Nanorods". Dissertation. Cornell, 2011.

Experiment Summary
-----------------------

.. autosummary::

    mrfmsim.experiment.CermitSingleSpinGroup

.. autodata:: mrfmsim.experiment.CermitSingleSpinGroup
.. group:: mrfmsim.experiment.CermitSingleSpinGroup
