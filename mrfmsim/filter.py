from mmodel import loop_modifier, Model


def node_by_loop_modifier(model):
    """Find the base nodes that contain the loop modifier

    If the node is a Model/Experiment instance, the graph
    of the instance is searched again. (DFS)
    The filter function returns the base model that uses
    the loop modifier, and all loop parameters.
    """

    model_stack = [model]
    loop_parameters = []
    loop_nodes = {}

    while model_stack:
        model = model_stack.pop()
        graph = model.graph
        model_loop_nodes = []
        for node in graph.nodes():
            node_dict = graph.nodes[node]
            print(node_dict)
            for mod in node_dict["modifiers"]:
                if mod[0] == loop_modifier:
                    loop_parameters.append(mod[1]["parameter"])
                    model_loop_nodes.append(node_dict)

            if issubclass(type(node_dict["base_obj"]), Model):
                model_stack.append(node_dict["base_obj"])
                model_loop_nodes.append(node_dict)
        loop_nodes[model.__name__] = model_loop_nodes
    
    return loop_parameters, loop_nodes
