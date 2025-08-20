import pytest
import numpy as np
from mrfmsim.component import CylinderMagnet, CylinderMagnetApproxByRect


"""Test CylinderMagnetApproxByRect module in mrfmsim.component.


CylinderMagnet & CylinderMagnetApproxByRect
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
        self.magnet = CylinderMagnet(
            magnet_radius=0.5, magnet_length=10, magnet_origin=[0, 0, 0], mu0_Ms=1
        )
        self.magnet_approx = CylinderMagnetApproxByRect(
            magnet_radius=0.5, magnet_length=10, magnet_origin=[0, 0, 0], mu0_Ms=1
        )

    # test the shape of the magnetic field
    def test_Bz_shape(self):
        '''Test the shape of the magnetic field Bz to be the same as the input grid'''
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bz = self.magnet_approx.Bz_method(grid[0], grid[1], grid[2])
        assert Bz.shape == (2, 5, 10)

    def test_Bzx_shape(self):
        '''Test the shape of the magnetic field Bzx to be the same as the input grid'''
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bzx = self.magnet_approx.Bzx_method(grid[0], grid[1], grid[2])
        assert Bzx.shape == (2, 5, 10)

    def test_Bzxx_shape(self):
        '''Test the shape of the magnetic field Bzxx to be the same as the input grid'''
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bzxx = self.magnet_approx.Bzxx_method(grid[0], grid[1], grid[2])
        assert Bzxx.shape == (2, 5, 10)

    # test the symmetry of the magnetic field
    def test_Bz_symmetry(self):
        '''Test the x-axis symmetry of the magnetic field Bz'''
        Bz1 = self.magnet_approx.Bz_method(1, 2, 6)
        Bz2 = self.magnet_approx.Bz_method(-1, 2, 6)
        assert np.allclose(Bz1, Bz2)

    def test_Bzx_symmetry(self):
        '''Test the x-axis antisymmetry of the magnetic field Bzx'''
        Bzx1 = self.magnet_approx.Bzx_method(1, 2, 6)
        Bzx2 = self.magnet_approx.Bzx_method(-1, 2, 6)
        assert np.allclose(Bzx1, -Bzx2)  # Bzx is antisymmetric

    def test_Bzxx_symmetry(self):
        '''Test the x-axis symmetry of the magnetic field Bzxx'''
        Bzxx1 = self.magnet_approx.Bzxx_method(1, 2, 6)
        Bzxx2 = self.magnet_approx.Bzxx_method(-1, 2, 6)
        assert np.allclose(Bzxx1, Bzxx2)  # Bzxx is symmetric

    # test the value of the magnetic field
    def test_Bz_NearField(self):
        '''Test the near field of the magnetic field Bz to be close to the exact value'''
        grid = np.ogrid[-3:3:10j, -3:3:10j, 6:7:2j]
        Bz_approx = self.magnet_approx.Bz_method(grid[0], grid[1], grid[2])
        Bz_exact = self.magnet.Bz_method(grid[0], grid[1], grid[2])
        assert np.allclose(Bz_approx, Bz_exact, rtol=1e-3)

    def test_Bzx_NearField(self):
        '''Test the near field of the magnetic field Bzx to be close to the exact value'''
        grid = np.ogrid[-3:3:10j, -3:3:10j, 6:7:2j]
        Bzx_approx = self.magnet_approx.Bzx_method(grid[0], grid[1], grid[2])
        Bzx_exact = self.magnet.Bzx_method(grid[0], grid[1], grid[2])
        assert np.allclose(Bzx_approx, Bzx_exact, rtol=1e-3)

    def test_Bzxx_NearField(self):
        '''Test the near field of the magnetic field Bzxx to be close to the exact value'''
        grid = np.ogrid[-3:3:10j, -3:3:10j, 6:7:2j]
        Bzxx_approx = self.magnet_approx.Bzxx_method(grid[0], grid[1], grid[2])
        Bzxx_exact = self.magnet.Bzxx_method(grid[0], grid[1], grid[2])
        assert np.allclose(Bzxx_approx, Bzxx_exact, rtol=1e-3)

    def test_Bz_FarField(self):
        '''Test the far field of the magnetic field Bz to be close to the exact value'''
        grid = np.ogrid[-13:-10:10j, -1:2:10j, 6:7:2j]
        Bz_approx = self.magnet_approx.Bz_method(grid[0], grid[1], grid[2])
        Bz_exact = self.magnet.Bz_method(grid[0], grid[1], grid[2])
        assert np.allclose(Bz_approx, Bz_exact, atol=1e-4)

    def test_Bzx_FarField(self):    
        '''Test the far field of the magnetic field Bzx to be close to the exact value'''
        grid = np.ogrid[-13:-10:10j, -1:2:10j, 6:7:2j]
        Bzx_approx = self.magnet_approx.Bzx_method(grid[0], grid[1], grid[2])
        Bzx_exact = self.magnet.Bzx_method(grid[0], grid[1], grid[2])
        assert np.allclose(Bzx_approx, Bzx_exact, atol=1e-6)

    def test_Bzxx_FarField(self):
        '''Test the far field of the magnetic field Bzxx to be close to the exact value'''
        grid = np.ogrid[-13:-10:10j, -1:2:10j, 6:7:2j]
        Bzxx_approx = self.magnet_approx.Bzxx_method(grid[0], grid[1], grid[2])
        Bzxx_exact = self.magnet.Bzxx_method(grid[0], grid[1], grid[2])
        assert np.allclose(Bzxx_approx, Bzxx_exact, atol=1e-6)


    # test the when x is 0, Bzx is 0
    def test_Bzx_when_x_is_0(self):
        '''Test the magnetic field Bzx when x is 0 to be 0'''
        Bzx = self.magnet_approx.Bzx_method(0, 10, 0)
        assert np.allclose(Bzx, 0, atol=1e-10)
