"""Shortcuts

The shortcut should work for both the Model and the Experiment classes.
"""

from mmodel.modifier import loop_input
from mmodel.utility import modelgraph_signature, modelgraph_returns
from mrfmsim import Node
from networkx.utils import nodes_equal
from mrfmsim.modifier import print_inputs, print_output, print_parameters
import networkx as nx


def print_shortcut(model, parameters, stdout_format):
    """Shortcut to printout parameters.

    The shortcut facilitates creation of model level modifier.
    Since modifier cannot access the node information, shortcut
    is a good way to modify the modifiers.

    The printout shortcut determines if the parameters is
    a input or output at the model level and output based on
    the format. Intermediate values are not accessible, change the
    returns of the model or add print_output modifier to the node.
    """

    G = model.graph
    G_returns = modelgraph_returns(G)
    sig = modelgraph_signature(G)
    inputs = set(sig.parameters) & set(parameters)
    outputs = set(G_returns) & set(parameters)
    output_dict = {k: G_returns.index(k) for k in outputs}

    modifiers = model.modifiers + [print_parameters(inputs, output_dict, stdout_format)]
    return model.edit(modifiers=modifiers)


def loop_shortcut(model, parameter: str, name=None):
    """Shortcut to add a loop to a subgraph.

    The parameter needs to be in the graph signature. Otherwise
    exception is raised. For parameters that are not from the
    graph (generated by modifiers), use regular loops or change
    modifiers.

    :param model: executable model
    :param str parameter: loop parameter
    :param str name: name of the new model, defaults to old model name.
    :return: a new model with looped parameter
    """
    # check if the parameter is in the signature
    if parameter not in model.signature.parameters:
        raise Exception(f"Invalid shortcut: {repr(parameter)} is not a model input.")

    G = model.graph
    name = name or model.name
    modifiers = model.modifiers
    components = model.components

    loop_mod = loop_input(parameter)

    # If the parameter is in the signature but not in the graph.
    # This is due to the signature modifier on the model.
    # Use regular loop or change the modifiers.

    if parameter not in modelgraph_signature(G).parameters:
        raise Exception(
            f"{repr(parameter)} is not included in the graph."
            f" Use regular loop or change the modifier."
        )

    H = G.subgraph(inputs=[parameter])

    if nodes_equal(G.nodes, H.nodes):
        modifiers = [*modifiers, loop_mod]

    elif len(H.nodes()) == 1:
        node = list(H.nodes)[0]
        # if the looped node is only one node
        # add loop modifier to node attribute
        node_modifiers = H.nodes[node]["node_obj"].modifiers
        node_modifiers = [*node_modifiers, loop_mod]
        G = G.edit_node(node, modifiers=node_modifiers)

    else:  # if there is more than one node
        sub_name = f"subnode_{parameter}"
        sub_des = (
            f"Submodel generated by loop_shortcut for parameter {repr(parameter)}."
        )
        output = ", ".join(modelgraph_returns(H))
        # create the model and substitute the subgraph
        looped_node = type(model)(
            f"submodel_{parameter}", H, model.handler, doc=sub_des
        )

        G = G.replace_subgraph(
            H, Node(sub_name, looped_node, output=output, modifiers=[loop_mod])
        )

    return model.edit(name=name, graph=G, modifiers=modifiers, components=components)
