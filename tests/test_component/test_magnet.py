#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test magnet module in mrfmsim.component.

SphereMagnet
------------

All sphere magnets are tested using the parameters:
radius = 50.0 nm
mu0_Ms = 1800.0 mT
origin = [0, 0, 0] nm

Bz_method
^^^^^^^^^^

1. Test Bz at poles (0.0, 0.0, 50.0) and (0.0, 0.0, -50.0) both result
   in Bz value of 1200.0 mT
2. Test Bz at the equator (50.0, 0.0, 0.0), (0.0, 5.0, 0.0), 
   and (-1.0*50.0/sqrt(2),  -1.0*50.0/sqrt(2), 0.0), all result in Bz
   value of -600.0 mT
"""

import pytest
import numpy as np
from mrfmsim.component import SphereMagnet, RectangularMagnet
from textwrap import dedent


class MagnetTester:
    """Base class for testing magnet classes."""

    magnet_str = ""

    def test_str(self, magnet):
        """Test magnet str."""

        assert str(magnet) == dedent(self.magnet_str)

    def check_bz(self, magnet, x, y, z, theory):
        """Test Bz calculation against the theory."""
        assert np.allclose(magnet.Bz_method(x, y, z), theory, rtol=1e-12)

    def check_bzx(self, magnet, x, y, z):
        """test Bzx at selected points against estimation from Bz calculation."""

        dx = 0.001

        Bzx_est = (
            magnet.Bz_method(x + 0.5 * dx, y, z) - magnet.Bz_method(x - 0.5 * dx, y, z)
        ) / dx
        Bzx_sim = magnet.Bzx_method(x, y, z)

        assert np.allclose(Bzx_est, Bzx_sim, rtol=1e-9)

    def check_bzxx(self, magnet, x, y, z):
        """test Bzxx at selected points against estimation from Bzx calculation."""

        dx = 0.001

        Bzxx_est = (
            magnet.Bzx_method(x + 0.5 * dx, y, z)
            - magnet.Bzx_method(x - 0.5 * dx, y, z)
        ) / dx
        Bzxx_sim = magnet.Bzxx_method(x, y, z)

        assert np.allclose(Bzxx_est, Bzxx_sim, rtol=1e-9)


class TestSphereMagnet(MagnetTester):
    """Test SphereManget class."""

    magnet_str = """\
    SphereMagnet
      magnet_radius = 50.0 nm
      magnet_origin = [0.0, 0.0, 0.0] nm
      mu0_Ms = 1800.000 mT"""

    @pytest.fixture
    def magnet(self):
        """Instantiate a SphereManget instance."""
        return SphereMagnet(magnet_radius=50.0, magnet_origin=[0.0, 0.0, 0.0], mu0_Ms=1800.0)

    @pytest.mark.parametrize(
        "x, y, z, theory",
        [
            # at poles
            (0.0, 0.0, 50.0, 1200.0),
            (0.0, 0.0, -50.0, 1200.0),
            # at equators
            (50.0, 0.0, 0.0, -600.0),
            (0.0, 50.0, 0.0, -600.0),
            (-1.0 * 50.0 / np.sqrt(2), -1.0 * 50.0 / np.sqrt(2), 0.0, -600.0),
        ],
    )
    def test_bz(self, magnet, x, y, z, theory):
        """Test Bz calculation at poles and equators."""

        self.check_bz(magnet, x, y, z, theory)

    @pytest.mark.parametrize(
        "x, y, z",
        [
            (57.29, 0.0, 0.0),  # at equator
            (10.91, 13.16, 53.18),  # near north pole
        ],
    )
    def test_bzx(self, magnet, x, y, z):
        """Test Bzx at selected points against estimation from Bz calculation."""

        self.check_bzx(magnet, x, y, z)

    @pytest.mark.parametrize(
        "x, y, z",
        [
            (57.29, 0.0, 0.0),  # at equator
            (10.91, 13.16, 53.18),  # near north pole
        ],
    )
    def test_bzxx(self, magnet, x, y, z):
        """Test Bzxx at selected points against estimation from Bzx calculation."""

        self.check_bzxx(magnet, x, y, z)


class TestRectangularMagnet(MagnetTester):
    """Tests RectangularMagnet."""

    magnet_str = """\
    RectangularMagnet
      magnet_length = [40.0, 60.0, 100.0] nm
      magnet_origin = [0.0, 0.0, 0.0] nm
      mu0_Ms = 1800.000 mT"""

    @pytest.fixture
    def magnet(self):
        """Instantiate a RectangularManget instance."""

        return RectangularMagnet(
            magnet_length=[40.0, 60.0, 100.0],
            magnet_origin=[0.0, 0.0, 0.0],
            mu0_Ms=1800.0,
        )

    @pytest.mark.parametrize("x, y, z", [(np.arange(50, 100, 5), 100, 100)])
    def test_rectmagnet_x_symmetry(self, magnet, x, y, z):
        """Test x direction symmetry

        Bz - even function in the x direction
        Bzx - odd function in the x direction
        Bzxx - even function in the x direction
        """

        assert np.allclose(
            magnet.Bz_method(x, y, z), magnet.Bz_method(-x, y, z), rtol=1e-10
        )
        assert np.allclose(
            magnet.Bzx_method(x, y, z), -magnet.Bzx_method(-x, y, z), rtol=1e-10
        )
        assert np.allclose(
            magnet.Bzxx_method(x, y, z), magnet.Bzxx_method(-x, y, z), rtol=1e-10
        )

    @pytest.mark.parametrize("x, y, z", [(0.0, 0.0, np.arange(50, 100, 5))])
    def test_rectmagnet_Bz_symmetry_z(self, magnet, x, y, z):
        """Test Bz_method of RectMagnet symmetry in the z direction."""

        np.allclose(magnet.Bz_method(x, y, z), magnet.Bz_method(x, y, -z), rtol=1e-10)

    def test_rectmagnet_Bz(self):
        """Test the rectangular magnet based on the numeric simulation.

        If we treat the magnet as a square loop wire, the magnetization
        at z distance away from the magnet's center can be calculated using
        Biot-Savart law. We use this measurement against a thin film magnet
        with the size of 10, 10, and 1 nm, and calculate the field 2 nm away
        from the center of the magnet. (The unit of B is mT)
        """
        magnet = RectangularMagnet(
            magnet_length=[10.0, 10.0, 1.0], mu0_Ms=1800.0, magnet_origin=[0.0, 0.0, 0.0]
        )
        assert np.allclose(magnet.Bz_method(0, 0, 2), 134.23, rtol=1e-2)

    @pytest.mark.parametrize("x, y, z", [(np.arange(100, 150, 5), -100, 100)])
    def test_rectmagnet_Bzx(self, magnet, x, y, z):
        """Test Bzx_method by using against the gradient of bz."""

        self.check_bzx(magnet, x, y, z)

    @pytest.mark.parametrize("x, y, z", [(np.arange(100, 150, 5), -100, 100)])
    def test_rectmagnet_Bzxx(self, magnet, x, y, z):
        """Test the Bzxx_method of RectMagnet against the derivative Bzx_method."""

        self.check_bzxx(magnet, x, y, z)
