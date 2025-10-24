import pytest
import numpy as np
from mrfmsim.component import CylinderMagnet, CylinderMagnetApproxByRect


"""Test CylinderMagnetApproxByRect module in mrfmsim.component.


CylinderMagnetApproxByRect
------------

All sphere magnets are tested using the parameters:
radius = 0.5 nm
length = 10 nm
mu0_Ms = 1 mT
origin = [0, 0, 0] nm

Bz_method
^^^^^^^^^^

1. Test Bz's output has the same shape as the input grid
2. Test Bz's output is symmetric along x-axis
3. Test Bz in the near field is close to the exact value
4. Test Bz in the far field is close to the exact value

Bzx_method
^^^^^^^^^^

1. Test Bzx's output has the same shape as the input grid
2. Test Bzx's output is symmetric along x-axis
3. Test Bzx in the near field is close to the exact value
4. Test Bzx in the far field is close to the exact value
5. Test Bzx when x is 0, Bzx is 0


Bzxx_method
^^^^^^^^^^

1. Test Bzxx's output has the same shape as the input grid
2. Test Bzxx's output is symmetric along x-axis
3. Test Bzxx in the near field is close to the exact value
4. Test Bzxx in the far field is close to the exact value


"""



class TestCylinderMagnet:
    def setup_method(self):
        self.magnet = CylinderMagnetApproxByRect(
            magnet_radius=0.5, magnet_length=10, magnet_origin=[0, 0, 0], mu0_Ms=1
        )

    # test the shape of the magnetic field to be the same as the input grid
    def test_Bz_shape(self):
        '''Test the shape of the magnetic field Bz to be the same as the input grid'''
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bz = self.magnet.Bz_method(grid[0], grid[1], grid[2])
        assert Bz.shape == (2, 5, 10)

    def test_Bzx_shape(self):
        '''Test the shape of the magnetic field Bzx to be the same as the input grid'''
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bzx = self.magnet.Bzx_method(grid[0], grid[1], grid[2])
        assert Bzx.shape == (2, 5, 10)

    def test_Bzxx_shape(self):
        '''Test the shape of the magnetic field Bzxx to be the same as the input grid'''
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bzxx = self.magnet.Bzxx_method(grid[0], grid[1], grid[2])
        assert Bzxx.shape == (2, 5, 10)

    # test the symmetry of the magnetic field along x-axis
    def test_Bz_symmetry(self):
        '''Test the symmetry of the magnetic field Bz along x-axis'''
        Bz1 = self.magnet.Bz_method(1, 2, 6)
        Bz2 = self.magnet.Bz_method(-1, 2, 6)
        assert np.allclose(Bz1, Bz2)

    def test_Bzx_symmetry(self):
        '''Test the symmetry of the magnetic field Bzx along x-axis'''
        Bzx1 = self.magnet.Bzx_method(1, 2, 6)
        Bzx2 = self.magnet.Bzx_method(-1, 2, 6)
        assert np.allclose(Bzx1, -Bzx2)  # Bzx is antisymmetric

    def test_Bzxx_symmetry(self):
        '''Test the symmetry of the magnetic field Bzxx along x-axis'''
        Bzxx1 = self.magnet.Bzxx_method(1, 2, 6)
        Bzxx2 = self.magnet.Bzxx_method(-1, 2, 6)
        assert np.allclose(Bzxx1, Bzxx2)  # Bzxx is symmetric

    # test the value of the magnetic field at poles(1.0, 2.0, 6.0) & (10.0, 0.0, 0.0)
    def test_Bz_1(self):
        '''Test the magnetic field Bz at near field'''
        Bz = self.magnet.Bz_method(1, 2, 6)
        assert np.allclose(Bz, 0.00391404, atol=1e-5)

    def test_Bzx_1(self):
        '''Test the magnetic field Bzx at near field'''
        Bzx = self.magnet.Bzx_method(1, 2, 6)
        assert np.allclose(Bzx, -0.00221805, atol=1e-5)

    def test_Bzxx_1(self):
        '''Test the magnetic field Bzxx at near field'''
        Bzxx = self.magnet.Bzxx_method(1, 2, 6)
        assert np.allclose(Bzxx, 0.0031995877, atol=1e-5)

    def test_Bz_2(self):
        '''Test the magnetic field Bz at far field'''
        Bz = self.magnet.Bz_method(10, 0, 0)
        assert np.allclose(Bz, -0.00044788490737216163, atol=1e-5)

    def test_Bzx_2(self):
        '''Test the magnetic field Bzx at far field'''
        Bzx = self.magnet.Bzx_method(10, 0, 0)
        assert np.allclose(Bzx, 0.00010754599, atol=1e-5)

    def test_Bzxx_2(self):
        '''Test the magnetic field Bzxx at far field'''
        Bzxx = self.magnet.Bzxx_method(10, 0, 0)
        assert np.allclose(Bzxx, -3.22679905171e-05, atol=1e-5)

    # test the when x is 0, Bzx is 0
    def test_Bzx_when_x_is_0(self):
        '''Test the magnetic field Bzx when x is 0'''
        Bzx = self.magnet.Bzx_method(0, 10, 0)
        assert np.allclose(Bzx, 0, atol=1e-10)
