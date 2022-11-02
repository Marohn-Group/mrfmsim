from mrfmsim.ancillary import run_method
import numpy as np


def test_run_method():
    """Test if run method works with numpy functions"""
    result = run_method(np.dot, a=np.array([1, 2]), b=np.array([3, 4]))
    assert result == 11
