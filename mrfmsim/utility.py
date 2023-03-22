from collections import defaultdict


def parse_format(parameter, units):
    """Parse parameter description from units dictionary."""

    des = units.get(parameter, defaultdict(str))
    form = "{} {{{}}} {}".format(parameter, des["format"], des["unit"])
    return form
