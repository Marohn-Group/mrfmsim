from mmodel.utility import param_sorter
from functools import wraps
from collections import defaultdict
import numba as nb
from mmodel.modifier import loop_input, zip_loop_inputs, profile_time
from inspect import Parameter, signature, Signature
from pprint import pformat


def replace_component(replacement: dict):
    """Modify the signature with components.

    The modifier is used on the model level, therefore inputs are keyword-only.

    :param dict[list | str] replacement: in the format of
        {component: [[original, replacement], original ...}
    """

    def modifier(func):
        sig = signature(func)
        params = sig.parameters  # immutable

        @wraps(func)
        def wrapped(**kwargs):
            for comp, rep_list in replacement.items():
                comp_obj = kwargs.pop(comp)

                for element in rep_list:
                    # allows simplified replacement
                    # if the replacement rep is the same as the sig
                    if isinstance(element, str):
                        attr = rep = element
                    else:
                        attr, rep = element

                    if attr in params:
                        # skip the attribute if it is not needed
                        # this allows the component modifier to be recycled
                        # even if the underlying function is changed
                        kwargs[attr] = getattr(comp_obj, rep)

            return func(**kwargs)

        params_dict = dict(params)  # mutable
        for comp, rep_list in replacement.items():
            params_dict[comp] = Parameter(comp, 1)

            for element in rep_list:
                if isinstance(element, str):
                    attr = element
                else:
                    attr = element[0]
                params_dict.pop(attr, None)

        wrapped.__signature__ = Signature(
            parameters=sorted(params_dict.values(), key=param_sorter)
        )
        return wrapped

    modifier.metadata = f"replace_component({pformat(replacement)})"
    return modifier


def print_inputs(inputs: list, stdout_format: str, end: str = "\n"):
    """Print the node input to the console.

    If the parameter is the result of the node, set the result parameter
    to True. Change the end string may allow printout to stay in one line.

    :param list parameter: parameter name
    :param str stdout_format: format string for input and output
        The format should be keyword only.
    :param str end: end of printout
    """

    def stdout_input_modifier(func):
        sig = signature(func)

        @wraps(func)
        def wrapped(*args, **kwargs):
            """Print input parameter."""
            arguments = sig.bind(*args, **kwargs).arguments
            input_dict = {k: arguments[k] for k in inputs}
            print(stdout_format.format(**input_dict), end=end)
            return func(**arguments)

        return wrapped

    stdout_input_modifier.metadata = (
        f"print_inputs({repr(inputs)}, {repr(stdout_format)}, {repr(end)})"
    )
    return stdout_input_modifier


def print_output(output: str, stdout_format: str, end: str = "\n"):
    """Print the node output to the console.

    If the parameter is the result of the node, set the result parameter
    to True.

    :param list parameter: parameter name
    :param str stdout_format: format string for input and output
        The format should be keyword only. The behavior is for keep the
        consistency with other print modifiers.
    :param str end: end of printout
    """

    def stdout_output_modifier(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            """Print output parameter."""

            result = func(*args, **kwargs)
            print(stdout_format.format(**{output: result}), end=end)
            return result

        return wrapped

    stdout_output_modifier.metadata = (
        f"print_output({repr(output)}, {repr(stdout_format)}, {repr(end)})"
    )
    return stdout_output_modifier


def print_parameters(inputs, output_dict, stdout_format):
    """Modifier for printout input and output.

    The modifier is a module level modifier, but it can be
    used at the node level. Note the modifier cannot output
    intermediate values in the model. Either use print_output
    add_modifier at node level, or change the model returns.

    :param list inputs: list of input parameters
    :param dict output_dict: (output, index) for returns
    :param str format: format string for input and output
        The format should be keyword only.
    """

    def stdout_output_modifier(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            """Print output parameter."""
            result = func(*args, **kwargs)

            arguments = signature(func).bind(*args, **kwargs).arguments
            input_dict = {k: arguments[k] for k in inputs}
            output_values = {k: result[v] for k, v in output_dict.items()}
            print(stdout_format.format(**input_dict, **output_values))
            return result

        return wrapped

    param_list = list(inputs) + list(output_dict.keys())
    stdout_output_modifier.metadata = (
        f"print_parameters: {repr(param_list)}, {repr(stdout_format)}"
    )
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
