"""Test the relative change in polarization."""

import mrfmsim.formula.polarization as pol
import numpy as np
from mrfmsim.component import Sample
import pytest


@pytest.fixture
def sample_e():
    """Electron sample."""
    return Sample(spin="e", temperature=0.001, T1=1.0, T2=1.0, spin_density=10.0)


@pytest.fixture
def sample_h():
    """Nucleus sample."""
    return Sample(spin="1H", temperature=4.2, T1=10, T2=5e-6, spin_density=49.0)


def test_rel_dpol_sat_steadystate(sample_e):
    """Test the rel_dpol_sat *absolute* tolerance.

    Sample -> e -> electron spin, J = 1/2, high field limit
    """

    p1 = pol.rel_dpol_sat_steadystate(0.0, 0.0, sample_e.dB_sat, sample_e.dB_hom)
    # depolarized
    p2 = pol.rel_dpol_sat_steadystate(0.0, 1.0, sample_e.dB_sat, sample_e.dB_hom)
    # polarized
    p3 = pol.rel_dpol_sat_steadystate(100.0, 1.0e-3, sample_e.dB_sat, sample_e.dB_hom)

    assert pytest.approx([0.0, -1.0, 0.0], abs=1e-10) == [p1, p2, p3]


def test_rel_dpol_ibm_cyclic(sample_h):
    """Test rpol_arp_ibm.

    Sample -> proton spin -> rpol_arp_ibm() limiting cases
    Sample -> h -> proton spin
    """

    # on resonance
    n1 = pol.rel_dpol_ibm_cyclic(0.0, 2.0e6, sample_h.Gamma)
    # below resonance
    n2 = pol.rel_dpol_ibm_cyclic(-100.0, 2.0e6, sample_h.Gamma)
    # above resonance
    n3 = pol.rel_dpol_ibm_cyclic(100.0, 2.0e6, sample_h.Gamma)

    assert pytest.approx([n1, n2, n3], abs=1e-10) == [-1.0, 0.0, 0.0]


def test_rel_dpol_nut(sample_h):
    """Test rel_dpol_nut.

    Sample -> proton spin -> rpol_nut(), on resonance pulses
    Sample -> h -> proton spin
    """

    Gamma = 0.0425774805964  # gyromagnetic ratio in MHz/mT
    rabi = 1.0 / (Gamma)  # Rabi period in microseconds for 1 mT

    # pi/2 pulse
    rpol_090 = pol.rel_dpol_nut(0.0, 1.0, sample_h.Gamma, 0.25 * rabi * 1.0e-6)

    # pi pulse
    rpol_180 = pol.rel_dpol_nut(0.0, 1.0, sample_h.Gamma, 0.50 * rabi * 1.0e-6)

    assert pytest.approx([rpol_090, rpol_180], abs=1e-10) == [-1.0, -2.0]


def test_rel_dpol_arp(sample_h):
    """Test rel_dpol_arp.

    if f_fm is close to infinity, the relative change in polarization
    is -2.0
    if b1 and the modulation frequency is small and b_offset is large
    the spin does not flip therefore the relative change in polarization
    is close to 0.0 (off-resonance case)
    """

    rpol_180 = pol.rel_dpol_arp(0.0, 1.0, 1e10, sample_h.Gamma)
    assert np.isclose(rpol_180, -2.0)

    rpol_0 = pol.rel_dpol_arp(10000.0, 0.1, 0.1, sample_h.Gamma)

    assert pytest.approx(0.0, abs=5e-10) == rpol_0


def test_rel_dpol_periodic_irrad_cont(sample_e):
    """Test rel_dpol_periodic_irrad in the continuous case.

    When the if t_off is 0, the intermittent irradiation becomes continuous
    irradiation. This should be the same as rel_dpol_sat
    When t_on is 0, the signal should vanish
    """
    # continuous
    rpol_cont = pol.rel_dpol_periodic_irrad(
        0,
        1.0,
        sample_e.dB_sat,
        sample_e.dB_hom,
        sample_e.T1,
        t_on=10 * sample_e.T1,
        t_off=0,
    )
    rpol = pol.rel_dpol_sat_steadystate(0, 1.0, sample_e.dB_sat, sample_e.dB_hom)

    assert pytest.approx(rpol_cont) == rpol


def test_rel_dpol_periodic_irrad_no_irrad(sample_e):
    """Test rel_dpol_periodic_irrad in no irradiation case.

    When t_on is 0, the signal should vanish
    """

    rpol_0 = pol.rel_dpol_periodic_irrad(
        0, 1.0, sample_e.dB_sat, sample_e.dB_hom, sample_e.T1, t_on=0, t_off=2e-4
    )

    assert rpol_0 == 0.0


def test_rel_dpol_periodic_irrad_off_res(sample_e):
    """Test rel_dpol_periodic_irrad off-resonance case.

    When is it off-resonance (B_offset is large), the signal is 0
    """

    # off-resonance case
    rpol_off_res = pol.rel_dpol_periodic_irrad(
        10000,
        0.5,
        sample_e.dB_sat,
        sample_e.dB_hom,
        sample_e.T1,
        t_on=4e-5,
        t_off=2e-4,
    )

    assert pytest.approx(rpol_off_res, abs=5e-10) == 0.0


def test_rel_dpol_sat_td(sample_e):
    """Test rel_dpol_sat_td when offset is 0.

    When the offset is 0, the result should be 0

    Here we construct a 1D grid size of 3, and
    extended grid size of 5
    """
    Bzx = np.random.rand(3)
    ext_B_offset = np.zeros([5])

    rpol = pol.rel_dpol_sat_td(
        Bzx, 1.0, ext_B_offset, 1, sample_e.Gamma, sample_e.T2, 2000
    )

    assert np.array_equal(rpol, [0, 0, 0])


def test_rel_dpol_sat_td_symmetry(sample_e):
    """Test rel_dpol_sat_td is symmetric around the initial and final offset.

    Here we construct a 1D grid size of 3, and an extended grid size of 5
    """
    Bzx = np.random.rand(3)
    ext_B_offset_a = np.array([2, 0, 0, 0, 2])
    ext_B_offset_b = np.array([0, 2, 2, 2, 0])

    rpol_a = pol.rel_dpol_sat_td(
        Bzx, 1.0, ext_B_offset_a, 1, sample_e.Gamma, sample_e.T2, 2000
    )
    rpol_b = pol.rel_dpol_sat_td(
        Bzx, 1.0, ext_B_offset_b, 1, sample_e.Gamma, sample_e.T2, 2000
    )
    assert np.array_equal(rpol_a, rpol_b)

def test_rel_dpol_sat_td_NaN(sample_e):
    """Test rel_dpol_sat_td will not return Nan when Bzx is 0 and B_offset is symmetric.
    """
    Bzx = np.array([1, 0, -1])
    ext_B_offset_a = np.array([2, 0, 0, 0, 2])
    ext_B_offset_b = np.array([0, 2, 2, 2, 0])

    rpol_a = pol.rel_dpol_sat_td(
        Bzx, 1.0, ext_B_offset_a, 1, sample_e.Gamma, sample_e.T2, 2000
    )
    rpol_b = pol.rel_dpol_sat_td(
        Bzx, 1.0, ext_B_offset_b, 1, sample_e.Gamma, sample_e.T2, 2000
    )
    assert not np.any(np.isnan(rpol_a))
    assert not np.any(np.isnan(rpol_b))


def test_rel_dpol_sat_td_without_td(sample_e):
    """Test rel_dpol_sat_td completely saturate spins if no td component.

    Here we construct a 1D grid size of 3 and an extended grid size of 5
    """
    Bzx = np.zeros(3)
    ext_B_offset = np.random.rand(5)

    rpol = pol.rel_dpol_sat_td(
        Bzx, 1.0, ext_B_offset, 1, sample_e.Gamma, sample_e.T2, 2000
    )

    assert np.array_equal(rpol, [-1, -1, -1])


def test_rel_dol_sat_td_smallsteps(sample_e):
    """Test rel_dol_sat_td_smallsteps.

    Small steps approximation should have the same result as regular
    when Bzx stays the same, given that delta_B_offset has the same
    sign as Bzx.
    """

    Bzx = np.ones(3)
    ext_Bzx = np.ones(5)
    ext_B_offset = np.random.rand(1) * np.array([1, 2, 3, 4, 5])

    rpol_td = pol.rel_dpol_sat_td(
        Bzx, 1.0, ext_B_offset, 1, sample_e.Gamma, sample_e.T2, 2000.0
    )

    rpol_smallsteps = pol.rel_dpol_sat_td_smallsteps(
        1.0, ext_Bzx, ext_B_offset, 1, sample_e.Gamma, sample_e.T2, 2000.0
    )

    assert np.array_equal(rpol_td, rpol_smallsteps)


def test_rel_dpol_multipulse_no_pol(sample_e):
    """Test rel_dpol_multipulse when relative polarization is 0."""

    rpol = pol.rel_dpol_multipulse(0, sample_e.T1, 1.0)
    assert rpol == 0


def test_rel_dpol_multipulse_short(sample_e):
    """Test rel_dpol_multipulse when the pulse time difference is short.

    Because the time between pulses is short and the equation ignores
    relaxation during pulses,
    """

    rpol = pol.rel_dpol_multipulse(-1, sample_e.T1, 0.001)
    assert pytest.approx(rpol, abs=0.001) == -1


def test_rel_dpol_multipulse_long(sample_e):
    """Test rel_dpol_multipulse when the time between pulses is long.

    In this case, the final polarization should be
    relaxed to 1 and the chang in polarization is 0.
    """

    rpol = pol.rel_dpol_multipulse(-0.5, sample_e.T1, 500.0)
    assert pytest.approx(rpol, abs=0.001) == 0
