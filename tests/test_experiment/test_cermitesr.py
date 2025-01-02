from mrfmsim.component import SphereMagnet, Grid, Sample, Cantilever
from mrfmsim.experiment import CermitESRGroup
import numpy as np
import pytest


CermitESR = CermitESRGroup.experiments["CermitESR"]
CermitESRSmallTip = CermitESRGroup.experiments["CermitESRSmallTip"]
# CermitSingleSpinApprox = CermitSingleSpinGroup["CermitSingleSpinApprox"]


@pytest.fixture
def sample():
    """Return the sample object."""

    return Sample(
        spin="e",
        temperature=11.0,
        T1=1.3e-3,
        T2=0.45e-6,
        spin_density=0.0241,
    )


@pytest.fixture
def cantilever():
    """Return the cantilever object."""

    return Cantilever(k_c=7.8e5, f_c=4.975e6)


class TestCERMITESR:
    """Test cermitesr experiment."""

    def test_cermitesr_SPAM(self, sample, cantilever):
        """Test the result in SPAM geometry, Moore parameters, local peak."""

        magnet = SphereMagnet(radius=1850.0, mu0_Ms=440.0, origin=[0, 1850, 0])
        grid = Grid(shape=[501, 21, 251], step=[8, 10, 8], origin=[0, -100, 0])

        cantilever = Cantilever(k_c=2e4, f_c=3e6)

        B1 = 3.9e-4
        mw_x_0p = 330
        B0 = 700
        f_rf = 17.7e9
        h = [0, 50, 0]  # tip sample separation [nm]

        df_spin = CermitESR(B0, B1, cantilever, f_rf, grid, h, magnet, mw_x_0p, sample)

        assert np.isclose(df_spin, cantilever.k2f_modulated * -0.940, rtol=5e-1)

    def test_cermitesr_hangdown(self, sample, cantilever):
        """Test the result in SPAM geometry, Issac parameters."""

        magnet = SphereMagnet(radius=3300.0, mu0_Ms=440.0, origin=[0, 0, 3300])
        grid = Grid(shape=[400, 1200, 8], step=[25, 25, 25], origin=[0, 0, -100])

        B1 = 1.3e-3
        mw_x_0p = 100
        B0 = 570
        f_rf = 18.5e9
        h = [0, 0, 1450]  # tip sample separation [nm]

        df_spin = CermitESR(B0, B1, cantilever, f_rf, grid, h, magnet, mw_x_0p, sample)

        assert np.isclose(df_spin, cantilever.k2f_modulated * -25.086, rtol=5e-1)


# class TestCERMITESR_smalltip:
#     """Test cermitesr_smalltip experiment."""

#     def test_compare_smalltip_vs_singlespin_approximation(self, cantilever):
#         """Compare the small tip result against the single spin result.

#         We cannot use the single spin exact solution for a rectangular tip.
#         Here, we use the approximation.
#         """

#         magnet = RectangularMagnet(
#             length=[100.0, 70.0, 1500.0],
#             mu0_Ms=1800.0,
#             origin=[0.0, 0.0, 1500.0 / 2.0],
#         )

#         grid = Grid(
#             shape=[1, 1, 1],
#             step=[0.01, 0.01, 0.01],
#             origin=[0.0, 0.0, 0.0],
#         )

#         sample = Sample(
#             spin="e",
#             temperature=4.2,
#             T1=1.0e-3,
#             T2=450e-9,
#             spin_density=1 / grid.voxel,  # only 1 spin in the grid
#         )

#         B0 = 100000
#         f_rf = 2813.8039e9
#         B1 = 2.2e-0
#         h = [0, 0, 30.0]
#         grid_array = grid.grid_array
#         trapz_pts = 20
#         mw_x_0p = 5

#         analytical = cantilever.k2f_modulated * CermitSingleSpinApprox(
#             magnet=magnet,
#             sample=sample,
#             grid_array=grid_array,
#             trapz_pts=trapz_pts,
#             x_0p=mw_x_0p,
#             h=h,
#         )

#         result = CermitESRSmallTip(
#             B0,
#             B1,
#             cantilever,
#             f_rf,
#             grid,
#             h,
#             magnet,
#             mw_x_0p,
#             sample,
#             trapz_pts,
#             mw_x_0p,  # here us the same x_0p (pulsing the whole cycle)
#         )

#         assert np.isclose(result, analytical, rtol=1e-4)
