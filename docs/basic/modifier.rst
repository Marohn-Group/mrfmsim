Modifiers and shortcuts
=======================

*mrfmsim* adds additional modifiers and shortcuts specific to the experimental
simulation to the *mmodel* modifiers. See
`modifier and shortcut <https://marohn-group.github.io/mmodel-docs/tutorial_modifier.html>`_
tutorial for details. 
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
   * - print_inputs
     - mmodel.modifier
     - Print the inputs of the function with units.
   * - print_output
     - mmodel.modifier
     - Print the outputs of the function with units.
   * - :mod:`replace_component <mrfmsim.modifier.replace_component>`
     - :mod:`mrfmsim.modifier`
     - Replace the component in the model.
   * - :mod:`numba_jit <mrfmsim.modifier.numba_jit>`
     - :mod:`mrfmsim.modifier`
     - Modify a node using numba jit.
   * - loop_shortcut
     - mmodel.shortcut
     - Loop over a parameter during the experiment execution. 
   * - print_shortcut
     - mmodel.shortcut
     - Apply ``print_inputs`` and ``print_output`` shortcuts to individual nodes
       that print out intermediate variable values during node execution.


:mod:`modifier` module
----------------------

.. automodule:: mrfmsim.modifier
    :members:
    :show-inheritance:
