import numpy as np
from mrfmsim.component import CylinderMagnetApprox


"""Test CylinderMagnet module in mrfmsim.component.


CylinderMagnetApprox
--------------------

All cylinder magnets are tested using the parameters:
radius = 0.5 nm
length = 10 nm
mu0_Ms = 1 mT
origin = [0, 0, 0] nm

Bz_method
^^^^^^^^^^

1. Test Bz output has the same shape as the input grid
2. Test Bz output is symmetric along x-axis
3. Test Bz in the near field is close to the exact value
4. Test Bz in the far field is close to the exact value

Bzx_method
^^^^^^^^^^

1. Test Bzx output has the same shape as the input grid
2. Test Bzx output is symmetric along x-axis
3. Test Bzx in the near field is close to the exact value
4. Test Bzx in the far field is close to the exact value
5. Test Bzx when x is 0, Bzx is 0

Bzxx_method
^^^^^^^^^^^

1. Test Bzxx output has the same shape as the input grid
2. Test Bzxx output is symmetric along x-axis
3. Test Bzxx in the near field is close to the exact value
4. Test Bzxx in the far field is close to the exact value
"""


class TestCylinderMagnet:
    def setup_method(self):
        self.magnet = CylinderMagnetApprox(
            magnet_radius=0.5, magnet_length=10, magnet_origin=[0, 0, 0], mu0_Ms=1
        )

    def test_Bz_shape(self):
        """Test the shape of the magnetic field Bz to be the same as the input grid."""
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bz = self.magnet.Bz_method(grid[0], grid[1], grid[2])
        assert Bz.shape == (2, 5, 10)

    def test_Bzx_shape(self):
        """Test the shape of the magnetic field Bzx to be the same as the input grid."""
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bzx = self.magnet.Bzx_method(grid[0], grid[1], grid[2])
        assert Bzx.shape == (2, 5, 10)

    def test_Bzxx_shape(self):
        """Test the shape of the magnetic field Bzxx to be the same as the input grid."""
        grid = np.ogrid[-1:1:2j, -1:1:5j, -1:1:10j]
        Bzxx = self.magnet.Bzxx_method(grid[0], grid[1], grid[2])
        assert Bzxx.shape == (2, 5, 10)

    def test_Bz_symmetry(self):
        """Test the symmetry of the magnetic field Bz along x-axis."""
        Bz1 = self.magnet.Bz_method(1, 2, 6)
        Bz2 = self.magnet.Bz_method(-1, 2, 6)
        assert np.allclose(Bz1, Bz2)

    def test_Bzx_symmetry(self):
        """Test the symmetry of the magnetic field Bzx along x-axis."""
        Bzx1 = self.magnet.Bzx_method(1, 2, 6)
        Bzx2 = self.magnet.Bzx_method(-1, 2, 6)
        assert np.allclose(Bzx1, -Bzx2)  # Bzx is antisymmetric

    def test_Bzxx_symmetry(self):
        """Test the symmetry of the magnetic field Bzxx along x-axis."""
        Bzxx1 = self.magnet.Bzxx_method(1, 2, 6)
        Bzxx2 = self.magnet.Bzxx_method(-1, 2, 6)
        assert np.allclose(Bzxx1, Bzxx2)  # Bzxx is symmetric

    def test_Bz_near_field(self):
        """Test the magnetic field Bz at near field.

        Test at poles (1.0, 2.0, 6.0).
        """
        Bz = self.magnet.Bz_method(1, 2, 6)
        assert np.allclose(Bz, 0.003938311762612047, atol=1e-5)

    def test_Bzx_near_field(self):
        """Test the magnetic field Bzx at near field.

        Test at poles (1.0, 2.0, 6.0).
        """
        Bzx = self.magnet.Bzx_method(1, 2, 6)
        assert np.allclose(Bzx, -0.0022319789019074046, atol=1e-5)

    def test_Bzxx_near_field(self):
        """Test the magnetic field Bzxx at near field.

        Test at poles (1.0, 2.0, 6.0).
        """
        Bzxx = self.magnet.Bzxx_method(1, 2, 6)
        assert np.allclose(Bzxx, -0.00035144076191428254, atol=1e-5)

    def test_Bz_far_field(self):
        """Test the magnetic field Bz at far field.

        Test at (10.0, 0.0, 0.0).
        """
        Bz = self.magnet.Bz_method(10, 0, 0)
        assert np.allclose(Bz, (-0.00045051510382442363), atol=1e-4)

    def test_Bzx_far_field(self):
        """Test the magnetic field Bzx at far field.

        Test at (10.0, 0.0, 0.0).
        """
        Bzx = self.magnet.Bzx_method(10, 0, 0)
        assert np.allclose(Bzx, 0.00010817803386829378, atol=1e-4)

    def test_Bzxx_far_field(self):
        """Test the magnetic field Bzxx at far field.

        Test at (10.0, 0.0, 0.0).
        """
        Bzxx = self.magnet.Bzxx_method(10, 0, 0)
        assert np.allclose(Bzxx, -3.245766094831442e-05, atol=1e-4)

    def test_Bzx_x_is_0(self):
        """Test the magnetic field Bzx when x is 0.

        Test at (0.0, 10.0, 0.0).
        """
        Bzx = self.magnet.Bzx_method(0, 10, 0)
        assert np.allclose(Bzx, 0, atol=1e-10)
