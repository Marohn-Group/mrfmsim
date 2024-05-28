import numpy as np
import numba as nb
from dataclasses import dataclass, field
from mrfmsim.component import ComponentBase


@dataclass
class SphereMagnet(ComponentBase):
    """Spherical magnet object with its Bz, Bzx, Bzxx calculations.

    :param float radius: sphere magnet radius [nm]
    :param list origin: the position of the magnet origin (x, y, z)
    :param float mu0_Ms: saturation magnetization [mT]
    """

    radius: float = field(metadata={"unit": "nm", "format": ".1f"})
    origin: list[float] = field(metadata={"unit": "nm"})
    mu0_Ms: float = field(metadata={"unit": "mT"})

    def Bz_method(self, x, y, z):
        r"""Calculate magnetic field :math:`B_z` [mT].

        :param float x: x coordinate of sample grid [nm]
        :param float y: y coordinate of sample grid [nm]
        :param float z: z coordinate of sample grid [nm]

        The magnetic field is calculated as

        .. math::
            B_z = \dfrac{\mu_0 M_s}{3}
            \left( 3 \dfrac{Z^2}{R^5} - \dfrac{1}{R^3} \right)
            R = \sqrt{X^2+Y^2+Z^2}

        Here :math:`(x,y,z)` is the location at which we want to know the field;
        :math:`(x_0, y_0, z_0)` is the location of the center of the magnet;
        :math:`r` is the radius of the magnet; :math:`X = (x-x_0)/r`;
        :math:`Y = (y-y_0)/r`, and :math:`Z = (z-z_0)/r` are normalized
        distances to the center of the magnet;
        :math:`\mu_0 M_s` is the magnetic sphere's saturation
        magnetization in mT.
        """

        dx = (x - self.origin[0]) / self.radius
        dy = (y - self.origin[1]) / self.radius
        dz = (z - self.origin[2]) / self.radius

        pre_term = self.mu0_Ms / 3.0

        return pre_term * self._bz(dx, dy, dz)

    @staticmethod
    @nb.vectorize(
        [nb.float64(nb.float64, nb.float64, nb.float64)],
        nopython=True,
        target="parallel",
    )
    def _bz(dx, dy, dz):
        """Internal calculation for bz, optimized with numba.

        :param dx: normalized distances to the center of the magnet in x
        :param dx: normalized distances to the center of the magnet in y
        :param dx: normalized distances to the center of the magnet in z
        :type: np.array
        :return: bz without pre-term
        :rtype: np.array
        """

        return (
            -1.0 / np.sqrt(dx**2 + dy**2 + dz**2) ** 3
            + 3.0 * dz**2 / np.sqrt(dx**2 + dy**2 + dz**2) ** 5
        )

    def Bzx_method(self, x, y, z):
        r"""Calculate magnetic field gradient :math:`B_{zx}`.

        :math:`B_{zx} \equiv \partial B_z / \partial x`
        [ :math:`\mathrm{mT} \: \mathrm{nm}^{-1}` ].
        With :math:`X`, :math:`Y`, :math:`Z`, :math:`R`, :math:`r`, and
        :math:`\mu_0 M_s` defined in Bz(x, y, z), the magnetic field
        gradient is calculated as

        .. math::
            B_{zx} = \dfrac{\partial B_z}{\partial z}
            = \dfrac{\mu_0 M_s}{r} X \:
            \left( \dfrac{1}{R^5} - 5 \dfrac{Z^2}{R^7} \right)
            R = \sqrt{X^2+Y^2+Z^2}

        :param float x: x coordinate of sample grid [nm]
        :param float y: y coordinate of sample grid [nm]
        :param float z: z coordinate of sample grid [nm]
        :return: magnetic field gradient
        :rtype: np.array
        """

        dx = (x - self.origin[0]) / self.radius
        dy = (y - self.origin[1]) / self.radius
        dz = (z - self.origin[2]) / self.radius
        pre_term = self.mu0_Ms / self.radius

        return pre_term * self._bzx(dx, dy, dz)

    @staticmethod
    @nb.vectorize(
        [nb.float64(nb.float64, nb.float64, nb.float64)],
        nopython=True,
        target="parallel",
    )
    def _bzx(dx, dy, dz):
        """Internal calculation for bzx, optimized with numba.

        :param dx: normalized distances to the center of the magnet in x
        :param dy: normalized distances to the center of the magnet in y
        :param dz: normalized distances to the center of the magnet in z
        :type: np.array
        :return: bzx without pre-term
        :rtype: np.array
        """

        return dx * (
            1.0 / np.sqrt(dx**2 + dy**2 + dz**2) ** 5
            - 5.0 * dz**2 / np.sqrt(dx**2 + dy**2 + dz**2) ** 7
        )

    def Bzxx_method(self, x, y, z):
        r"""Calculate magnetic field second derivative :math:`B_{zxx}`.

        :math:`B_{zxx} \equiv \partial^2 B_z / \partial x^2`
        [:math:`\mathrm{mT} \: \mathrm{nm}^{-2}`]. The inputs are
        With :math:`X`, :math:`Y`, :math:`Z`, :math:`R`, :math:`r`, and
        :math:`\mu_0 M_s` defined as above, the magnetic field
        second derivative is calculated as

        .. math::
            B_{zxx} = \dfrac{\partial B_z}{\partial z}
            = \dfrac{\mu_0 M_s}{r^2} \:
            \left( \dfrac{1}{R^5} - 5 \dfrac{X^2}{R^7}
            - 5 \dfrac{Z^2}{R^7} + 35 \dfrac{X^2 Z^2}{R^9} \right)
            R = \sqrt{X^2+Y^2+Z^2}

        :param float x: x coordinate of sample grid [nm]
        :param float y: y coordinate of sample grid [nm]
        :param float z: z coordinate of sample grid [nm]
        :return: magnetic field second derivative
        :rtype: np.array
        """

        dx = (x - self.origin[0]) / self.radius
        dy = (y - self.origin[1]) / self.radius
        dz = (z - self.origin[2]) / self.radius
        pre_term = self.mu0_Ms / (self.radius**2)

        return pre_term * self._bzxx(dx, dy, dz)

    @staticmethod
    @nb.vectorize(
        [nb.float64(nb.float64, nb.float64, nb.float64)],
        nopython=True,
        target="parallel",
    )
    def _bzxx(dx, dy, dz):
        """Internal calculation for bzxx, optimized with numba.

        :param dx: normalized distances to the center of the magnet in x
        :param dy: normalized distances to the center of the magnet in y
        :param dz: normalized distances to the center of the magnet in z
        :type: np.array
        :return: bzxx without pre-term
        :rtype: np.array
        """

        return (
            1.0 / np.sqrt(dx**2 + dy**2 + dz**2) ** 5
            - 5.0 * (dx**2) / np.sqrt(dx**2 + dy**2 + dz**2) ** 7
            - 5.0 * (dz**2) / np.sqrt(dx**2 + dy**2 + dz**2) ** 7
            + 35.0 * (dx**2) * (dz**2) / np.sqrt(dx**2 + dy**2 + dz**2) ** 9
        )


