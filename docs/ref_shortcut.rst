Shortcut
======================

The shortcuts are used to directly modify the Experiment/Model. The 
*mrfmsim* package adds additional shortcuts:

- ``print_shortcut``: automatically apply ``print_inputs`` and 
  ``print_output`` shortcuts to individual nodes that print out intermediate
  variable values during node execution.

- ``loop_shortcut``: loop over a parameter during the experiment execution. 
  The shortcut finds the optimal location in the graph to create the 
  subgraph and create the loop.

Print Shortcut
----------------

The goal of the print shortcut is to print out intermediate values during
node execution to check the execution process. The shortcut is helpful for
slow algorithms and looped models. We also do not want the algorithm to
create unnecessary subgraphs. Therefore the final design of the shortcut
applies modifiers to individual nodes instead of the entire model. The
design is flexible and works if the underlying graph structure is changed.
To maintain flexibility, the user decides the string format and the
output style. For output style that is unachievable by the shortcut, the
users are encouraged to directly add modifiers to the nodes.

For example a graph of :math:`G=\{V=\{A, B, C\}, E=\{(A, B), (B, C)\}\}`::

    A -> B -> C

    def A(a, b):
        c = a + b
        return c

    def B(c, d):
        e = c + d
        return e

    def C(e, f):
        g = e + f
        return g

And the model is ``M = Model(graph=G, ...)``. To output the input value a, 
intermediate value of c and e::

    print_shortcut(M, ['a={a:.2f}', 'c={c:.2f}', 'e={e:.2f}'])
  
The output for ``M(a=1, b=2, d=4, f=10)`` is::
  
    a=1.00
    c=3.00 
    e=7.00

The shortcut works by applying a ``print_inputs`` modifier and 
``print_output`` modifier to node A, and a ``print_output`` modifier to 
node B.

The shortcuts can modify the print keyword arguments. For example, the
default ``end`` parameter for the print function is "\n". To change the
``end`` parameter to "" | ", the user can do::

    M = print_shortcut(M, ['a={a:.2f}', 'c={c:.2f}', 'e={e:.2f}'], end=' | ')

The output for ``M(a=1, b=2, d=4, f=10)`` is::
  
    a=1.00 | c=3.00 | e=7.00 |

However, in a loop, the output stays in a single line but we want to create
a linebreak for each loop. The user can apply a modifier that has a unique 
``end`` parameter to create the linebreak, or use a second shortcut:: 

    M = print_shorcut(print_shortcut(M, ['a={a:.2f}', 'c={c:.2f}'], end=' | '), ['e={e:.2f}'])

The output for a looped ``M_loop(a=[1, 2], b=2, d=4, f=10)`` is::
  
    a=1.00 | c=3.00 | e=7.00
    a=2.00 | c=4.00 | e=8.00

with a linebreak at the end.

The decision to have a uniform print parameter argument is to simplify the
user interface and the underlying algorithm. The shortcut is used to apply
the print-related shortcuts quickly. Users are encouraged to create 
additional nodes for monitoring execution process, which can benefit from 
the ``print_shortcut`` as well.

Loop Shortcut
----------------

The loop shortcut works by locating the first dependency of the parameter 
in the graph. It then creates a subgraph that contains all the nodes that
depend on the parameter. A new experiment is created with the subgraph as a 
single node, and the node function is an experiment model. When multiple 
parameters need to be looped, the user needs to inspect the order of the 
parameter appearance in the graph to achieve an optimal result.

For example, a graph of :math:`G=\{V=\{A, B, C\}, E=\{(A, B), (B, C)\}\}`::

    A -> B -> C

    A(a, b)
    B(c, d)
    C(e, f)

The optimal way to loop c and e, is to define the loop of parameter e in 
node C first and then define the loop of parameter c in node B second. If 
the order given is reversed, both parameters c and e are looped at node B 
level. The reason for the behavior is that when loop c is created, the 
graph::

    A -> BC

    A(a, b)
    BC(c, d, e, f)

As a result, the subsequent loop definition only recognizes the subgraph 
node BC and loop the node instead.

.. note::

    For a two-loop system, the optimal order can always be resolved. 
    However, looping more than three parameters, the optimal order may not 
    be resolved. Therefore, the design decision is made for the user to 
    define the loop order.


:mod:`shortcut` module
----------------------

.. automodule:: mrfmsim.shortcut
    :members:
    :show-inheritance:
