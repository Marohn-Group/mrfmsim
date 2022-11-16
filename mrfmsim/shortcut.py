"""Shortcuts

The shortcut should work for both Model and Experiment
"""

from mmodel import (
    loop_modifier,
    subgraph_by_parameters,
    modify_subgraph,
    modify_node,
    model_signature,
    model_returns,
)
from networkx.utils import nodes_equal
from mrfmsim.modifier import stdout_modifier


def loop_shortcut(model, parameter: str, stdout: dict = None):
    """Shortcut to add loop to a subgraph

    :param model: executable model
    :param str parameter: loop parameter
    :param dict stdout: stdout_modifier keyword arguments
        values, result and unit
    :return: a new model with looped parameter
    """
    # check if the parameter is in the signature
    if parameter not in model.__signature__.parameters:
        raise Exception(f"'{parameter}' is not a model parameter")

    name = model.__name__
    handler = model.handler
    graph = model.graph
    modifiers = model.modifiers
    node_name = f"{parameter}_loop_node"
    description = model.description

    ModelClass = type(model)  # works for both mmodel.Model and mrfmsim.Experiment

    loop_mod = loop_modifier, {"parameter": parameter}
    if stdout is not None:  # accept empty dictionary input
        if stdout.get('parameters', None) is None:
            stdout['parameters'] = [parameter]
        combined_mod = [(stdout_modifier, stdout), loop_mod]
    else:
        combined_mod = [loop_mod]
    # this is case when the parameter is in signature but not in graph
    # this is due to signature modifier on the model level
    # therefore the whole model is looped.

    if parameter not in model_signature(graph).parameters:
        modifiers = modifiers + combined_mod
        name = f"{name}_loop_{parameter}"

    else:  # the parameter is within the graph

        subgraph = subgraph_by_parameters(graph, [parameter])

        if nodes_equal(graph.nodes, subgraph.nodes):
            modifiers = modifiers + combined_mod
            name = f"{name}_loop_{parameter}"

        elif len(subgraph.nodes()) == 1:
            node = list(subgraph.nodes)[0]
            # if the looped node is only one node
            # add loop modifier to node attribute
            node_modifiers = subgraph.nodes[node]["modifiers"] + combined_mod
            graph = modify_node(graph, node, modifiers=node_modifiers)

        else:
            submodel_description = (
                f'"{parameter}" looped sub model created by mrfmsim.loop_shortcut'
            )
            # create the model and substitute the subgraph
            looped_node = ModelClass(
                f"{parameter}_looped_sub_model",
                subgraph,
                handler,
                modifiers=combined_mod,
                description=submodel_description,
            )
            # create new graph
            output = ", ".join(model_returns(subgraph))
            output = f"looped_{output}"

            graph = modify_subgraph(
                graph, subgraph, node_name, looped_node, output=output
            )

    looped_model = ModelClass(
        name, graph, handler, modifiers=modifiers, description=description
    )

    return looped_model
