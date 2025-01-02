from mrfmsim.formula.math import slice_matrix, as_strided_x
import numpy as np
import pytest


def test_slice_matrix():
    """Test slice matrix cuts the matrix in the center."""

    matrix = np.array(
        [[1, 2, 3, 4, 5], [11, 22, 33, 44, 55], [111, 222, 333, 444, 555]]
    )

    assert np.array_equal(
        slice_matrix(matrix, (3, 3)),
        np.array([[2, 3, 4], [22, 33, 44], [222, 333, 444]]),
    )
    assert np.array_equal(slice_matrix(matrix, (1, 3)), np.array([[22, 33, 44]]))

    # check that the slice matrix is a view of the original
    assert np.shares_memory(slice_matrix(matrix, (1, 3)), matrix)


def test_as_strided_x():
    """Testing if as_strided_x maximum matches running max."""

    matrix_a = np.random.rand(30, 20, 10)
    window = 10

    new_shape = (
        matrix_a.shape[0] - window + 1,
        matrix_a.shape[1],
        matrix_a.shape[2],
    )
    # running maximum with a python loop
    result = np.zeros(new_shape)
    for i in range(result.shape[0]):
        result[i, ...] = np.amax(matrix_a[i : i + window, ...], axis=0)

    # running maximum calculated with strided_axis0
    strided_result = as_strided_x(matrix_a, window).max(axis=1)

    assert np.array_equal(result, strided_result)
