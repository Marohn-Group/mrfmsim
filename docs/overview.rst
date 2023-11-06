Overview
========

``mrfmsim`` package was originally designed as a simulation package
for the MRFM experiment. For previous development, please see the
archived package 
`mrfmsim_archived <https://github.com/peterhs73/MrfmSim-archived>`__. 
The community's interest in the author's presentation at Nano-MRI:
at Nano-MRI: The next generation prompted the development of a
the package that includes more experiments from the MRFM community. 
The previous versions of MRFM uses an object-oriented design, which 
is restrictive and specific to the Marohn group. Since we developed
`mmodel <https://github.com/Marohn-Group/mmodel>`__ package as a
backend for ``mrfmsim``, allowing us to use directed acyclic 
graphs (DAG) to define experiments. Here we highlight the benefits
of using ``mmdoel`` as the backend. For a detailed explanation of 
the "graph", "model", "modifier", and "shortcut" functionalities,
see `mmodel documentation <https://github.com/Marohn-Group/mmodel-docs>`__. 

Here we use a Cornell-style CERMIT-ESR experiment as an example
(see `MrfmSim-Marohn documentation <https://github.com/Marohn-Group/mrfmsim-marohn-docs>`__ 
for the explanation of the experiment). The
notebook with all the codes of this page is available at
:download:`mrfmsim_overview </_downloads/mrfmsim_overview.ipynb>`.

The following code assumes the ``mrfmsim_marohn`` package is loaded::

    import mrfmsim
    mrfmsim.load_plugins()

We define the necessary inputs for the experiment::

    from mrfmsim.component import SphereMagnet, Grid, Sample, Cantilever

    sample = Sample(
        spin_type="electron",
        temperature=11.0,
        T1=1.3e-3,
        T2=0.45e-6,
        spin_density=0.5,
    )
    magnet = SphereMagnet(radius=3300.0, mu0_Ms=440.0, origin=[0, 0, 3300])
    grid = Grid(shape=[400, 1200, 8], step=[25, 25, 25], origin=[0, 0, -100])
    cantilever = Cantilever(k_c=7.8e5, f_c=4.975e6)

    B1 = 1.3e-3  # transverse magnetic field
    mw_x_0p = 100  # zero to peak amplitude of the cantilever motion [nm]
    B0 = 500  # external field [mT]
    f_rf = 19e9  # microwave frequency [Hz]
    h = [0, 0, 1450]  # tip sample separation [nm]

Graph representation and metadata
---------------------------------

The graph representation of the experiment allows us to easily visualize the steps of the experiment. The metadata shows the signature, returns, description and more of the experiment.

To printout the metadata of the model::

    from mrfmsim.experiment import cermitesr
    
    >>> print(cermitesr)
    >>> CermitESR(B0, B1, cantilever, f_rf, grid, h, magnet, mw_x_0p, sample)
        returns: df_spin
        graph: cornell_esr_graph
        handler: MemHandler
        modifiers:
          - replace_component({'magnet': ['Bz_method', 'Bzxx_method'], 'sample': ['J',
          'Gamma', 'spin_density', 'temperature', 'dB_sat', 'dB_hom'], 'grid':
          ['grid_array', 'shape', 'step', 'voxel', 'extend_grid_method'],
          'cantilever': ['dk_to_df_ac_cermit']})

        Simulates a Cornell-style frequency shift magnetic resonance force microscope
          experiment in which microwaves are applied for half a cantilever cyclic to
          saturate electron spin resonance in a bowl-shaped region swept out by the
          cantilever motion.

To draw the graph of the model::

    from mrfmsim.experiment import cermitesr
    cermitesr.draw()

.. image:: _static/cermitesr.pdf
    :width: 800px
    :align: center


Model Modification Post Definition
----------------------------------

A key feature of mmodel is to allow quick modification to existing
models directly. The result is a must faster development cycle for
experiment simulation.


Runtime profiling
~~~~~~~~~~~~~~~~~~

We can easily profile the performance of the target nodes using by
applying modifiers to the desired nodes. We can modify individual
graph nodes or we can use ``modifier_shortcut`` and the modifier 
``profile_time`` to modify the experiment model directly.

