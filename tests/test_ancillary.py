from mrfmsim.ancillary import execute
import numpy as np


def test_execute():
    """Test if execute works with numpy functions."""

    result = execute(np.dot, a=np.array([1, 2]), b=np.array([3, 4]))

    assert result == 11
