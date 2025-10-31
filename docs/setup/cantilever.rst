Cantilever
==========

An ``Cantilever`` object is used to store cantilever parameters and calculate
coefficients needed to convert a spring constant shift to a resonance-frequency
shift, based on the experiment. The available coefficients are for the DC signal and modulated signal. 

Example Usage
^^^^^^^^^^^^^

Create a cantilever object with a spring constant of 780 aN/nm and
frequency of 4975 Hz:

.. code-block:: python

    cantilever = Cantilever(k_c=780, f_c=4975)

To print out the cantilever summary:

.. code-block:: python

    >>> print(cantilever)
    Cantilever
      k_c = 780 aN/nm
      f_c = 4975 Hz
      k2f_modulated = 1.436e+00 Hz.nm/aN
      k2f = 3.189e+00 Hz.nm/aN

:mod:`cantilever` module
------------------------

.. automodule:: mrfmsim.component.cantilever
    :members:
    :show-inheritance:
