Modifiers and shorcuts
======================

*mrfmsim* adds additional modifiers and shortcuts specific to the experimental
simulation to the *mmodel* modifiers. See
`mmodel.modifier <https://marohn-group.github.io/mmodel-docs/ref_modifier.html>`_
for details. 
The shortcuts are used to modify the Experiment/Model object directly, which consists
of applying modifiers to individual nodes or the model/experiment.


List of modifiers and shortcuts for the *mrfmsim* and *mmodel* package.

.. list-table::
   :widths: 10 10 90
   :header-rows: 1

   * - Modifiers/Shorcuts
     - Module
     - Description
   * - loop_input
     - mmodel.modifier
     - Modify function to iterate one given parameter.
   * - zip_loop_inputs
     - mmodel.modifier
     - Modify function to iterate the parameters pairwise.
   * - profile_time
     - mmodel.modifier
     - Profile the execution time of a function.
   * - :mod:`print_inputs <mrfmsim.modifier.print_inputs>`
     - :mod:`mrfmsim.modifier`
     - Print the inputs of the function with units.
   * - :mod:`print_output <mrfmsim.modifier.print_output>`
     - :mod:`mrfmsim.modifier`
     - Print the outputs of the function with units.
   * - :mod:`replace_component <mrfmsim.modifier.replace_component>`
     - :mod:`mrfmsim.modifier`
     - Replace the component in the model.
   * - :mod:`loop_shortcut <mrfmsim.shortcut.loop_shortcut>`
     - :mod:`mrfmsim.shortcut`
     - Loop over a parameter during the experiment execution. 
   * - :mod:`print_shortcut <mrfmsim.shortcut.print_shortcut>`
     - :mod:`mrfmsim.shortcut`
     - Apply ``print_inputs`` and ``print_output`` shortcuts to individual nodes
       that print out intermediate variable values during node execution.


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

The optimal way to loop c and e is to define the loop of parameter e in 
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


Print Shortcut
----------------

The print shortcut aims to print out intermediate values during
node execution to check the execution process. The shortcut is helpful for
slow algorithms and looped models. We also do not want the algorithm to
create unnecessary subgraphs. Therefore, the final design of the shortcut
applies modifiers to individual nodes instead of the entire model. The
design is flexible and works if the underlying graph structure is changed.
The user decides the string format and output style to maintain flexibility.
For the shortcut's unachievable output style, the
users are encouraged to add modifiers to the nodes directly.

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
intermediate value of c and e:

.. code-block:: python

    >>> print_shortcut(M, ['a={a:.2f}', 'c={c:.2f}', 'e={e:.2f}'])
    >>> M(a=1, b=2, d=4, f=10)
    a=1.00
    c=3.00 
    e=7.00

The shortcut works by applying a ``print_inputs`` modifier and 
``print_output`` modifier to node A, and a ``print_output`` modifier to 
node B.

The shortcuts can modify the print keyword arguments. For example, the
print function's default "end" parameter is "\n". To change the
"end" parameter to " | ":

.. code-block:: python

    >>> M = print_shortcut(M, ['a={a:.2f}', 'c={c:.2f}', 'e={e:.2f}'], end=' | ')
    >>> M(a=1, b=2, d=4, f=10)
    a=1.00 | c=3.00 | e=7.00 |

However, in a loop, the output stays in a single line, but we want to create
a linebreak for each loop. The user can apply a modifier that has a unique 
"end" parameter to create the line break or use a second shortcut:

.. code-block:: python

    M = print_shorcut(print_shortcut(M, ['a={a:.2f}', 'c={c:.2f}'], end=' | '), ['e={e:.2f}'])

The output for a looped model:

.. code-block:: python

    >>> M_loop = loop_shortcut(M, 'a')
    >>> M_loop(a_loop=[1, 2], b=2, d=4, f=10)
    a=1.00 | c=3.00 | e=7.00
    a=2.00 | c=4.00 | e=8.00

The decision to have a uniform print parameter argument is to simplify the
user interface and the underlying algorithm. The shortcut is used to apply
the print-related shortcuts quickly. Users are encouraged to create 
additional nodes for monitoring the execution process, which can benefit from 
the ``print_shortcut`` as well.

:mod:`modifier` module
----------------------

.. automodule:: mrfmsim.modifier
    :members:
    :show-inheritance:

:mod:`shortcut` module
----------------------

.. automodule:: mrfmsim.shortcut
    :members:
    :show-inheritance:
