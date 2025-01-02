Components
-----------------------------

To create a component ``dataclass``, simply inherit from ``ComponentBase`` 
and define the fields as ``dataclass`` fields. 

For example, to create a cantilever class that stores the cantilever
frequency "f_c" and cantilever spring constant "k_c", we can inherit
the ``ComponentBase`` class and define the attributes as follows:

.. code-block:: python

    from mrfmsim.component import ComponentBase
    from dataclasses import dataclass

    @dataclass
    class Cantilever(ComponentBase):
        f_c: float
        k_c: float


    >>> cantilever = Cantilever(f_c=3000, k_c=1.0)
    >>> cantilever.f_c
    3000
    >>> cantilever.k_c
    1.0

    >>> cantilever # dataclass output
    Cantilever(f_c=3000, k_c=100.0)
    >>> print(cantilever) # formatted output
    Cantilever(f_c=3000
        k_c=100.000)

If we want additional attributes through calculation, instead of defining
``__init__`` method, we can define a ``__post_init__`` method. To specify
that these are not instantiation variables, we specify that they are
``init=False`` in the ``dataclass`` field. See 
`post-init processing 
<https://docs.python.org/3.10/library/dataclasses.html#post-init-processing>`_.

.. code-block:: python

    from dataclasses import field
    import numpy as np

    @dataclass
    class Cantilever(ComponentBase):
        k_c: float
        f_c: float = 5000
        omega: float = field(init=False)

        def __post_init__(self):
            self.omega = 2 * np.pi * self.f_c

    >>> cantilever = Cantilever(k_c=100.0)
    >>> cantilever.omega
    31415.926535897932

    >>> print(cantilever)
    Cantilever(f_c=5000
        k_c=100.000
        omega=31415.927)

In the above code, the cantilever frequency defaults to 5000 Hz.

To add units and formatted string output for the attributes, we can add
"unit" and "format" to the ``dataclass`` field' metadata.

.. code-block:: python

    @dataclass
    class Cantilever(ComponentBase):
        k_c: float = field(metadata={"unit": "aN/nm", "format": ".3e"})
        f_c: float = field(metadata={"unit": "Hz", "format": ".3e"}, default=3000)
        omega: float = field(init=False, metadata={"unit": "rad/s", "format": ".3f"})

        def __post_init__(self):
            self.omega = 2 * np.pi * self.f_c

    >>> cantilever = Cantilever(k_c=100.0)
    >>> print(cantilever)
    Cantilever(k_c=1.000e+02 aN/nm
        f_c=3000 Hz
        omega=18849.556 rad/s)
