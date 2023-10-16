from mrfmsim.modifier import (
    replace_component,
    print_inputs,
    print_output,
    numba_jit
)
import inspect
import pytest
from types import SimpleNamespace


class TestReplaceComponent:
    @pytest.fixture
    def comp_mod(self):
        """Return a component modified function."""

        return replace_component({"obj1": ["a", "b"], "obj2": ["c", "d"]})

    @pytest.fixture
    def func(self):
        def func(a, b, c, d, e, f):
            return a * b * c * d * e * f

        return func

    def test_signature(self, func, comp_mod):
        """Test component modified function has the correct signature and order"""

        sig_parameters = list(inspect.signature(comp_mod(func)).parameters.keys())
        assert sig_parameters == ["e", "f", "obj1", "obj2"]

    def test_execution(self, func, comp_mod):
        """Test component modified function to process the correct input."""

        obj1 = SimpleNamespace(a=1, b=2)
        obj2 = SimpleNamespace(c=3, d=4)

        assert comp_mod(func)(e=5, f=6, obj1=obj1, obj2=obj2) == 720

    def test_metadata(self, comp_mod):
        """Test component modified function has the correct metadata."""

        assert (
            comp_mod.metadata
            == "replace_component({'obj1': ['a', 'b'], 'obj2': ['c', 'd']})"
        )


class TestPrintoutModifier:
    @pytest.fixture
    def func(self):
        def b_tot(b1, b0, bz):
            return b1 + b0 + bz

        return b_tot

    def test_print_inputs(self, capsys, func, units):
        """Test the print_inputs."""

        mod_func = print_inputs(["b1", "b0", "bz"], units=units, end="--")(func)
        mod_func(b1=1, b0=2, bz=3)
        captured = capsys.readouterr()
        assert captured.out == "b1 1.000 [mT]--b0 2.000e+00 [mT]--bz 3--"

    def test_print_inputs_incorrect_input(self, func, units):
        """Test printout modified to function with multiple returns."""

        with pytest.raises(
            Exception, match="Invalid parameter: 'f_rf' not in b_tot signature."
        ):
            print_inputs(["b1", "b0", "f_rf"], units)(func)

    def test_print_output_modifier(self, capsys, func, units):
        """Test the stdout_output_modifier."""

        mod_func = print_output("b_tot", units=units, end="---")(func)
        mod_func(b1=1, b0=2, bz=3)
        captured = capsys.readouterr()
        assert captured.out == "b_tot 6.0 [mT]---"

    def test_metadata(self, units):
        """Test printout modified function has the correct metadata."""
        assert (
            print_inputs(["b1", "b0", "bz"], units=units, end="--").metadata
            == "print_inputs(['b1', 'b0', 'bz'])"
        )
        assert (
            print_output("b_tot", units=units, end="---").metadata
            == "print_output('b_tot')"
        )

def test_numba_jit():
    """Test the numba_jit decorator modifier."""

    mod = numba_jit(nopython=True, parallel=True)

    def func(x):
        return x

    assert mod.metadata == "numba_jit(nopython=True, parallel=True)"
    assert mod(func)(1) == 1
