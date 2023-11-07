#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from dataclasses import dataclass, field
from mrfmsim.component import ComponentBase


@dataclass
class Cantilever(ComponentBase):
    """Cantilever object.

    :param float k: spring constant [aN/nm]
    :param float f: mechanical resonance frequency [Hz]
    """

    k_c: float = field(metadata={"unit": "aN/nm", "format": ".3e"})
    f_c: float = field(metadata={"unit": "Hz", "format": ".3e"})
    k2f_modulated: float = field(
        init=False, repr=False, metadata={"unit": "Hz.nm/aN", "format": ".3e"}
    )
    k2f: float = field(init=False, repr=False, metadata={"unit": "Hz.nm/aN", "format": ".3e"})

    def __post_init__(self):
        self.k2f_modulated = self.f_c / (self.k_c * np.pi * np.sqrt(2))
        self.k2f = self.f_c / (2 * self.k_c)

    # def dk_to_df_modulated(self, dk_spin):
    #     """Convert spring constant to the modulated square wave frequency RMS.

    #     The primary Fourier component of a square wave is 4/pi.
    #     You lose a factor of two because you modulate between 1 and 0 and
    #     not 1 and -1. The final factor :math:`1/sqrt(2)` is the RMS value
    #     of the signal.
    #     """
    #     return dk_spin * self.f_c / (self.k_c * np.pi * np.sqrt(2))

    # def dk_to_df(self, dk_spin):
    #     """Convert spring constant to the frequency."""
    #     return dk_spin * self.f_c / (2 * self.k_c)
