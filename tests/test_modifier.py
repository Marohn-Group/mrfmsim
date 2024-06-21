from mrfmsim.modifier import (
    replace_component,
    print_inputs,
    print_output,
    numba_jit,
    parse_fields,
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

    def test_duplicated_parameter(self, func):
        """Test component parameter already exists in function."""

        with pytest.raises(
            AssertionError, match="Parameter 'a' is already in the signature"
        ):
            replace_component({"a": [("b", "a")]})(func)


class TestPrintModifiers:
    @pytest.fixture
    def func(self):
        def b_tot(b1, b0, bz):
            return b1 + b0 + bz

        return b_tot

    def test_parse_field_with_attributes_or_slicers(self):
        """Test the parse_field that can parse field with attributes or slicers."""

        assert sorted(parse_fields("{b0[0]} [mT] b0 {b0[1]:.3e} [mT] {b1.value}")) == [
            "b0",
            "b1",
        ]

    def test_parse_field(self):
        """Test the parse_field function."""

        assert sorted(
            parse_fields("b1 {b1:.3f} [mT] b0 {b0:.3e} [mT] bz {bz} [mT]")
        ) == [
            "b0",
            "b1",
            "bz",
        ]

    def test_print_inputs(self, capsys, func):
        """Test the print_inputs."""

        mod = print_inputs("b1 {b1:.3f} [mT] b0 {b0:.3e} [mT] bz {bz}", end="--")
        mod_func = mod(func)
        mod_func(b1=1, b0=2, bz=3)
        captured = capsys.readouterr()
        assert captured.out == "b1 1.000 [mT] b0 2.000e+00 [mT] bz 3--"
        assert (
            mod.metadata == "print_inputs(format_str='b1 {b1:.3f} "
            "[mT] b0 {b0:.3e} [mT] bz {bz}', end='--')"
        )

    def test_print_output_modifier(self, capsys, func):
        """Test the stdout_output_modifier."""

        mod = print_output("b_tot {b_tot:.1f} [mT]")
        mod_func = mod(func)
        mod_func(b1=1, b0=2, bz=3)
        captured = capsys.readouterr()
        assert captured.out == "b_tot 6.0 [mT]\n"
        assert mod.metadata == "print_output(format_str='b_tot {b_tot:.1f} [mT]')"


def test_numba_jit():
    """Test the numba_jit decorator modifier."""

    mod = numba_jit(nopython=True, parallel=True)

    def func(x):
        return x

    assert mod.metadata == "numba_jit(nopython=True, parallel=True)"
    assert mod(func)(1) == 1
