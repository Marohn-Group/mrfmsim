"""Ancillary functions to help node definition"""


def execute(method, **kwargs):
    """Execute given method.

    Keyword arguments only. The use case is when the method is a user
    input instead of built-in the graph.
    """
    return method(**kwargs)
