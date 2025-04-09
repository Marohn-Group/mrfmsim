import pytest
import numpy as np
from mrfmsim.component import CylinderMagnet


class TestCylinderMagnet:
    def setup_method(self):
        self.magnet = CylinderMagnet(magnet_radius=0.5, magnet_length=10, magnet_origin=[0, 0, 0], mu0_Ms=1)

    def test_Bz_shape(self):
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bz = self.magnet.Bz_method(grid[0], grid[1], grid[2])
        assert Bz.shape == (2, 5, 10)

    def test_Bzx_shape(self):
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bzx = self.magnet.Bzx_method(grid[0], grid[1], grid[2])
        assert Bzx.shape == (2, 5, 10)

    def test_Bzxx_shape(self):
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bzxx = self.magnet.Bzxx_method(grid[0], grid[1], grid[2])
        assert Bzxx.shape == (2, 5, 10)

    def test_Bz_symmetry(self):
        Bz1 = self.magnet.Bz_method(1, 2, 6)
        Bz2 = self.magnet.Bz_method(-1, 2, 6)
        assert np.allclose(Bz1, Bz2)


    def test_Bzx_symmetry(self):
        Bzx1 = self.magnet.Bzx_method(1, 2, 6)
        Bzx2 = self.magnet.Bzx_method(-1, 2, 6)
        assert np.allclose(Bzx1, -Bzx2)

    def test_Bzxx_symmetry(self):
        Bzxx1 = self.magnet.Bzxx_method(1, 2, 6)
        Bzxx2 = self.magnet.Bzxx_method(-1, 2, 6)
        assert np.allclose(Bzxx1, Bzxx2)


    def test_Bz_1(self):
        Bz = self.magnet.Bz_method(1, 2, 6)
        assert np.allclose(Bz, 0.00567438, atol=1e-5)

    def test_Bzx_1(self):
        Bzx = self.magnet.Bzx_method(1, 2, 6)
        assert np.allclose(Bzx, -0.00376482, atol=1e-5)

    def test_Bzxx_1(self):
        Bzxx = self.magnet.Bzxx_method(1, 2, 6)
        assert np.allclose(Bzxx, 0.00545423, atol=1e-5)

    def test_Bz_2(self):
        Bz = self.magnet.Bz_method(10, 0, 0)
        assert np.allclose(Bz, -0.00146935, atol=1e-5)

    def test_Bzx_2(self):
        Bzx = self.magnet.Bzx_method(10, 0, 0)
        assert np.allclose(Bzx, 0.000319819, atol=1e-5)

    def test_Bzxx_2(self):
        Bzxx = self.magnet.Bzxx_method(10, 0, 0)
        assert np.allclose(Bzxx,-0.0000913467, atol=1e-5)

    def test_Bzx_when_x_is_0(self):
        Bzx = self.magnet.Bzx_method(0, 10, 0)
        assert np.allclose(Bzx, 0, atol=1e-10)

        
