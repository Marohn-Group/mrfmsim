#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from mrfmsim.component import Sample
import pytest

SAMPLE_REPR = """Sample(
  dB_hom=7.476e-01 [mT] # homogenous linewidth
  dB_sat=5.286e-04 [mT] # saturation linewidth
  f_larmor=4.258e+07 [Hz] # larmor frequency
  Gamma=2.675e+05 [rad/s.mT] # gyromagnetic ratio
  J=0.5 # total spin angular momentum
  mu_z=0.014 [aN.nm/mT] # equilibrium per spin magnetization
  mz2_eq=1.990e-04 [aN^2.nm^2/mT^2] # magnetization variance per spin
  spin_density=49.000 [nm^-3] # spin density
  spin_type=1H
  T1=1.000e+01 [s] # spin-lattice relaxation
  T2=5.000e-06 [s] # spin-spin relaxation
  temperature=4.200 [K] # temperature
)"""


class TestSample:
    """Tests to prove that Sample is getting set up correctly."""

    @pytest.fixture
    def sample(self):
        return Sample(
            spin_type="1H", T1=10, T2=5e-6, spin_density=49.0, temperature=4.2
        )

    # def test_str(self, sample):
    #     """Tests sample str representation."""
    #     assert str(sample) == SAMPLE_REPR

    def test_proton_magnetic_moment(self, sample):
        """Cross check magnetic moment"""

        hbar = 1.054571628e-7
        mu_p = hbar * sample.Gamma / 2.0

        assert np.isclose(mu_p, 0.0141, rtol=2e-3)
