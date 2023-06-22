Shortcut
======================

The shortcuts are used to directly modify the Experiment. `mrfmsim` adds additional
shortcuts:

- ``print_shortcut``: printout desired parameters with units during the experiment
  execution. The shortcut automatically determines whether the parameter is an
  input or output

- ``loop_shortcut``: loop over a parameter during the experiment execution. The
  shortcut finds the optimal location in the graph to create the subgraph and
  create the loop.


Loop Shortcut
----------------------

The loop shortcut works by locating the first dependency of the parameter in the 
graph. It then creates a subgraph that contains all the nodes that
depend on the parameter. A new experiment is created with the subgraph as a single
node, and the node function is an experiment model. When multiple parameters need
to be looped, the user needs to inspect the order of the parameter appearance in
the graph to achieve an optimal result.

For example, a graph of :math:`G=\{V=\{A, B, C\}, E=\{(A, B), (B, C)\}\}`::

    A -> B -> C

    A(a, b)
    B(c, d)
    C(e, f)

The optimal way to loop c and e, is to define the loop of parameter e in node C first
and then define the loop of parameter c in node B second. If the order given is reversed,
both parameters c and e are looped at node B level. The reason for the behavior is that
when loop c is created, the graph::

    A -> BC

    A(a, b)
    BC(c, d, e, f)

As a result, the subsequent loop definition only recognizes the subgraph node BC and
loop the node instead.

.. note::

    For a two-loop system, the optimal order can always be resolved. However, looping
    more than three parameters, the optimal order may not be resolved. Therefore, the
    design decision is made for the user to define the loop order.


:mod:`shortcut` module
----------------------

.. automodule:: mrfmsim.shortcut
    :members:
    :show-inheritance:
