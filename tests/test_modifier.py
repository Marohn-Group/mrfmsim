from mrfmsim.modifier import (
    component_modifier,
    stdout_input_modifier,
    stdout_output_modifier,
)
import inspect
import pytest
from types import SimpleNamespace


class TestComponentModifier:
    @pytest.fixture
    def comp_mod_func(self):
        """Return a component modified function."""

        def func(a, b, c, d, e, f):
            return a * b * c * d * e * f

        return component_modifier(func, {"obj1": ["a", "b"], "obj2": ["c", "d"]})

    def test_signature(self, comp_mod_func):
        """Test component modified function has the correct signature and order"""

        sig_parameters = list(inspect.signature(comp_mod_func).parameters.keys())
        assert sig_parameters == ["e", "f", "obj1", "obj2"]

    def test_execution(self, comp_mod_func):
        """Test component modified function to process the correct input."""

        obj1 = SimpleNamespace(a=1, b=2)
        obj2 = SimpleNamespace(c=3, d=4)

        assert comp_mod_func(e=5, f=6, obj1=obj1, obj2=obj2) == 720


class TestStdoutModifier:
    @pytest.fixture
    def func(self):
        def b_tot(b1, b0, bz):
            return b1 + b0 + bz

        return b_tot

    def test_stdout_input_modifier(self, capsys, func, units):
        """Test the stdout_input_modifier."""

        mod_func = stdout_input_modifier(func, ["b1", "b0", "bz"], units=units)
        mod_func(b1=1, b0=2, bz=3)
        captured = capsys.readouterr()
        assert captured.out == "b1 1.000 [mT]\nb0 2.000e+00 [mT]\nbz 3\n"

    def test_stdout_input_incorrect_input(self, func, units):
        """Test printout modified to function with multiple returns."""

        with pytest.raises(
            Exception, match="Invalid parameter: 'f_rf' not in b_tot signature."
        ):
            stdout_input_modifier(func, ["b1", "b0", "f_rf"], units)

    def test_stdout_output_modifier(self, capsys, func, units):
        """Test the stdout_output_modifier."""

        mod_func = stdout_output_modifier(func, 'b_tot', units=units)
        mod_func(b1=1, b0=2, bz=3)
        captured = capsys.readouterr()
        assert captured.out == "b_tot 6.0 [mT]\n"
        

    # def test_no_result(self, capsys, func, units):
    #     """Test that modifier function returns if result=False."""

    #     mod_func = stdout_modifier(func, ["b1", "b0", "bz"], result=False, units=units)
    #     mod_func(b1=1, b0=2, bz=3)
    #     captured = capsys.readouterr()
    #     assert captured.out == "0 | b1 1.000 [mT] | b0 2.000e+00 [mT] | bz 3 | \n"

    # def test_no_returns_attr(self, capsys, func, units):
    #     """Test printout modified function has the correct output.

    #     Test variables that is in the units.yaml file and variable
    #     that is not. The function does not have a return parameter,
    #     therefore the result does not have units.
    #     """

    #     mod_func = stdout_modifier(func, ["b1", "b0", "bz"], units=units)

    #     mod_func(b1=1, b0=2, bz=3)
    #     captured = capsys.readouterr()
    #     assert captured.out == "0 | b1 1.000 [mT] | b0 2.000e+00 [mT] | bz 3 | 6\n"

    #     # test that the counter is increased
    #     mod_func(b1=2, b0=1, bz=0)
    #     captured = capsys.readouterr()
    #     assert captured.out == "1 | b1 2.000 [mT] | b0 1.000e+00 [mT] | bz 0 | 3\n"

    # def test_single_return(self, capsys, func, units):
    #     """Test printout modified function has the correct output with one returns."""

    #     func.returns = ["b_tot"]

    #     mod_func = stdout_modifier(func, [], units=units)

    #     mod_func(b1=1, b0=2, bz=3)

    #     captured = capsys.readouterr()
    #     assert captured.out == "0 | b_tot 6.0 [mT]\n"

    # def test_multiple_returns(self, capsys, units):
    #     """Test printout modified function with multiple returns."""

    #     def func(a, b):
    #         return a, b

    #     func.returns = ["b1", "b0"]

    #     mod_func = stdout_modifier(func, [], units=units)

    #     mod_func(a=1, b=2)

    #     captured = capsys.readouterr()
    #     assert captured.out == "0 | b1 1.000 [mT], b0 2.000e+00 [mT]\n"

    #     def func(a, b):
    #         return a, b

    #     func.returns = ["bz", "b0"]

    #     mod_func = stdout_modifier(func, [], units=units)

    #     mod_func(a=1, b=2)

    #     captured = capsys.readouterr()
    #     assert captured.out == "0 | bz 1 , b0 2.000e+00 [mT]\n"
