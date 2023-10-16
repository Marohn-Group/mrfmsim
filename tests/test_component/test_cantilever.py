#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrfmsim.component import Cantilever
import numpy as np
import pytest


class TestCantilever:
    @pytest.fixture
    def cantilever(self):
        return Cantilever(k_c=7.8e5, f_c=4.975e6)

    def test_dk_to_df_modulate(self, cantilever):
        """Test dk_to_df_modulate conversion."""

        dk = 2.0
        assert np.isclose(cantilever.dk_to_df_modulated(dk), 2.87120)

    def test_dk_to_df(self, cantilever):
        """Test dk_to_df conversion."""

        dk = 2.0
        assert np.isclose(cantilever.dk_to_df(dk), 6.378205)
