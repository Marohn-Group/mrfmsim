from mrfmsim.modifier import replace_component, numba_jit
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
        """Test component modified function has the correct signature and order."""

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
            comp_mod.metadata == "replace_component({'obj1': ['a', 'b']"
            ", 'obj2': ['c', 'd']})"
        )

    # test name duplication behaviors

    def test_duplicated_parameter(self):
        """Test component parameter already exists in function."""

        def func(a, b, obj):
            return a + b, obj

        with pytest.raises(
            AssertionError, match="parameter 'obj' already in the signature"
        ):
            replace_component({"obj": ["a", "b"]})(func)

    def test_self_parameter(self):
        """Test component parameter with duplicated component name.

        THe function should allow signature that already exists.
        """

        def func(a, b, obj):
            return a + b, obj

        mod = replace_component({"obj": ["a", "b"]}, True)
        sig_parameters = list(inspect.signature(mod(func)).parameters.keys())
        assert sig_parameters == ["obj"]

        obj = SimpleNamespace(a=1, b=2)
        mod_func = mod(func)

        assert mod(func)(obj=obj) == (3, obj)

    def test_self_parameter_with_duplicated(self):
        """Test component parameter with duplicated attribute.

        The function should raise an error.
        """

        def func(a, b, obj):
            return a + b, obj

        with pytest.raises(
            ValueError, match="attribute name cannot be the same as component 'obj'"
        ):
            replace_component({"obj": ["a", "b", "obj"]}, True)(func)

        with pytest.raises(
            AssertionError, match="parameter 'obj' already in the signature"
        ):
            replace_component({"obj": ["a", "b", "obj"]}, False)(func)


def test_numba_jit():
    """Test the numba_jit decorator modifier."""

    mod = numba_jit(nopython=True, parallel=True)

    def func(x):
        return x

    assert mod.metadata == "numba_jit(nopython=True, parallel=True)"
    assert mod(func)(1) == 1
