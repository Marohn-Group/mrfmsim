from mmodel.utility import replace_signature_with_object
from functools import wraps
import inspect
from collections import defaultdict


def replace_component(replacement: dict):
    """Modify the signature with components."""

    def modifier(func):
        sig = inspect.signature(func)
        params = sig.parameters

        @wraps(func)
        def wrapped(**kwargs):

            for component, substitutes in replacement.items():
                component_obj = kwargs.pop(component)
                for attr in substitutes:
                    # skip the attribute if it is not needed
                    # this allows the component modifier to be recycled
                    # even if the underlying function is changed
                    if attr in params:
                        kwargs[attr] = getattr(component_obj, attr)

            return func(**kwargs)

        wrapped.__signature__ = replace_signature_with_object(sig, replacement)
        return wrapped
    
    modifier.metadata = f"replace_component({replacement})"
    return modifier


def parse_format(parameter, units):
    """Parse parameter description from units dictionary.

    The function is used for stdout modifiers.
    """

    des = units.get(parameter, defaultdict(str))
    form = "{} {{{}}} {}".format(parameter, des["format"], des["unit"])
    return form


def print_inputs(inputs: list, units: dict = {}, end: str = "\n"):
    """Print the node input to the console.

    If the parameter is the result of the node, set the result parameter
    to True.

    :param list parameter: parameter name
    :param dict units: a dictionary of units and display format
    """

    def stdout_input_modifier(func):
        func_sig = inspect.signature(func).parameters
        form_dict = {}
        for val in inputs:
            if val not in func_sig:
                raise Exception(
                    f"Invalid parameter: {repr(val)} not in {func.__name__} signature."
                )
            form_dict[val] = parse_format(val, units)

        @wraps(func)
        def wrapped(**kwargs):
            """Print input parameter."""
            for val in inputs:
                print(form_dict[val].format(kwargs[val]).rstrip(), end=end)
            return func(**kwargs)

        return wrapped
    # skip the long unit dictionary printout
    stdout_input_modifier.metadata = f"print_inputs({repr(inputs)})"
    return stdout_input_modifier


def print_output(output: str, units: dict = {}, end: str = "\n"):
    """Print the node output to the console.

    If the parameter is the result of the node, set the result parameter
    to True.

    :param list parameter: parameter name
    :param dict units: a dictionary of units and display format
    """
    def stdout_output_modifier(func):


        form = parse_format(output, units)

        @wraps(func)
        def wrapped(**kwargs):
            """Print output parameter."""

            result = func(**kwargs)
            print(form.format(result).rstrip(), end=end)
            return result

        return wrapped
    stdout_output_modifier.metadata = f"print_output({repr(output)})"
    return stdout_output_modifier
