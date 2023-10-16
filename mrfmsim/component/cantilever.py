#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class Cantilever:
    """cantilever object."""

    def __init__(self, k_c, f_c):
        """Initialize cantilever.
    
        :param float k: spring constant [nN/m]
        :param float f: mechanical resonance freq [mHz]
        """
        self.k_c = k_c
        self.f_c = f_c

    def dk_to_df_modulated(self, dk_spin):
        """Converting spring constant to the modulated square wave frequency RMS.
        
        The primary Fourier component of a square wave is 4/pi.
        You lose a factor of two because you modulate between 1 and 0 and
        not 1 and -1. The final factor :math:`1/sqrt(2)` is the RMS value
        of the signal.
        """
        return dk_spin * self.f_c / (self.k_c * np.pi * np.sqrt(2))

    def dk_to_df(self, dk_spin):
        """Convert spring constant to the frequency."""
        return dk_spin * self.f_c / (2 * self.k_c)
