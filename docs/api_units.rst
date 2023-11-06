Units
======

Currently, the units are not attached to the values in
the calculation result. They are defined separately for reference
purposes only. (However, this might change in the future.)

The units should be defined as a dictionary, with the key as the
parameter name, and the value as a dictionary with the following
(use the "radius" unit as an example):

- ``unit``: the string display of the unit, e.g. ``[nm]``.
- ``latex_label``: the LaTeX display of the unit, e.g. ``[\mathrm{nm}]``.
- ``description``: a description of the unit, e.g. ``magnet radius``.
- ``format``: format of the value when displayed, e.g. ".1f".

To simply the definition process, a YAML units file can be used, see the
``units.yaml`` file used in ``mrfmsim-marohn`` for an example.
