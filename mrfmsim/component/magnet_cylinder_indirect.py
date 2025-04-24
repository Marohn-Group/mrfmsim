import numpy as np
import sympy
from sympy import elliptic_k, elliptic_pi
from scipy.special import elliprf, ellipk, elliprj, ellipe
from dataclasses import dataclass, field
from mrfmsim.component import ComponentBase


@dataclass
class CylinderMagnetIndirect(ComponentBase):
    """Cylinder magnet object with its Bz, Bzx, Bzxx calculations.

    :param float radius: cylinder magnet radius [nm] !!!There would ba a singularity when x^2+y^2=R^2, so set a small difference to R!!! Also when x^2+y^2=0, B_zxx would run into a singularity, try to avoid this point.
    :param float length: cylinder magnet length [nm]
    :param tuple origin: the position of the magnet origin (x, y, z)
    :param float mu0_Ms: permeability of free space [H/m]
    """

    magnet_radius: float = field(metadata={"unit": "nm", "format": ".1f"})
    magnet_length: float = field(metadata={"unit": "nm", "format": ".1f"})
    magnet_origin: tuple[float, float, float] = field(
        metadata={"unit": "nm", "format": ".1f"}
    )
    mu0_Ms: float = field(metadata={"unit": "mT"})

    def __post_init__(self):
        r"""
        This function is used to calculate the Bz, Bzr, Bzrr of the cylinder magnet using sympy. Due to the complexity of the expression, we use sympy to calculate the expression and then use sympy.lambdify to convert the expression to a numpy function.
        first use sympy to calculate the Bz, Bzr, Bzrr,the equation if from paper:https://doi.org/10.1016/j.jmmm.2018.02.003.(https://www.sciencedirect.com/science/article/pii/S0304885317334662), (note that the def of n is different in the paper and the code, so we need to change the def of n in the code).
        Also, we use ep11, ep21, ep31, ep12, ep22, ep32 to replace the elliptic_k, elliptic_e, elliptic_pi, to avoid call elliptic_k, elliptic_e, elliptic_pi repeatedly.

        variables:
        r: radius of the sample grid
        Z: z coordinate of the sample grid
        R: radius of the magnet
        L: length of the magnet
        ep11, ep21, ep31, ep12, ep22, ep32: precomputed elliptic functions
        """

        r, Z, R, L = sympy.symbols("r Z R L")
        ep11, ep21, ep31 = sympy.symbols("ep11 ep21 ep31")
        ep12, ep22, ep32 = sympy.symbols("ep12 ep22 ep32")

        g = (r - R) / (r + R)

        eps1 = Z + L
        eps2 = Z - L

        alpha1 = 1 / sympy.sqrt(eps1**2 + (r + R) ** 2)
        alpha2 = 1 / sympy.sqrt(eps2**2 + (r + R) ** 2)

        k1 = (eps1**2 + (r - R) ** 2) / (eps1**2 + (r + R) ** 2)
        k2 = (eps2**2 + (r - R) ** 2) / (eps2**2 + (r + R) ** 2)
        n = 1 - g**2

        P21 = -g / (1 - g**2) * (elliptic_pi(n, 1 - k1) - elliptic_k(1 - k1)) - 1 / (
            1 - g**2
        ) * (g**2 * elliptic_pi(n, 1 - k1) - elliptic_k(1 - k1))
        P22 = -g / (1 - g**2) * (elliptic_pi(n, 1 - k2) - elliptic_k(1 - k2)) - 1 / (
            1 - g**2
        ) * (g**2 * elliptic_pi(n, 1 - k2) - elliptic_k(1 - k2))

        Bz = (P21 * alpha1 * eps1 - P22 * eps2 * alpha2) * R / (r + R) / sympy.pi
        Bzr = sympy.diff(Bz, r)
        Bzrr = sympy.diff(Bzr, r)

        Bz_subs = Bz.subs(
            {
                sympy.elliptic_k(1 - k1): ep11,
                sympy.elliptic_e(1 - k1): ep21,
                sympy.elliptic_pi(n, 1 - k1): ep31,
                sympy.elliptic_k(1 - k2): ep12,
                sympy.elliptic_e(1 - k2): ep22,
                sympy.elliptic_pi(n, 1 - k2): ep32,
            }
        )

        Bzr_subs = Bzr.subs(
            {
                sympy.elliptic_k(1 - k1): ep11,
                sympy.elliptic_e(1 - k1): ep21,
                sympy.elliptic_pi(n, 1 - k1): ep31,
                sympy.elliptic_k(1 - k2): ep12,
                sympy.elliptic_e(1 - k2): ep22,
                sympy.elliptic_pi(n, 1 - k2): ep32,
            }
        )

        Bzrr_subs = Bzrr.subs(
            {
                sympy.elliptic_k(1 - k1): ep11,
                sympy.elliptic_e(1 - k1): ep21,
                sympy.elliptic_pi(n, 1 - k1): ep31,
                sympy.elliptic_k(1 - k2): ep12,
                sympy.elliptic_e(1 - k2): ep22,
                sympy.elliptic_pi(n, 1 - k2): ep32,
            }
        )

        special_functions = {"sqrt": np.sqrt, "pi": np.pi}

        self.Bz_np = sympy.lambdify(
            (r, Z, R, L, ep11, ep21, ep31, ep12, ep22, ep32),
            Bz_subs,
            modules=[special_functions, "numpy"],
        )
        self.Bzr_np = sympy.lambdify(
            (r, Z, R, L, ep11, ep21, ep31, ep12, ep22, ep32),
            Bzr_subs,
            modules=[special_functions, "numpy"],
        )
        self.Bzrr_np = sympy.lambdify(
            (r, Z, R, L, ep11, ep21, ep31, ep12, ep22, ep32),
            Bzrr_subs,
            modules=[special_functions, "numpy"],
        )

    def Bz_method(self, x, y, z):
        r"""Calculate magnetic field :math:`B_z` [mT].

                The magnetic field is calculated as

        .. math::
            Bz = mu0_Ms * (P21 * alpha1 * eps1 - P22 * eps2 * alpha2) * R / (r + R) / pi

        in which:
            eps1 = z + L/2
            eps2 = z - L/2
            k1 = (eps1**2 + (r - R) ** 2) / (eps1**2 + (r + R) ** 2)
            k2 = (eps2**2 + (r - R) ** 2) / (eps2**2 + (r + R) ** 2)
            g = (r - R) / (r + R)
            n = 1 - g**2
            alpha1 = 1 / \sqrt{eps1**2 + (r + R) ** 2}
            alpha2 = 1 / \sqrt{eps2**2 + (r + R) ** 2}
            P21 = -g / (1 - g**2) * (elliptic_pi(n, 1 - k1) - elliptic_k(1 - k1)) - 1 / (1 - g**2 ) * (g**2 * elliptic_pi(n, 1 - k1) - elliptic_k(1 - k1))
            P22 = -g / (1 - g**2) * (elliptic_pi(n, 1 - k2) - elliptic_k(1 - k2)) - 1 / (1 - g**2 ) * (g**2 * elliptic_pi(n, 1 - k2) - elliptic_k(1 - k2))
        note that:
            the def of n (in elliptic integral) is different in the paper and the code, so we need to change the def of n in the code.

        :param float x: x coordinate of sample grid [nm]
        :param float y: y coordinate of sample grid [nm]
        :param float z: z coordinate of sample grid [nm]


        Here :math:`(x,y,z)` is the location at which we want to know the field;
        :math:`r` is the radius of the magnet; :math:`r**2 = x**2 + y**2`;
        :math 'dx = x-x_0'
        :math 'dy = y-y_0'
        :math 'dz = z-z_0'
        distances to the center of the magnet;
        :math:`\mu_0 M_s` is the magnetic sphere's saturation
        magnetization in mT.

        There is a singularity when x^2+y^2==0, so we need to manually replace B_z with its corresponding algebraic form:

        .. math::
            Bz = \dfrac{\mu0_Ms}{2} * \dfrac{z + L/2}{\sqrt{(z + L/2)**2 + R**2}} - \dfrac{\mu0_Ms}{2} * \dfrac{z - L/2}{\sqrt{(z - L/2)**2 + R**2}}
        """

        def ellipiticPi(n, m):
            return elliprf(0.0, 1.0 - m, 1.0) + (n / 3.0) * elliprj(
                0.0, 1.0 - m, 1.0, 1.0 - n
            )

        dr = np.sqrt(
            (x - self.magnet_origin[0]) ** 2 + (y - self.magnet_origin[1]) ** 2
        )
        dz = z - self.magnet_origin[2]
        L = self.magnet_length / 2
        g = (dr - self.magnet_radius) / (dr + self.magnet_radius)
        eps1 = z + L
        eps2 = z - L
        k1 = (eps1**2 + (dr - self.magnet_radius) ** 2) / (
            eps1**2 + (dr + self.magnet_radius) ** 2
        )
        k2 = (eps2**2 + (dr - self.magnet_radius) ** 2) / (
            eps2**2 + (dr + self.magnet_radius) ** 2
        )
        n = 1 - g**2

        ep11 = ellipk(1 - k1)
        ep21 = ellipe(1 - k1)
        ep31 = ellipiticPi(n, 1 - k1)

        ep12 = ellipk(1 - k2)
        ep22 = ellipe(1 - k2)
        ep32 = ellipiticPi(n, 1 - k2)

        zero_coords = np.argwhere(dr == 0)

        if zero_coords.size > 0:
            dr[zero_coords[0][0]][zero_coords[0][1]][zero_coords[0][2]] = np.nan
            BZ = self.mu0_Ms * self.Bz_np(
                r=dr,
                Z=dz,
                R=self.magnet_radius,
                L=L,
                ep11=ep11,
                ep21=ep21,
                ep31=ep31,
                ep12=ep12,
                ep22=ep22,
                ep32=ep32,
            )
            BZ[zero_coords[0][0]][zero_coords[0][1]][:] = (
                self.mu0_Ms
                / 2
                * (
                    (dz + self.magnet_length / 2)
                    / np.sqrt(
                        (dz + self.magnet_length / 2) ** 2 + (self.magnet_radius) ** 2
                    )
                    - (dz - self.magnet_length / 2)
                    / np.sqrt(
                        (dz - self.magnet_length / 2) ** 2 + (self.magnet_radius) ** 2
                    )
                )
            )
            return BZ

        else:
            return self.mu0_Ms * self.Bz_np(
                r=dr,
                Z=dz,
                R=self.magnet_radius,
                L=L,
                ep11=ep11,
                ep21=ep21,
                ep31=ep31,
                ep12=ep12,
                ep22=ep22,
                ep32=ep32,
            )

    def Bzx_method(self, x, y, z):
        r"""Calculate magnetic field :math:`B_z` [mT].

                The magnetic field is calculated as

        .. math:
            \dfrac{\partial B_z}{\partial x} = \dfrac{\partial B_z}{\partial r} * \dfrac{\partial r}{\partial x}+\dfrac{\partial B_z}{\partial z} * \dfrac{\partial z}{\partial x}
            =\dfrac{\partial B_z}{\partial r} * \dfrac{x}{r}

        :param float x: x coordinate of sample grid [nm]
        :param float y: y coordinate of sample grid [nm]
        :param float z: z coordinate of sample grid [nm]

        Here :math:`(x,y,z)` is the location at which we want to know the field;
        :math:`r` is the radius of the magnet; :math:`r**2 = x**2 + y**2`;
        :math 'dx = x-x_0'
        :math 'dy = y-y_0'
        :math 'dz = z-z_0'
        distances to the center of the magnet;
        :math:`\mu_0 M_s` is the magnetic sphere's saturation
        magnetization in mT.
        """

        def ellipiticPi(n, m):
            return elliprf(0.0, 1.0 - m, 1.0) + (n / 3.0) * elliprj(
                0.0, 1.0 - m, 1.0, 1.0 - n
            )

        dr = np.sqrt(
            (x - self.magnet_origin[0]) ** 2 + (y - self.magnet_origin[1]) ** 2
        )
        dz = z - self.magnet_origin[2]
        zero_coords = np.argwhere(dr == 0)

        L = self.magnet_length / 2
        g = (dr - self.magnet_radius) / (dr + self.magnet_radius)
        eps1 = z + L
        eps2 = z - L
        k1 = (eps1**2 + (dr - self.magnet_radius) ** 2) / (
            eps1**2 + (dr + self.magnet_radius) ** 2
        )
        k2 = (eps2**2 + (dr - self.magnet_radius) ** 2) / (
            eps2**2 + (dr + self.magnet_radius) ** 2
        )
        n = 1 - g**2

        ep11 = ellipk(1 - k1)
        ep21 = ellipe(1 - k1)
        ep31 = ellipiticPi(n, 1 - k1)

        ep12 = ellipk(1 - k2)
        ep22 = ellipe(1 - k2)
        ep32 = ellipiticPi(n, 1 - k2)

        if zero_coords.size > 0:
            dr[zero_coords[0][0]][zero_coords[0][1]][zero_coords[0][2]] = np.nan
            BZr = (
                self.mu0_Ms
                * self.Bzr_np(
                    r=dr,
                    Z=dz,
                    R=self.magnet_radius,
                    L=L,
                    ep11=ep11,
                    ep21=ep21,
                    ep31=ep31,
                    ep12=ep12,
                    ep22=ep22,
                    ep32=ep32,
                )
                * (x - self.magnet_origin[0])
                / dr
            )
            BZr[zero_coords[0][0]][zero_coords[0][1]][:] = np.zeros(len(dz))
            return BZr

        else:
            return (
                self.mu0_Ms
                * self.Bzr_np(
                    r=dr,
                    Z=dz,
                    R=self.magnet_radius,
                    L=L,
                    ep11=ep11,
                    ep21=ep21,
                    ep31=ep31,
                    ep12=ep12,
                    ep22=ep22,
                    ep32=ep32,
                )
                * (x - self.magnet_origin[0])
                / dr
            )

    def Bzxx_method(self, x, y, z):
        r"""Calculate magnetic field :math:`B_z` [mT].

                The magnetic field is calculated as

        .. math:
            using sympy directly calculate the derivative of Bzr

        :param float x: x coordinate of sample grid [nm]
        :param float y: y coordinate of sample grid [nm]
        :param float z: z coordinate of sample grid [nm]


        Here :math:`(x,y,z)` is the location at which we want to know the field;
        :math:`r` is the radius of the magnet; :math:`r**2 = x**2 + y**2`;
        :math 'dx = x-x_0'
        :math 'dy = y-y_0'
        :math 'dz = z-z_0'
        distances to the center of the magnet;
        :math:`\mu_0 M_s` is the magnetic sphere's saturation
        magnetization in mT.
        """

        def ellipiticPi(n, m):
            return elliprf(0.0, 1.0 - m, 1.0) + (n / 3.0) * elliprj(
                0.0, 1.0 - m, 1.0, 1.0 - n
            )

        dr = np.sqrt(
            (x - self.magnet_origin[0]) ** 2 + (y - self.magnet_origin[1]) ** 2
        )
        dz = z - self.magnet_origin[2]

        zero_coords = np.argwhere(dr == 0)

        L = self.magnet_length / 2
        g = (dr - self.magnet_radius) / (dr + self.magnet_radius)
        eps1 = z + L
        eps2 = z - L
        k1 = (eps1**2 + (dr - self.magnet_radius) ** 2) / (
            eps1**2 + (dr + self.magnet_radius) ** 2
        )
        k2 = (eps2**2 + (dr - self.magnet_radius) ** 2) / (
            eps2**2 + (dr + self.magnet_radius) ** 2
        )
        n = 1 - g**2

        # then we calculate the ep11, ep21, ep31, ep12, ep22, ep32, We will precompute the numerical values of these elliptic functions and pass them as inputs to the functions to avoid repeatedly calling the elliptic functions and thus reduce runtime. However, this will increase memory usage.
        ep11 = ellipk(1 - k1)
        ep21 = ellipe(1 - k1)
        ep31 = ellipiticPi(n, 1 - k1)

        ep12 = ellipk(1 - k2)
        ep22 = ellipe(1 - k2)
        ep32 = ellipiticPi(n, 1 - k2)

        if zero_coords.size > 0:
            dr[zero_coords[0][0]][zero_coords[0][1]][zero_coords[0][2]] = (
                x[1] - x[0]
            ) / 1000  # I still don't have a good way to approximate this point, so I just set a small difference to 0, notice that Bzxx is symmetric.
            BZxx = (
                self.mu0_Ms
                * self.Bzrr_np(
                    r=dr,
                    Z=dz,
                    R=self.magnet_radius,
                    L=L,
                    ep11=ep11,
                    ep21=ep21,
                    ep31=ep31,
                    ep12=ep12,
                    ep22=ep22,
                    ep32=ep32,
                )
                * (x - self.magnet_origin[0]) ** 2
                / dr**2
                - self.mu0_Ms
                * self.Bzr_np(
                    r=dr,
                    Z=dz,
                    R=self.magnet_radius,
                    L=L,
                    ep11=ep11,
                    ep21=ep21,
                    ep31=ep31,
                    ep12=ep12,
                    ep22=ep22,
                    ep32=ep32,
                )
                * (y - self.magnet_origin[1]) ** 2
                / dr**3
            )
            return BZxx

        else:
            return (
                self.mu0_Ms
                * self.Bzrr_np(
                    r=dr,
                    Z=dz,
                    R=self.magnet_radius,
                    L=L,
                    ep11=ep11,
                    ep21=ep21,
                    ep31=ep31,
                    ep12=ep12,
                    ep22=ep22,
                    ep32=ep32,
                )
                * (x - self.magnet_origin[0]) ** 2
                / dr**2
                - self.mu0_Ms
                * self.Bzr_np(
                    r=dr,
                    Z=dz,
                    R=self.magnet_radius,
                    L=L,
                    ep11=ep11,
                    ep21=ep21,
                    ep31=ep31,
                    ep12=ep12,
                    ep22=ep22,
                    ep32=ep32,
                )
                * (y - self.magnet_origin[1]) ** 2
                / dr**3
            )
