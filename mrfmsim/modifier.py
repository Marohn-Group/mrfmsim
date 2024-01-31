from mmodel.utility import param_sorter
from functools import wraps
import numba as nb
from inspect import Parameter, signature, Signature
from pprint import pformat
from string import Formatter
from collections import defaultdict


def replace_component(replacement: dict):
    """Modify the signature with components.

    The modifier modifies the internal model function. The wrapper
    function is keyword-only.

    :param dict[list | str] replacement: in the format of
        {component: [[original, replacement], original ...}
    """

    def modifier(func):
        sig = signature(func)
        params = sig.parameters  # immutable

        new_params_dict = dict(params)  # mutable
        replacement_dict = defaultdict(list)
        for comp, rep_list in replacement.items():
            assert (
                comp not in params
            ), f"Parameter {repr(comp)} is already in the signature."
            new_params_dict[comp] = Parameter(comp, 1)

            for element in rep_list:
                if isinstance(element, str):
                    attr = element
                    replacement_dict[comp].append((attr, attr))
                else:
                    attr = element[0]
                    replacement_dict[comp].append(element)
                new_params_dict.pop(attr, None)

        @wraps(func)
        def wrapped(**kwargs):
            for comp, rep_list in replacement_dict.items():
                comp_obj = kwargs.pop(comp)
                for param, repl in rep_list:
                    kwargs[param] = getattr(comp_obj, repl)

            return func(**kwargs)

        wrapped.__signature__ = Signature(
            parameters=sorted(new_params_dict.values(), key=param_sorter)
        )
        return wrapped

    modifier.metadata = f"replace_component({pformat(replacement)})"
    return modifier


def parse_fields(format_str):
    """Parse the field from the format string.

    :param str format_str: format string
    :return: list of fields

    The function parses out the field names in the format string.
    Some field names have slicers or attribute access, such as
    B0.value, B0[0], B0[0:2]. The function only returns B0 for all
    these fields. Since there can be duplicated fields after the
    name split, the function returns unique elements.
    """

    # this is a internal function for Formatter
    # consider rewrite with custom function to prevent breaking
    # the function ignores slicing and attribute access
    # B0.value -> B0, B0[0] -> B0
    from _string import formatter_field_name_split

    fields = [
        formatter_field_name_split(field)[0]
        for _, field, _, _ in Formatter().parse(format_str)
        if field
    ]
    return list(set(fields))  # return unique elements


def print_inputs(stdout_format: str, **pargs):
    """Print the node input to the console.

    :param str stdout_format: format string for input and output
        The format should be keyword only.
    :param pargs: keyword arguments for the print function

    The names of the parameters are parsed from the format string.
    """

    def stdout_inputs_modifier(func):
        inputs = parse_fields(stdout_format)

        @wraps(func)
        def wrapped(**kwargs):
            """Print input parameter."""
            input_dict = {k: kwargs[k] for k in inputs}
            print(stdout_format.format(**input_dict), **pargs)
            return func(**kwargs)

        return wrapped

    params = [repr(stdout_format)] + [f"{k}={repr(v)}" for k, v in pargs.items()]
    stdout_inputs_modifier.metadata = f"print_inputs({', '.join(params)})"
    return stdout_inputs_modifier


def print_output(stdout_format: str, **pargs):
    """Print the node output to the console.

    :param str stdout_format: format string for input and output
        The format should be keyword only. The behavior is for keeping the
        consistency with other print modifiers.
    :param str end: end of printout

    The names of the parameters are parsed from the format string. The
    use of the stdout_format is different from the input method, as
    the modifiers do not know the return name of the node. Only one
    output field is allowed and the field name is used as the return name.
    """

    def stdout_output_modifier(func):
        output = parse_fields(stdout_format)[0]

        @wraps(func)
        def wrapped(**kwargs):
            """Print output parameter."""

            result = func(**kwargs)
            print(stdout_format.format(**{output: result}), **pargs)
            return result

        return wrapped

    params = [repr(stdout_format)] + [f"{k}={repr(v)}" for k, v in pargs.items()]
    stdout_output_modifier.metadata = f"print_output({', '.join(params)})"
    return stdout_output_modifier


def numba_jit(**kwargs):
    """Numba jit modifier with keyword arguments.

    Add metadata to numba.jit. The numba decorator outputs
    all the parameters make it hard to read.
    Use the decorator the same way as numba.jit().
    """

    def decorator(func):
        func = nb.jit(**kwargs)(func)
        return func

    meta = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    decorator.metadata = f"numba_jit({meta})"
    return decorator
