from mrfmsim.formula.misc import convert_grid_pts, sum_of_product
import numpy as np
import pytest


def test_convert_grid_pts():
    """Test convert_grid_pts.

    Make sure the final value is an int and is the floor value."""

    assert convert_grid_pts(2, [1.5, 1, 1]) == 1
    assert convert_grid_pts(1.1, [1.1, 1, 1]) == 1


def test_sum_of_product():
    """Test sum_of_product.

    Make sure the final value is an int and is the floor value."""

    assert sum_of_product([1, 2, 3], [4, 5, 6], 3) == 96

    shape = (2, 2, 1)
    a = np.ones(shape)

    assert sum_of_product(a, 10) == 40
