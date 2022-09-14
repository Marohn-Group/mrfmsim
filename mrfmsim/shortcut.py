"""Shortcuts"""

from mmodel import loop_modifier, subgraph_by_parameters, modify_subgraph
from networkx.utils import nodes_equal


def loop_shortcut(model, parameter: str):
    """Shortcut to add loop to a subgraph

    :param model: executable model
    :param str parameter: loop parameter
    :return: a new model with looped parameter
    """

    loop_mod = loop_modifier, {"parameter": parameter}
    handler = model._handler
    graph = model._graph
    model_mod_list = model._modifiers
    node_name = f'"{parameter}" loop node'
    description = model.description

    # check if the parameter is in the signature
    if parameter not in model.__signature__.parameters:
        raise Exception(f"'{parameter}' is not a model parameter")

    subgraph = subgraph_by_parameters(graph, [parameter])

    ModelClass = type(model)  # works for both mmodel.Model and mrfmsim.Experiment

    if nodes_equal(graph.nodes, subgraph.nodes):
        model_mod_list = model_mod_list + [loop_mod]
        looped_model = ModelClass(graph, handler, modifiers=model_mod_list)

    else:
        # create the model and substitute the subgraph
        looped_node = ModelClass(subgraph, handler, modifiers=[loop_mod])
        looped_graph = modify_subgraph(graph, subgraph, node_name, looped_node)
        looped_model = ModelClass(looped_graph, handler, description, model_mod_list)

    return looped_model