@dataclass
class RectangularMagnet(ComponentBase):
    """Rectangular magnet object with the bz, bzx, bzxx calculations.

    :param list length: length of rectangular magnet in (x, y, z) direction [nm]
    :param list origin: the position of the magnet origin (x, y, z)
    :param float mu0_Ms: saturation magnetization [mT]
    :ivar np.array _range:
        [-xrange, +xrange, -yrange, +yrange, -zrange, zrange]
        range in the x, y and z direction after the center point to the origin.
    """

    length: list[float] = field(metadata={"unit": "nm"})
    origin: list[float] = field(metadata={"unit": "nm"})
    mu0_Ms: float = field(metadata={"unit": "mT"})

    def __post_init__(self):
        self._range = np.column_stack(
            (
                -np.array(self.length) / 2 + self.origin,
                np.array(self.length) / 2 + self.origin,
            )
        ).ravel()
        self._pre_term = self.mu0_Ms / (4 * np.pi)

    def Bz_method(self, x, y, z):
        r"""Calculate magnetic field :math:`B_z` [mT].

        The magnetic field is calculated following Ravaud2009.
        Using the Coulombian model, assuming a uniform magnetization throughout
        the volume of the magnet and modeling each face of the magnet as a
        layer of continuous current density. The total field is found by
        summing over the faces.
        The magnetic field is given by:

        .. math::
            B_z = \dfrac{\mu_0 M_s}{4\pi} \sum_{i=1}^{2}
                \sum_{j=1}^2 \sum_{k=1}^2(-1)^{i+j+k}
                arctan \left( \dfrac{(x - x_i)(y - y_i))}{(z - z_k)R} \right)

        Here :math:`(x,y,z)` are the coordinates for the location at which we
        want to know the field;
        The magnet spans from x1 to x2 in the ``x``-direction,
        y1 to y2 in the ``y``-direction, and z1 to z2 in
        the ``z``-direction;

        .. math::
            R = \sqrt{(x - x_i)^2 + (y - y_j)^2 + (z - z_k)^2}

        where :math:`\mu_0 M_s` is the magnet's saturation magnetization in mT.

        **Reference**:
        Ravaud, R. and Lemarquand, G. "Magnetic field produced by a
        parallelepipedic magnet of various and uniform polarization" ,
        *PIER*, **2009**, *98*, 207-219
        [`10.2528/PIER09091704 <http://dx.doi.org/10.2528/PIER09091704>`__].

        - set the magnet up so that the x and y dimensions are centered about
          the zero point.
        - The translation in z should shift the tip of the magnet in the
          z-direction to be the given distance from the surface.

        :param float x: x coordinate of sample grid [nm]
        :param float y: y coordinate of sample grid [nm]
        :param float z: z coordinate of sample grid [nm]
        """

        dx1, dx2 = x - self._range[0], x - self._range[1]
        dy1, dy2 = y - self._range[2], y - self._range[3]
        dz1, dz2 = z - self._range[4], z - self._range[5]

        return self._pre_term * self._bz(dx1, dx2, dy1, dy2, dz1, dz2)

    @staticmethod
    @nb.vectorize(
        [
            nb.float64(
                nb.float64,
                nb.float64,
                nb.float64,
                nb.float64,
                nb.float64,
                nb.float64,
            )
        ],
        nopython=True,
        target="parallel",
    )
    def _bz(dx1, dx2, dy1, dy2, dz1, dz2):
        """Calculate the summation term for magnetic field optimized by numba.

        See method bz for the explanation.
        :param float dx1, dx2: distance between grid and the one end of magnet
                        in x direction [nm]
        :param float dy1, dy2: distance between grid and the one end of magnet
                        in y direction [nm]
        :param float dz1, dz2: distance between grid and the one end of magnet
                        in z direction [nm]
        """

        return (
            -np.arctan2(dx1 * dy1, (np.sqrt(dx1**2 + dy1**2 + dz1**2) * dz1))
            + np.arctan2(dx2 * dy1, (np.sqrt(dx2**2 + dy1**2 + dz1**2) * dz1))
            + np.arctan2(dx1 * dy2, (np.sqrt(dx1**2 + dy2**2 + dz1**2) * dz1))
            - np.arctan2(dx2 * dy2, (np.sqrt(dx2**2 + dy2**2 + dz1**2) * dz1))
            + np.arctan2(dx1 * dy1, (np.sqrt(dx1**2 + dy1**2 + dz2**2) * dz2))
            - np.arctan2(dx2 * dy1, (np.sqrt(dx2**2 + dy1**2 + dz2**2) * dz2))
            - np.arctan2(dx1 * dy2, (np.sqrt(dx1**2 + dy2**2 + dz2**2) * dz2))
            + np.arctan2(dx2 * dy2, (np.sqrt(dx2**2 + dy2**2 + dz2**2) * dz2))
        )

    def Bzx_method(self, x, y, z):
        r"""Calculate magnetic field gradient :math:`B_{zx}`.

        :math:`B_{zx} \equiv \partial B_z / \partial x`
        [:math:`\mathrm{mT} \: \mathrm{nm}^{-1}`].
        The magnetic field gradient
        :math:`B_{zx} = \dfrac{\partial{B_z}}{\partial x}` is
        given by the following:

        .. math::
           B_{zx} = \dfrac{\mu_0 M_s}{4 \pi} \sum_{i=1}^2 \sum_{j=1}^2
               \sum_{k=1}^2(-1)^{i+j+k}
               \left( \dfrac{(y-y_j)(z-z_k)}{ R((x-x_i)^2 + (z-z_k)^2))}
               \right)

        As described above, :math:`(x,y,z)` are coordinates for the location
        at which we want to know the field gradient; the magnet spans from
        x1 to x2 in the ``x``-direction, y1 to y2 in the ``y``-direction, and
        from z1 to z2 in the ``z``-direction;

        .. math::
            R = \sqrt{(x - x_i) + (y - y_j) + (z - z_k)}

        :math:`\mu_0 M_s` is the magnet's saturation magnetization in mT.

        :param float x: ``x`` coordinate [nm]
        :param float y: ``y`` coordinate [nm]
        :param float z: ``z`` coordinate [nm]
        """

        dx1, dx2 = x - self._range[0], x - self._range[1]
        dy1, dy2 = y - self._range[2], y - self._range[3]
        dz1, dz2 = z - self._range[4], z - self._range[5]

        return self._pre_term * self._bzx(dx1, dx2, dy1, dy2, dz1, dz2)

    @staticmethod
    @nb.vectorize(
        [
            nb.float64(
                nb.float64,
                nb.float64,
                nb.float64,
                nb.float64,
                nb.float64,
                nb.float64,
            )
        ],
        nopython=True,
        target="parallel",
    )
    def _bzx(dx1, dx2, dy1, dy2, dz1, dz2):
        """Calculate the summation term for magnetic field gradient.

        Optimized with numba. See method bzx for the explanation.

        :param np.array dx1, dx2: distance between grid and the 2 ends of
            magnet in x direction [nm]
        :param np.array dy1, dy2: distance between grid and the 2 ends of
            magnet in y direction [nm]
        :param np.array dz1, dz2: distance between grid and the 2 ends of
            magnet in z direction [nm]
        """

        return (
            -dy1
            * dz1
            / (np.sqrt(dx1**2 + dy1**2 + dz1**2) * (dx1**2 + dz1**2))
            + dy1
            * dz1
            / (np.sqrt(dx2**2 + dy1**2 + dz1**2) * (dx2**2 + dz1**2))
            + dy2
            * dz1
            / (np.sqrt(dx1**2 + dy2**2 + dz1**2) * (dx1**2 + dz1**2))
            - dy2
            * dz1
            / (np.sqrt(dx2**2 + dy2**2 + dz1**2) * (dx2**2 + dz1**2))
            + dy1
            * dz2
            / (np.sqrt(dx1**2 + dy1**2 + dz2**2) * (dx1**2 + dz2**2))
            - dy1
            * dz2
            / (np.sqrt(dx2**2 + dy1**2 + dz2**2) * (dx2**2 + dz2**2))
            - dy2
            * dz2
            / (np.sqrt(dx1**2 + dy2**2 + dz2**2) * (dx1**2 + dz2**2))
            + dy2
            * dz2
            / (np.sqrt(dx2**2 + dy2**2 + dz2**2) * (dx2**2 + dz2**2))
        )

    def Bzxx_method(self, x, y, z):
        r"""Calculate magnetic field second derivative :math:`B_{zxx}`/

        :math:`B_{zxx} \equiv \partial^2 B_z / \partial x^2`
        [ :math:`\mathrm{mT} \; \mathrm{nm}^{-2}`]
        The magnetic field's second derivative is given by the following:

        .. math::
           B_{zxx} = \dfrac{\partial B_z}{\partial z}
               = \dfrac{\mu_0 M_s}{4 \pi} \sum_{i=1}^2
                   \sum_{j=1}^2 \sum_{k=1}^2(-1)^{i+j+k}
                   \left( \dfrac{-(x-x_i)(y-y_j)(z-z_k)
                   (3(x-x_i)^2 +2(y-y_j)^2 + 3(z-z_k)^2)}
                   {((x-x_i)^2 + (y-y_j)^2 + (z-z_k)^2)^{3/2}
                   ((x-x_i)^2 + (z-z_k)^2)^2} \right)

        with the variables defined above.
        :param float x: ``x`` coordinate [nm]
        :param float y: ``y`` coordinate [nm]
        :param float z: ``z`` coordinate [nm]
        """

        dx1, dx2 = x - self._range[0], x - self._range[1]
        dy1, dy2 = y - self._range[2], y - self._range[3]
        dz1, dz2 = z - self._range[4], z - self._range[5]

        return self._pre_term * self._bzxx(dx1, dx2, dy1, dy2, dz1, dz2)

    @staticmethod
    @nb.vectorize(
        [
            nb.float64(
                nb.float64,
                nb.float64,
                nb.float64,
                nb.float64,
                nb.float64,
                nb.float64,
            )
        ],
        nopython=True,
        target="parallel",
    )
    def _bzxx(dx1, dx2, dy1, dy2, dz1, dz2):
        """The summation term for the second derivative of magnetic field.

        Optimized by numba. See bzxx method for the explanation.
        :param float dx1, dx2: distance between grid and the one end of magnet
                        in x direction [nm]
        :param float dy1, dy2: distance between grid and the one end of magnet
                        in y direction [nm]
        :param float dz1, dz2: distance between grid and the one end of magnet
                        in z direction [nm]
        """

        return (
            +dx1
            * dy1
            * dz1
            * (3.0 * dx1**2 + 2.0 * dy1**2 + 3.0 * dz1**2)
            / ((dx1**2 + dy1**2 + dz1**2) ** 1.5 * (dx1**2 + dz1**2) ** 2)
            - dx2
            * dy1
            * dz1
            * (3.0 * dx2**2 + 2.0 * dy1**2 + 3.0 * dz1**2)
            / ((dx2**2 + dy1**2 + dz1**2) ** 1.5 * (dx2**2 + dz1**2) ** 2)
            - dx1
            * dy2
            * dz1
            * (3.0 * dx1**2 + 2.0 * dy2**2 + 3.0 * dz1**2)
            / ((dx1**2 + dy2**2 + dz1**2) ** 1.5 * (dx1**2 + dz1**2) ** 2)
            + dx2
            * dy2
            * dz1
            * (3.0 * dx2**2 + 2.0 * dy2**2 + 3.0 * dz1**2)
            / ((dx2**2 + dy2**2 + dz1**2) ** 1.5 * (dx2**2 + dz1**2) ** 2)
            - dx1
            * dy1
            * dz2
            * (3.0 * dx1**2 + 2.0 * dy1**2 + 3.0 * dz2**2)
            / ((dx1**2 + dy1**2 + dz2**2) ** 1.5 * (dx1**2 + dz2**2) ** 2)
            + dx2
            * dy1
            * dz2
            * (3.0 * dx2**2 + 2.0 * dy1**2 + 3.0 * dz2**2)
            / ((dx2**2 + dy1**2 + dz2**2) ** 1.5 * (dx2**2 + dz2**2) ** 2)
            + dx1
            * dy2
            * dz2
            * (3.0 * dx1**2 + 2.0 * dy2**2 + 3.0 * dz2**2)
            / ((dx1**2 + dy2**2 + dz2**2) ** 1.5 * (dx1**2 + dz2**2) ** 2)
            - dx2
            * dy2
            * dz2
            * (3.0 * dx2**2 + 2.0 * dy2**2 + 3.0 * dz2**2)
            / ((dx2**2 + dy2**2 + dz2**2) ** 1.5 * (dx2**2 + dz2**2) ** 2)
        )
