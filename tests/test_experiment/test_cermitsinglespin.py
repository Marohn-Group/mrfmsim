"""Test the group of CERMIT ESR experiments."""

from mrfmsim.experiment import CermitSingleSpinGroup
from mrfmsim.component import Sample, SphereMagnet
import numpy as np
import pytest

CermitESRSingleSpin = CermitSingleSpinGroup.experiments["CermitSingleSpin"]
CermitSingleSpinApprox = CermitSingleSpinGroup.experiments["CermitSingleSpinApprox"]


class TestCermitSinglespin:
    """Test the CERMIT ESR experiment with a single spin.

    See test_misc.py for the test of the numerical solution.
    Here, we test that the approximated solution is similar to the exact solution.
    """

    @pytest.fixture
    def sample(self):
        """Return the sample object."""

        return Sample(
            spin="e",
            temperature=4.2,
            T1=1.0e-3,
            T2=450e-9,
            spin_density=None,
        )

    @pytest.fixture
    def n_pts(self):
        """Number of points in the trapezoid approximation."""

        return 40

    @pytest.mark.parametrize("x_0p", np.linspace(5, 245, 3))
    def test_cermitesr_singlespin_spam(self, sample, n_pts, x_0p):
        """Compare the numerical solution with the exact solution."""

        ogrid = np.ogrid[0:0:1j, 0:0:1j, 0:0:1j]
        magnet = SphereMagnet(radius=3300.0, mu0_Ms=440.0, origin=[0, 3000, 0])

        approx = CermitSingleSpinApprox(
            magnet=magnet,
            sample=sample,
            grid_array=ogrid,
            h=[0, 300, 0],
            x_0p=x_0p,
            trapz_pts=n_pts,
        )
        exact = CermitESRSingleSpin(
            magnet=magnet,
            sample=sample,
            magnet_spin_dist=300,
            x_0p=x_0p,
            geometry="spam",
        )

        assert np.isclose(approx, exact, rtol=1e-6)

    @pytest.mark.parametrize("x_0p", np.linspace(5, 245, 3))
    def test_cermitesr_singlespin_hangdown(self, sample, n_pts, x_0p):
        """Compare the numerical solution with the exact solution."""

        ogrid = np.ogrid[0:0:1j, 0:0:1j, 0:0:1j]
        magnet = SphereMagnet(radius=3300.0, mu0_Ms=440.0, origin=[0, 0, 4000])

        approx = CermitSingleSpinApprox(
            magnet=magnet,
            sample=sample,
            grid_array=ogrid,
            h=[0, 0, 300],
            x_0p=x_0p,
            trapz_pts=n_pts,
        )
        exact = CermitESRSingleSpin(
            magnet=magnet,
            sample=sample,
            magnet_spin_dist=300,
            x_0p=x_0p,
            geometry="hangdown",
        )

        assert np.isclose(approx, exact, rtol=1e-6)
