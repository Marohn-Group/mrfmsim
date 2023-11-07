#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrfmsim.component import Cantilever
import numpy as np
import pytest
from textwrap import dedent


@pytest.fixture
def cantilever():
    return Cantilever(k_c=7.8e2, f_c=4.975e6)


def test_Cantilever_str(cantilever):
    """Test the string representation of a cantilever object."""

    cantilever_str = """\
    Cantilever(k_c=7.800e+02 aN/nm
    \tf_c=4.975e+06 Hz
    \tk2f_modulated=1.436e+03 Hz.nm/aN
    \tk2f=3.189e+03 Hz.nm/aN)"""

    assert str(cantilever) == dedent(cantilever_str)


def test_Cantilever_dk_to_df_modulated(cantilever):
    """Test dk_to_df_modulate conversion."""

    dk = 2.0
    assert np.isclose(cantilever.k2f_modulated * dk, 2871.20)


def test_Cantilever_dk_to_df(cantilever):
    """Test dk_to_df conversion."""

    dk = 2.0
    assert np.isclose(cantilever.k2f * dk, 6378.205)
