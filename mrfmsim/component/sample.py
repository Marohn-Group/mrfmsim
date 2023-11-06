#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from dataclasses import dataclass, field
from mrfmsim.component import ComponentBase

spin_dict = {
    # note: not accounting for the g-factor of the electron spin;
    "e": {"Gamma": 1.760859708e8, "J": 0.5},  # rad/s.mT
    "1H": {"Gamma": 2.675222005e05, "J": 0.5},  # rad/s.mT
    "71Ga": {"Gamma": 2.0 * np.pi * 12.98e3, "J": 1.5},  # rad/s.mT
    "19F": {"Gamma": 2.0 * np.pi * 40.05e3, "J": 0.5},  # rad/s.mT
    "2H": {"Gamma": 2.0 * np.pi * 6.536e3, "J": 1.0},  # rad/s.mT
}


@dataclass
class Sample(ComponentBase):
    r"""Sample object for magnetic resonance force microscopy experiments.

    For spins 'e', '1H', '71Ga', '19F', or '2H' the Gamma and J are preset.
    For other spins, input the name, Gamma and J directly.

    :param str spin: spin type
    :param float T1: spin-lattice relaxation :math:`T_1` [s]
    :param float T2: spin-spin relaxation :math:`T_2` [s]
    :param float temperature: the sample temperature [K]
    :param float spin_density: the sample spin density :math:`\rho` [1/nm^3]
    :param float Gamma: spin gyromagnetic ratio [rad/s.mT]
        defaults to None if spin_type is one of the preset
    :param float L: spin angular momentum [unitless]
        default to None if spin_type is one of the preset
    :param float dB_hom: homogeneous linewidth [mT]
    :param float dB_sat: saturation linewidth [mT]
    """

    spin: str
    T1: float = field(metadata={"unit": "s", "format": ".3e"})
    T2: float = field(metadata={"unit": "s", "format": ".3e"})
    temperature: float = field(metadata={"unit": "K"})
    spin_density: float = field(metadata={"unit": "1/nm^3"})
    Gamma: float = field(default=None, metadata={"unit": "rad/(s.mT)", "format": ".3e"})
    J: float = field(default=None, metadata={"format": ".1f"})
    dB_hom: float = field(init=False, default=None, metadata={"unit": "mT"})
    dB_sat: float = field(init=False, default=None, metadata={"unit": "mT"})

    def __post_init__(self):
        self.Gamma = self.Gamma or spin_dict[self.spin]["Gamma"]  # rad/s.mT
        self.J = self.J or spin_dict[self.spin]["J"]
        self.dB_hom = 1 / (self.Gamma * self.T2)  # mT
        self.dB_sat = 1 / (self.Gamma * np.sqrt(self.T1 * self.T2))  # mT


# class Sample:
#     r"""Sample object for magnetic resonance force microscopy experiments.

#     The **Sample** carries the properties of the nuclear or electron
#     spins in the sample.
#     The default spin type includes the properties of
#     'electron', '1H', '2H', '19F', '71Ga'. For spin that is not included
#     simply provide a name for spin, gamma, and j.
#     :cvar float hbar: reduced Plank constant, unit [aN nm s]
#     :cvar float kB: Boltzmann constant [aN nm k:math:'^{-1}']
#     """
#     hbar = 1.054571628e-7  # aN nm s - reduced Plank constant
#     kB = 1.3806504e4  # aN nm K^{-1} - Boltzmann constant

#     _spintype = {
#         # note: not accounting for the g-factor of the electron spin;
#         "electron": {"Gamma": 1.760859708e8, "J": 0.5},  # rad/s.mT
#         "1H": {"Gamma": 2.675222005e05, "J": 0.5},  # rad/s.mT
#         "71Ga": {"Gamma": 2.0 * np.pi * 12.98e3, "J": 1.5},  # rad/s.mT
#         "19F": {"Gamma": 2.0 * np.pi * 40.05e3, "J": 0.5},  # rad/s.mT
#         "2H": {"Gamma": 2.0 * np.pi * 6.536e3, "J": 1.0},  # rad/s.mT
#     }

#     def __init__(
#         self, spin_type, T1, T2, temperature, spin_density, Gamma=None, J=None
#     ):
#         r"""Initialize sample object.

#         The values for the gyromagnetic ratio and total spin angular momentum
#         are populated automatically based on the nucleus.
#         The homogeneous linewidth ``dB_hom`` is defined as
#         .. math::
#             \Delta B_{\text{homog}} = \dfrac{1}{\gamma T_2}.
#         The saturation linewidth ``dB_sat`` is defined as
#         .. math::
#             \Delta B_{\text{sat}} = \dfrac{1}{\gamma \sqrt{T_1 \: T_2}}.

#         The variance in a single spin's magnetization in the low-polarization limit (mz2_eq)
#         is given by [#Xue]_

#         .. math::

#              \sigma_{{\cal M}_{z}}^{2} = \hbar^2 \gamma^2 \dfrac{J \: (J + 1)}{3}


#         :param str spin_type: 'e', '1H', '71Ga', '19F', or '2H'
#         :param float T1: the spin-lattice relaxation time :math:`T_1` [s]
#         :param float T2: spin dephasing time :math:`T_2` [s]
#         :param float spin_density: the sample spin
#             density :math:`\rho` [1/nm^3]; *note the units*
#         :param float Gamma: spin gyromagnetic ratio [rad/s.mT]
#             defaults to None if spin_type is one of the preset
#         :param float J: total spin angular momentum [unitless]
#             default to None if spin_type is one of the preset
#         :ivar float Gamma: gyromagnetic ratio [rad/s.mT]
#         :ivar float dB_hom: the homogeneous linewidth [mT]
#         :ivar float dB_sat: the saturation linewidth [mT]


#         .. [#Xue] Equations 1 and 2 in Xue, F.; Weber, D.; Peddibhotla, P. & Poggio, M.
#         "Measurement of statistical nuclear spin polarization in a nanoscale GaAs sample",
#         *Phys. Rev. B*, **2011**, *84*, 205328
#         [`10.1103/PhysRevB.84.205328 <http://dx.doi.org/10.1103/PhysRevB.84.205328>`__].

#         """

#         self.spin_type = spin_type
#         self.Gamma = Gamma or self._spintype[spin_type]["Gamma"]  # rad/s.mT
#         self.J = J or self._spintype[spin_type]["J"]
#         self.mu_z = self.hbar * self.Gamma * self.J
#         self.T1 = T1
#         self.T2 = T2
#         self.spin_density = spin_density
#         self.dB_hom = 1 / (self.Gamma * self.T2)  # mT
#         self.dB_sat = 1 / (self.Gamma * np.sqrt(self.T1 * self.T2))  # mT
#         self.f_larmor = self.Gamma * 1e3 / (2 * np.pi)
#         self.temperature = temperature

#         # calculate the mz2_eq
#         self.mz2_eq = (
#             self.hbar * self.Gamma * np.sqrt(self.J * (self.J + 1) / 3.0)
#         ) ** 2  # (aN.nm/mT)^2

# unit: str = field(init=False, default=None)

# def __post_init__(self):
#     self.registry = get_unit_registry(**asdict(self))
#     if self.registry is not None:
#         self.unit = self.registry.default_system
