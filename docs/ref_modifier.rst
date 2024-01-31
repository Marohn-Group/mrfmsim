Modifier
======================

*mrfmsim* adds additional modifiers specific to the experimental
simulation to the *mmodel* modifiers. See
`mmodel.modifier <https://marohn-group.github.io/mmodel-docs/ref_modifier.html>`_
for details.

- ``print_inputs``: print the inputs of the function with units.
- ``print_outputs``: print the outputs of the function with units.
- ``replace_component``: used in the Experiment class definition.
  The "replace_inputs" adds a modifier to the model.

.. note::

    All the *mmodel* modifiers are loaded under the *mrfmsim* namespace.
    They can be accessed by ``mrfmsim.modifier.<modifier_name>``.

:mod:`modifier` module
----------------------

.. automodule:: mrfmsim.modifier
    :members:
    :show-inheritance:
