Overview
========

The *mrfmsim* package was originally designed as a simulation package for the 
MRFM experiment. For previous development, please see the archived package 
`mrfmsim_archived <https://github.com/peterhs73/MrfmSim-archived>`__.
The previous versions of MRFM used an object-oriented design, which 
is restrictive to modifications and specific to the Marohn group.
The community's interest in the author's presentation at Nano-MRI: The next
generation prompted the development of a modular and extendable platform to
work with different experiment models, whether from various
prototyping stages or other groups. To achieve the flexibility,
we developed `mmodel <https://github.com/Marohn-Group/mmodel>`__ package as a
backend for *mrfmsim*, allowing us to use directed acyclic 
graphs (DAG) to define experiments. The graph backend allows modular experiment
definition and fast modification to existing models. 
*mrfmsim* extends the *mmodel* framework by adding physical models and calculations
specific to MRFM experiments.

examples
--------

Here, we use a Cornell-style CERMIT ESR experiment as an example
The notebook with all the codes on this page is available at
:download:`mrfmsim_overview </_downloads/mrfmsim_overview.ipynb>`.


We define the necessary inputs for the experiment:

.. code:: python

    from mrfmsim.component import SphereMagnet, Grid, Sample, Cantilever


    sample = Sample(
        spin="e",
        temperature=11.0,
        T1=1.3e-3,
        T2=0.45e-6,
        spin_density=0.5,
    )
    magnet = SphereMagnet(magnet_radius=3300.0, mu0_Ms=440.0, magnet_origin=[0, 0, 3300])
    grid = Grid(grid_shape=[400, 1200, 8], grid_step=[25, 25, 25], grid_origin=[0, 0, -100])
    cantilever = Cantilever(k_c=7.8e5, f_c=4.975e6)

    # define the input parameters
    B1 = 1.3e-3  # transverse magnetic field
    mw_x_0p = 100  # zero to peak amplitude of the cantilever motion [nm]
    B0 = 500  # external field [mT]
    f_rf = 19e9  # microwave frequency [Hz]
    h = [0, 0, 1450]  # tip sample separation [nm]

We can view the summary of the Sample object.

.. code:: python

    >>> print(sample)
    Sample
      spin = 'e'
      T1 = 1.300e-03 s
      T2 = 4.500e-07 s
      temperature = 11.000 K
      spin_density = 0.500 1/nm^3
      Gamma = 1.761e+08 rad/(s.mT)
      J = 0.5
      dB_hom = 0.023 mT
      dB_sat = 0.000 mT


graph representation and metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The graph representation of the experiment allows us to visualize the steps of the 
experiment easily. The metadata shows the experiment's signature, returns, description,
and more. 

To access a standalone experiment model:

.. code:: python

    from mrfmsim.experiment import IBMCyclic
    
    >>> print(IBMCyclic)
    IBMCyclic(B0, df_fm, f_rf, grid, h, magnet, sample)
    returns: (dF2_spin, dF_spin)
    graph: ibm_cyclic_graph
    handler: MemHandler

    Simulate an IBM-style cyclic-inversion magnetic resonance force microscope
    experiment.

To access an experiment model from a experiment group:

.. code:: python

    # print c summary
    print(CermitESRGroup)
    # list experiments
    print(list(CermitESRGroup.experiments.keys()))

    CermitESR = CermitESRGroup['CermitESR']

To printout the metadata of the model:

.. code:: python

    print(CermitESR)

    CermitESR(B0, B1, cantilever, f_rf, grid, h, magnet, mw_x_0p, sample)
    returns: df_spin
    group: CermitESR
    graph: CermitESR_graph
    handler: MemHandler

    CERMIT ESR experiment for a large tip.

To draw the graph of the model:

.. code:: python

    CermitESR.visualize()

.. image:: _static/CermitESR.pdf
    :width: 800px
    :align: center


Model Modification
^^^^^^^^^^^^^^^^^^

A key feature of modular modeling is that it directly allows quick modification
of existing models. The result is a much faster development
cycle for experiment simulation.


Modify nodes - runtime profiling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can easily profile the performance of the target nodes by
applying modifiers to the desired nodes. To edit individual nodes,
use the ``edit_node`` function from the model that returns a new
model.

Using the "CermitESR" experiment model, we can
inspect the run time of "minimum absolute x offset" and
"relative polarization change" performance:

.. code:: python

    from mmodel.modifier import profile_time
    mods = CermitESR.get_node_object("rel_dpol sat").modifiers
    CermitESR_profile = CermitESR.edit_node("rel_dpol sat", modifiers=mods + [profile_time(10)])
    
    >>> signal = CermitESR_profile(B0, B1, cantilever, f_rf, grid, h, magnet, mw_x_0p, sample)
    rel_dpol_sat_steadystate - 10 loops, best of 1: 30.27 ms per loop

