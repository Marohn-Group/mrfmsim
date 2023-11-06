from mrfmsim.modifier import (
    replace_component,
    print_inputs,
    print_output,
    numba_jit,
    print_parameters,
)
import inspect
import pytest
from types import SimpleNamespace


class TestReplaceComponent:
    @pytest.fixture
    def comp_mod(self):
        """Return a component modified function."""

        return replace_component(
            {"obj1": ["a", ("b", "b1")], "obj2": [("c", "c2"), "d"]}
        )

    @pytest.fixture
    def func(self):
        def func(a, b, c, d, e, f):
            return a * b * c * d * e * f

        return func

    def test_signature(self, func, comp_mod):
        """Test component modified function has the correct signature and order."""

        sig_parameters = list(inspect.signature(comp_mod(func)).parameters.keys())
        assert sig_parameters == ["e", "f", "obj1", "obj2"]

    def test_execution(self, func, comp_mod):
        """Test component modified function to process the correct input."""

        obj1 = SimpleNamespace(a=1, b1=2)
        obj2 = SimpleNamespace(c2=3, d=4)

        assert comp_mod(func)(e=5, f=6, obj1=obj1, obj2=obj2) == 720

    def test_metadata(self, comp_mod):
        """Test component modified function has the correct metadata."""

        assert (
            comp_mod.metadata == "replace_component({'obj1': ['a', ('b', 'b1')]"
            ", 'obj2': [('c', 'c2'), 'd']})"
        )


class TestPrintModifiers:
    @pytest.fixture
    def func(self):
        def b_tot(b1, b0, bz):
            return b1 + b0 + bz

        return b_tot

    def test_print_inputs(self, capsys, func):
        """Test the print_inputs."""

        mod_func = print_inputs(
            ["b1", "b0", "bz"], "b1 {b1:.3f} [mT] b0 {b0:.3e} [mT] bz {bz}", end="--"
        )(func)
        mod_func(b1=1, b0=2, bz=3)
        captured = capsys.readouterr()
        assert captured.out == "b1 1.000 [mT] b0 2.000e+00 [mT] bz 3--"

    def test_print_output_modifier(self, capsys, func):
        """Test the stdout_output_modifier."""

        mod_func = print_output("b_tot", "b_tot {b_tot:.1f} [mT]")(func)
        mod_func(b1=1, b0=2, bz=3)
        captured = capsys.readouterr()
        assert captured.out == "b_tot 6.0 [mT]\n"

    def test_print_parameters(self, capsys):
        """Test the print_parameters."""

        mod_func = print_parameters(["a"], {"b": 1}, "a={a:.1f} b={b}")(
            lambda a: (a**2, a * 2)
        )
        mod_func(a=1)
        captured = capsys.readouterr()
        assert captured.out == "a=1.0 b=2\n"

    def test_metadata(self):
        """Test printout modified function has the correct metadata."""
        assert (
            print_inputs(
                ["b1", "b0", "bz"], "b1 {b1:.3f} [mT] b0 {b0:.3e} [mT] bz {bz}", "--"
            ).metadata
            == "print_inputs(['b1', 'b0', 'bz'], 'b1 {b1:.3f}"
            " [mT] b0 {b0:.3e} [mT] bz {bz}', '--')"
        )
        assert (
            print_output("b_tot", "{b_tot:.1f} [mT]").metadata
            == "print_output('b_tot', '{b_tot:.1f} [mT]', '\\n')"
        )

        assert (
            print_parameters(["a"], {"b": 1}, "a={a} b={b}").metadata
            == "print_parameters: ['a', 'b'], 'a={a} b={b}'"
        )


def test_numba_jit():
    """Test the numba_jit decorator modifier."""

    mod = numba_jit(nopython=True, parallel=True)

    def func(x):
        return x

    assert mod.metadata == "numba_jit(nopython=True, parallel=True)"
    assert mod(func)(1) == 1
