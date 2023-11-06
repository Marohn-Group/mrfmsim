from textwrap import dedent


def test_node_str(experiment):
    """Test if the node adds the output_unit in the string output."""

    node_str = """\
    multiply

    multiply(e, g)
    return: k
    return_unit: m^2
    functype: numpy.ufunc

    Multiply arguments element-wise."""

    assert str(experiment.get_node_obj("multiply")) == dedent(node_str)


def test_node_str_unitless(experiment):
    """Test if the node string ignores return_unit if output_unit is not defined."""

    node_str = """\
    subtract

    sub(c, d)
    return: e
    functype: builtin_function_or_method

    Same as a - b."""

    assert str(experiment.get_node_obj("subtract")) == dedent(node_str)