Modify returns - output intermediate values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To output intermediate values, we can directly change the returns.

To output the intermediate values of "f_rf" and "dk_spin" and the result
of "df_spin"::

    CermitESR_intermediate = CermitESR.edit(returns=["f_rf", "dk_spin", "df_spin"])

    >>> CermitESR_intermediate(B0, B1, cantilever, f_rf, grid, h, magnet, mw_x_0p, sample)
    (19000000000.0, -0.0024141111050284525, -0.0034656991967769407)

The returned values are in the same order as the returns list.


Modify model - optimal looping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For a complex model, we want to optimize the parameter loop so that
only nodes that are dependent on the target parameter are looped. 
For example, in many MRFM experiments, we need to first calculate the
field and field gradient generated by the tip of the magnet.
The subsequent calculation involves a large three-dimensional matrix
operations. 
Depending on the size of the simulation grid, the matrix operations
can be very computationally intensive.

If we want to simulate the change of the signal over a wide range of 
external field (:math:`B_0`) and microwave frequency 
(:math:`f_\mathrm{rf}``), we would want to avoid repeated
calculations of unnecessary components that are independent of the
two parameters.

The graph-based experiment model can automatically determine the 
optimal loop location and generate a new model with the desired loops.
The looping can be added at the node level using modifiers or
adjusted at the model level using shortcuts.

To loop the "f_rf" parameter (use the cermitesr_stdout model
to print out the intermediate values):

.. code:: python

    from mmodel.shortcut import loop_shortcut
    CermitESR_frf_loop = loop_shortcut(CermitESR, "f_rf", name="CermitESR_frf_Loop")
    CermitESR_frf_loop.visualize()

.. image:: _static/CermitESR_frf_loop.pdf
    :width: 800px
    :align: center

|br|
To loop the "B0" parameter on top of "f_rf"::

    CermitESR_B0_frf_loop = loop_shortcut(
        CermitESR_frf_loop, "B0", name="CermitESR_B0frf_Loop"
    )
    CermitESR_B0_frf_loop.visualize()

.. image:: _static/CermitESR_b0_frf_loop.pdf
    :width: 800px
    :align: center

|br|
The model can be executed by supplying lists for "B0" and "f_rf":

.. code:: python

    import numpy as np
    B0_list = np.arange(500, 900, 200)  # external field [mT]
    f_rf_list = np.arange(18.5e9, 19.5e9, 0.5e9)  # microwave frequency [Hz]

    >>> CermitESR_B0_frf_loop(
            B0_loop=B0_list,
            B1=B1,
            cantilever=cantilever,
            f_rf_loop=f_rf_list,
            grid=grid,
            h=h,
            magnet=magnet,
            mw_x_0p=mw_x_0p,
            sample=sample,
        )
    [[-0.005362279436110155, -0.003465699196776941],
     [0.0071300149234139135, 0.02300114588870745]]


The ``loop_shortcut`` changes the parameter name to ``{parameter}_loop``
to distinguish the iterable input from the original input type.
For the 2 by 2 loop, the output is::

    [[func(B0[0], f_rf[0]), func(B0[0], f_rf[1])],
     [func(B0[1], f_rf[0]), func(B0[1], f_rf[1])]]

This is equivalent to the result from the following loops:

.. code:: python

    for B0 in B0_list:
        ...

        for f_rf in f_rf_list:
            ...

.. note::

    Note that for individual parameters, the loop shortcut can achieve
    optimal looping. However, for multiple parameters, users must decide
    which parameter to loop first. Since all nodes that are
    dependent on "f_rf" also depend on "B_0", we loop "f_rf" first. 

Modify nodes - print out node input and output values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes, we only want to inspect the intermediate value instead of adding
them to returns. To achieve this, we can add print-related modifiers
``modifier.print_inputs`` and ``modifier.print_ouput`` to individual nodes.
To simplify the process, the shortcut ``shortcut.print_shortcut`` can automatically
apply print statements to the nodes. The print format
uses the keyword python format string. Additional keyword arguments for the print
function, such as ``end``, ``flush``, and ``file`` can be
added directly to the shortcut function. 

Here we show how to output the input "B0", "f_rf" and "df_spin" during
the execution:

.. code:: python

    from mmodel.shortcut import print_shortcut
    print_model = print_shortcut(
        CermitESR, ["B0 = {B0:.2f} mT", "f_rf = {f_rf:.2f} Hz", "df_spin = {df_spin:.2e} Hz"]
    )

    >>> signal = print_model(B0, B1, cantilever, f_rf, grid, h, magnet, mw_x_0p, sample)
    B0 = 500.00 mT
    f_rf = 1.90e+10 Hz
    df_spin = -3.47e-03 Hz

.. Note::

    The print shortcut only adds modifiers to individual nodes. They do not interfere with
    the looping modification.


.. |br| raw:: html
    
    <br/>
