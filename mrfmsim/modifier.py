from mmodel.utility import replace_signature
from functools import wraps
import inspect
from collections import defaultdict


def component_modifier(func, component_substitutes):
    """Modify the signature with components"""

    @wraps(func)
    def wrapped(**kwargs):

        for component, substitutes in component_substitutes.items():
            component_obj = kwargs.pop(component)
            for attr in substitutes:

                kwargs[attr] = getattr(component_obj, attr)

        return func(**kwargs)

    sig = inspect.signature(func)
    wrapped.__signature__ = replace_signature(sig, component_substitutes)

    return wrapped


def stdout_modifier(func, variables: list = [], result: bool = True, units: dict = {}):
    """Print the variables and the result to console of a specific node

    The modifier is helpful to output looped node input and outputs. The
    function return are automatically printed out.
    The units parameters should be attached to individual experiment.
    If the attribute is not found, then no units are printed.

    :param list variables: list of variables to print out
        defaults to empty list. (Only result is printed)
    :param dict units: dictionary of units and display format
    """

    formats = {}
    func_sig = inspect.signature(func).parameters
    # units = units or getattr(func, 'units', {})

    for val in variables:
        if val not in func_sig:
            raise Exception(f"cannot modify {func.__name__}, {val} not in signature")
        des = units.get(val, defaultdict(str))
        form = "{} {{{}}} {}".format(val, des["format"], des["unit"])
        formats[val] = form

    if hasattr(func, "returns") and result:
        rt_length = len(func.returns)
        form_list = []
        for val_name in func.returns:
            des = units.get(val_name, defaultdict(str))
            form_list.append(
                "{} {{{}}} {}".format(val_name, des["format"], des["unit"])
            )
        form = ", ".join(form_list)
    elif not result: # force no output
        rt_length = 1
        form = ""
    else:  # if function has no "returns" attribute the returns are outputted together
        rt_length = 0
        form = "{}"

    formats["result"] = form

    @wraps(func)
    def wrapped(**kwargs):
        """print format is 'count vars | result'"""
        print(wrapped.count, end=" | ")
        for val in variables:
            print(formats[val].format(kwargs[val]).rstrip(), end=" | ")

        result = func(**kwargs)
        if rt_length < 2:
            print(formats["result"].format(result).rstrip())
        else:  # if there is more than 1 returns, need to unzip result
            print(formats["result"].format(*result).rstrip())
        wrapped.count += 1

        return result

    wrapped.count = 0
    return wrapped
