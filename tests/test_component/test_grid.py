#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test mrfmsim.components.grid module."""

import numpy as np
import pytest
from mrfmsim.component import Grid
from textwrap import dedent


class TestGrid:
    @pytest.fixture
    def grid(self):
        """Standard grid."""
        return Grid(
            grid_shape=(11, 5, 9),
            grid_step=[1.10, 0.40, 1.10],
            grid_origin=[1.0, 1.0, 1.0],
        )

    def test_str(self, grid):
        """Test grid str."""

        grid_str = """\
        Grid
          grid_shape = (11, 5, 9)
          grid_step = [1.1, 0.4, 1.1] nm
          grid_origin = [1.0, 1.0, 1.0] nm
          grid_voxel = 0.484 nm^3
          grid_range = [11.0, 1.6, 8.8] nm
          grid_length = [12.1, 2.0, 9.9] nm"""

        assert str(grid) == dedent(grid_str)

    def test_grid_voxel(self, grid):
        """Test attribute grid voxel."""

        assert grid.grid_voxel == 1.1 * 0.40 * 1.1

    def test_grid_range(self, grid):
        """Test grid range."""

        assert np.array_equal(grid.grid_range, np.array([11.0, 1.6, 8.8]))

    def test_grid_length(self, grid):
        """Test grid length."""

        assert np.allclose(grid.grid_length, np.array([12.1, 2.0, 9.9]), rtol=1e-15)

    def test_grid_array(self, grid):
        """Test grid values.

        The grid array should match the shape and value
        """

        assert len(grid.grid_array) == 3

        # test grid values
        grid_x = np.array([-4.5, -3.4, -2.3, -1.2, -0.1, 1.0, 2.1, 3.2, 4.3, 5.4, 6.5])
        grid_y = np.array([0.2, 0.6, 1.0, 1.4, 1.8])
        grid_z = np.array([-3.4, -2.3, -1.2, -0.1, 1.0, 2.1, 3.2, 4.3, 5.4])

        assert np.allclose(
            grid.grid_array[0], grid_x.reshape(11, 1, 1), rtol=1e-15, atol=1e-15
        )
        assert np.allclose(
            grid.grid_array[1], grid_y.reshape(1, 5, 1), rtol=1e-15, atol=1e-15
        )
        assert np.allclose(
            grid.grid_array[2], grid_z.reshape(1, 1, 9), rtol=1e-15, atol=1e-15
        )

    def test_grid_extents_method(self):
        """Test grid extents calculation as a staticmethod."""

        length = np.array([2, 4, 6])
        origin = np.array([3, 4, 5])
        assert np.array_equal(
            Grid.grid_extents_method(length, origin), [[2, 4], [2, 6], [2, 8]]
        )

    def test_extend_grid_by_pts(self, grid):
        """Test test_extend_xgrid_by_pts."""

        grid_x = np.array(
            [-5.6, -4.5, -3.4, -2.3, -1.2, -0.1, 1.0, 2.1, 3.2, 4.3, 5.4, 6.5, 7.6]
        )

        ext_grid_array = grid.extend_grid_by_points([1, 0, 0])
        assert len(ext_grid_array) == 3
        assert np.allclose(
            ext_grid_array[0], grid_x.reshape(13, 1, 1), rtol=1e-15, atol=1e-15
        )
        assert np.array_equal(ext_grid_array[1], grid.grid_array[1])
        assert np.array_equal(ext_grid_array[2], grid.grid_array[2])

    def test_extend_grid_by_length(self, grid):
        """Test extend_xgrid_by_length."""

        grid_x = np.array(
            [-5.6, -4.5, -3.4, -2.3, -1.2, -0.1, 1.0, 2.1, 3.2, 4.3, 5.4, 6.5, 7.6]
        )

        ext_grid_array = grid.extend_grid_by_length([1.2, 0, 0])
        assert len(ext_grid_array) == 3
        assert np.allclose(
            ext_grid_array[0], grid_x.reshape(13, 1, 1), rtol=1e-15, atol=1e-15
        )
        assert np.array_equal(ext_grid_array[1], grid.grid_array[1])
        assert np.array_equal(ext_grid_array[2], grid.grid_array[2])