Using the ``cermitesr`` experiment model we can
inspect the run time of "minimum absolute x offset" and
"relative polarization change" performance::

    from mrfmsim.shortcut import modifier_shortcut
    from mrfmsim.modifier import profile_time

    mod_dict = {
        "minimum absolute x offset": [profile_time()],
        "relative polarization change": [profile_time()],
    }

    cermitesr_profile = modifier_shortcut(cermitesr, mod_dict, name="CermitESR_Profile")

    >>> cermitesr_profile(B0, B1, cantilever, f_rf, grid, h, magnet, mw_x_0p, sample)
    >>> min_abs_offset - 1 loop, best of 1: 72.01 ms per loop
        rel_dpol_sat_steadystate - 10 loops, best of 1: 2.05 ms per loop

        -0.003465699196776941

Output values during execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can return intermediate values by modifying the experiment
returns, but sometimes we only want to inspect the value. We can
quickly add parameter printing to the model with units. The feature
is especially useful when we loop the experiment in the next
section.
For example, we want to show the value of "f_rf" (input), "dk_spin" 
(Intermediate) and "df_spin" (output). We use the ``UNITS``
dictionary in ``mrfmsim_marohn`` package::

    from mrfmsim.shortcut import print_shortcut
    from mrfmsim_marohn import UNITS

    cermitesr_stdout = print_shortcut(cermitesr, ["f_rf", "dk_spin", "df_spin"], units=UNITS, name="CermitESR_Stdout")

    >>> cermitesr_stdout(B0, B1, cantilever, f_rf, grid, h, magnet, mw_x_0p, sample)
    >>> f_rf 1.900e+10 [Hz] | dk_spin -0.002 [aN/nm] | df_spin -0.003 [mHz]
        
        -0.003465699196776941

.. Note::

    Currently, an output parameter should always be added to the
    ``print_shortcut`` to ensure the linebreak. The behavior will
    be corrected in the future.

Optimal looping
~~~~~~~~~~~~~~~~

In a lot of the MRFM experiments, we need to first calculate the
field and field gradient generated by the tip of the magnet.
The subsequent calculation involves a large three-dimensional matrix
operations. 
Depending on the size of the simulation grid, the matrix operations
can be very computationally intensive.

If we want to simulate the change of the signal over a wide range of 
external field (:math:`B_0`) and microwave frequency 
(:math:`f_\mathrm{rf}``), we would want to avoid repeat
calculations of unnecessary components that are independent of the
two parameters.

The graph-based experiment model can automatically determine the 
optimal loop location and generate a new model with desired loops.

To loop the "f_rf" parameter (use the cermitesr_stdout model
to print out the intermediate values)::

    from mrfmsim.shortcut import loop_shortcut

    cermitesr_frf_loop = loop_shortcut(cermitesr_stdout, "f_rf", name="CermitESR_frfLoop")

    cermitesr_frf_loop.draw(export="cermitesr_frf_loop.pdf")

.. image:: _static/cermitesr_frf_loop.pdf
    :width: 800px
    :align: center

To loop the "B0" parameter on top of "f_rf"::

    cermitesr_b0_frf_loop = loop_shortcut(
        cermitesr_frf_loop, "B0", name="CermitESR_b0frfLoop"
    )

    cermitesr_b0_frf_loop.draw(export="cermitesr_b0_frf_loop.pdf")


.. image:: _static/cermitesr_b0_frf_loop.pdf
    :width: 800px
    :align: center

The model can be executed by supplying lists for "B0" and "f_rf"::

    import numpy as np

    B0_list = np.arange(500, 900, 200)  # external field [mT]
    f_rf_list = np.arange(18.5e9, 19.5e9, 0.5e9)  # microwave frequency [Hz]

    >>> cermitesr_b0_frf_loop(
            B0=B0_list,
            B1=B1,
            cantilever=cantilever,
            f_rf=f_rf_list,
            grid=grid,
            h=h,
            magnet=magnet,
            mw_x_0p=mw_x_0p,
            sample=sample,
        )
    >>> f_rf 1.850e+10 [Hz] | dk_spin -0.004 [aN/nm] | df_spin -0.005 [mHz]
        f_rf 1.900e+10 [Hz] | dk_spin -0.002 [aN/nm] | df_spin -0.003 [mHz]
        f_rf 1.850e+10 [Hz] | dk_spin 0.005 [aN/nm] | df_spin 0.007 [mHz]
        f_rf 1.900e+10 [Hz] | dk_spin 0.016 [aN/nm] | df_spin 0.023 [mHz]

        [[-0.005362279436110155, -0.003465699196776941],
         [0.0071300149234139135, 0.02300114588870745]]

The result is a 2x2 matrix equivalent to the result from the
following loops::

    for B0 in B0_list:
        ...

        for f_rf in f_rf_list:
            ...

