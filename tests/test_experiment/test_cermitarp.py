from mrfmsim.experiment import CermitARPGroup
from mrfmsim.component import Sample, SphereMagnet, Grid, RectangularMagnet
import numpy as np
import pytest


CermitARP = CermitARPGroup.experiments["CermitARP"]
CermitARPSmallTip = CermitARPGroup.experiments["CermitARPSmallTip"]


class TestCERMITARP:
    r"""Test cermitarp experiments.

    .. code-block:: python

        grid = GridObject(
            L = [0.5E-3,0.5E-3,0.5E-3],
            dL= [0.5E-3,0.5E-3,0.5E-3],
            o=[0.0, 0.0, 0.0])

    The resulting grid is

    * centered at zero,
    * contains :math:`2 \times 2 \times 2 = 8` grid points, and
    * runs from ``-0.5e-3`` to ``+0.5e-3`` nm in each direction.

    So that the grid contains 1 spin total, we need to fudge the spin density
    to be
    :math:`1.0 \times 10^{9} \: \mathrm{spins} \: \mathrm{nm}^{3}`.
    Other notable features of the calculations:

    * We work at 10 millikelvin and 10.0 tesla so that the electron spin is
      nearly fully polarized
    * In the ARP experiment, we set the irradiation frequency to be in
      resonance with spins directly below the tip.  These spins experience
      a total field of 10437.318 mT.
      The assumed :math:`B_1` is 10 mT, and the FM sweep is ten times
      that (in field units).  In setting up ``expt1`` below, we must take
      care to set ``B_0_start`` to 10000.0 mT and not 10437.318 mT.

    We check to see that the single-spin signal and the pulse time agree with
    expected values to be within a 2 percent (relative) error.
    """

    @pytest.fixture
    def grid(self):
        """Setup grid."""

        return Grid(
            grid_shape=[2, 2, 2],
            grid_step=[0.5e-3, 0.5e-3, 0.5e-3],
            grid_origin=[0.0, 0.0, 0.0],
        )

    @pytest.fixture
    def sample(self):
        """Setup sample."""
        return Sample(
            spin="e",  # an imaginary electron-spin sample
            temperature=10.0e-3,  # 10 mK so the spin is fully polarized
            T1=1,
            T2=0.45e-6,
            spin_density=1.0e9,
        )

    @pytest.fixture
    def magnet(self):
        """Setup magnet."""
        return SphereMagnet(
            magnet_radius=50.0,  # magnet radius [nm]
            mu0_Ms=1800.0,  # cobalt [mT]
            magnet_origin=[0.0, 0.0, 50.0],
        )

    def test_cermitarp(self, grid, magnet, sample):
        """Test Cornell ARP full signal simulation."""
        B0 = 10000.000  # external field, 10 T
        B_tip = 437.318  # calculated field at the sample location
        B_tot = B0 + B_tip  # total field seen by spins right below the tip
        B1 = 10.0
        df_fm = 10.0 * B1 * 1.760859708e8 / (2 * np.pi)
        f_rf = B_tot * 1.760859708e8 / (2 * np.pi)

        result = CermitARP(
            B0=B0,
            B1=B1,
            df_fm=df_fm,
            f_rf=f_rf,
            grid=grid,
            h=[0, 0, 20.0],
            magnet=magnet,
            sample=sample,
        )

        assert np.allclose(result, -2.0 * 4.95203, rtol=2e-2)

    # @pytest.mark.skip(reason="incorrect experimental setup")
    # def test_cermitarp_smalltip(self, grid, magnet, sample):
    #     """Test smallamp_arp experiments."""
    #     sample = Sample(
    #        spin="e",
    #         temperature=11,
    #         T1=1.0e-3,
    #         T2=450.0e-9,
    #         spin_density=0.0241,
    #     )
    #     magnet = RectangularMagnet(
    #         magnet_length=[100.0, 1475.0, 111.0], mu0_Ms=600.0, grid_origin=[0, 1475.0 / 2, 0]
    #     )

    #     grid = Grid(grid_shape=[51, 11, 5], grid_step=[30, 23, 250], grid_origin=[0, -115, 0])

    #     B1 = 3.0e-4
    #     B0 = 624.0
    #     trapz_pts = 20
    #     f_rf = 17.6e9
    #     h = [0, 80, 0]
    #     x_0p = 40.0
    #     df_fm = 10.0 * B1 * 1.760859708e8 / (2 * np.pi)
    #     result = cermitarp_smalltip(
    #         B0, B1, df_fm, f_rf, grid, h, magnet, sample, trapz_pts, x_0p
    #     )

    #     assert np.isclose(result, -0.455, rtol=5e-1)


class TestCERMITESRSmallTip:
    """Compare different limits between experiment settings."""

    @pytest.fixture
    def sample(self):
        """Setup sample."""
        return Sample(
            spin="1H",
            temperature=4.2,
            T1=20.0,
            T2=5.0e-6,
            spin_density=49.0,
        )  # polystyrene

    def test_smallamp_arp_vs_exact_solution_small_amp(self, sample):
        """Test smalltip_arp vs. cornellcermit_arp

        Test that in small amplitude conditions, the approximation is the
        same as the small tip, which does not ignore the amplitude."""

        grid = Grid(grid_shape=[41, 41, 11], grid_step=[75, 75, 30], grid_origin=[0, 0, -150])
        magnet = RectangularMagnet(
            magnet_length=[135.0, 80.0, 1500.0],
            mu0_Ms=1800.0,
            magnet_origin=[0, 0, 750],
        )

        B1 = 2.5
        B0 = 4850.0
        df_fm = 1e6
        f_rf = 210.0e6
        h = [0, 0, 112]
        x_0p = 0.1
        trapz_pts = 21

        result_no_amp = CermitARP(B0, B1, df_fm, f_rf, grid, h, magnet, sample)
        result_large_amp = CermitARPSmallTip(
            B0, B1, df_fm, f_rf, grid, h, magnet, sample, trapz_pts, x_0p
        )

        assert np.isclose(result_no_amp, result_large_amp, rtol=1e-5)

    def test_smallamp_arp_vs_exact_solution_large_sep(self, sample):
        """Test cermitarp_smalltip vs cermitarp

        Test that when tip-sample separation is large the amplitude can also
        be ignored
        """

        sample = Sample(
            spin="1H",
            temperature=4.2,
            T1=20.0,
            T2=5.0e-6,
            spin_density=49.0,
        )  # polystyrene

        grid = Grid(grid_shape=[41, 41, 11], grid_step=[75, 75, 30], grid_origin=[0, 0, -150])
        magnet = RectangularMagnet(
            magnet_length=[135.0, 80.0, 1500.0],
            mu0_Ms=1800.0,
            magnet_origin=[0, 0, 750],
        )

        B1 = 2.5
        B0 = 4850.0
        df_fm = 1e6
        f_rf = 210.0e6
        h = [0, 0, 112]
        x_0p = 0.1
        trapz_pts = 21

        result_no_amp = CermitARP(B0, B1, df_fm, f_rf, grid, h, magnet, sample)
        result_large_amp = CermitARPSmallTip(
            B0, B1, df_fm, f_rf, grid, h, magnet, sample, trapz_pts, x_0p
        )

        assert np.isclose(result_no_amp, result_large_amp, rtol=1e-5)
