#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrfmsim.component import Sample
from textwrap import dedent


def test_sample_str():
    """Tests sample str representation without units."""

    sample = Sample(spin="1H", T1=1e-6, T2=5e-6, spin_density=49.0, temperature=4.2)

    sample_str = """\
    Sample
      spin = '1H'
      T1 = 1.000e-06 s
      T2 = 5.000e-06 s
      temperature = 4.200 K
      spin_density = 49.000 1/nm^3
      Gamma = 2.675e+05 rad/(s.mT)
      J = 0.5
      dB_hom = 0.748 mT
      dB_sat = 1.672 mT"""

    assert str(sample) == dedent(sample_str)
