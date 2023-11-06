#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrfmsim.component import Sample
from textwrap import dedent


def test_Sample_str():
    """Tests sample str representation without units."""

    sample = Sample(spin="1H", T1=1e-6, T2=5e-6, spin_density=49.0, temperature=4.2)

    sample_str = """\
    Sample(spin=1H
    \tT1=1.000e-06 s
    \tT2=5.000e-06 s
    \ttemperature=4.200 K
    \tspin_density=49.000 1/nm^3
    \tGamma=2.675e+05 rad/(s.mT)
    \tJ=0.5
    \tdB_hom=0.748 mT
    \tdB_sat=1.672 mT)"""

    assert str(sample) == dedent(sample_str)
