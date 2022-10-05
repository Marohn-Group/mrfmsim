"""Shortcuts

The shortcut should work for both Model and Experiment
"""

from mmodel import loop_modifier, subgraph_by_parameters, modify_subgraph, model_signature
from networkx.utils import nodes_equal


def loop_shortcut(model, parameter: str):
    """Shortcut to add loop to a subgraph

    :param model: executable model
    :param str parameter: loop parameter
    :return: a new model with looped parameter
    """

    loop_mod = loop_modifier, {"parameter": parameter}
    name = model.__name__
    handler = model.handler
    graph = model.graph
    modifiers = model.modifiers
    node_name = f'"{parameter}" loop node'
    description = model.description

    ModelClass = type(model)  # works for both mmodel.Model and mrfmsim.Experiment

    # check if the parameter is in the signature
    if parameter not in model.__signature__.parameters:
        raise Exception(f"'{parameter}' is not a model parameter")

    # this is case when the parameter is in signature but not in graph
    # this is due to signature modifier on the model level
    # therefore the whole model is looped.
    
    elif parameter not in model_signature(graph).parameters:
        modifiers = modifiers + [loop_mod]

    else:  # the parameter is within the graph

        subgraph = subgraph_by_parameters(graph, [parameter])

        if nodes_equal(graph.nodes, subgraph.nodes):
            modifiers = modifiers + [loop_mod]

        else:
            sub_model_name = f'"{parameter}" looped sub model'
            # create the model and substitute the subgraph
            looped_node = ModelClass(
                sub_model_name, subgraph, handler, modifiers=[loop_mod]
            )
            # create new graph
            graph = modify_subgraph(graph, subgraph, node_name, looped_node)

    looped_model = ModelClass(
        name, graph, handler, modifiers=modifiers, description=description
    )

    return looped_model
