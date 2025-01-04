from mrfmsim import formula
from mrfmsim import Node, ExperimentGroup
from .stdelements import STANDARD_NODES

node_objects = [
    Node("rel_dpol td_sat", formula.rel_dpol_sat_td, output="rel_dpol"),
    Node("rel_dpol small_steps", formula.rel_dpol_sat_td_smallsteps, output="rel_dpol"),
    Node("rel_dpol averaged", formula.rel_dpol_multipulse, output="rel_dpol"),
]

CermitTD_edges = [
    ["grid extended", "Bz extended"],
    ["Bz extended", "B_tot extended"],
    ["B_tot extended", ["B_tot sliced", "B_offset extended"]],
    ["B_tot sliced", "mz_eq"],
    [["B_offset extended", "Bzx", "x_0p window pts"], "rel_dpol td_sat"],
    ["rel_dpol td_sat", "rel_dpol averaged"],
    [["mz_eq", "Bzxx", "rel_dpol averaged"], "spring constant shift"],
    ["spring constant shift", "frequency shift"],
]

CermitTDSmallTip_edges = [
    ["grid extended", ["Bz extended", "Bzx extended"]],
    ["Bz extended", "B_tot extended"],
    ["B_tot extended", ["B_tot sliced", "B_offset extended"]],
    ["B_tot sliced", "mz_eq"],
    [["B_offset extended", "Bzx extended", "x_0p window pts"], "rel_dpol small_steps"],
    ["rel_dpol small_steps", "rel_dpol averaged"],
    [["mz_eq", "Bzxx trapz", "rel_dpol averaged"], "spring constant shift trapz"],
    ["spring constant shift trapz", "frequency shift"],
]

experiment_recipes = {
    "CermitTD": {
        "grouped_edges": CermitTD_edges,
        "doc": "Time-dependent CERMIT experiment for a large tip.",
    },
    "CermitTDSmallTip": {
        "grouped_edges": CermitTDSmallTip_edges,
        "doc": "Time-dependent CERMIT experiment for a small tip.",
    },
}

components = {
    "magnet": ["Bz_method", "Bzx_method", "Bzxx_method"],
    "sample": ["J", "Gamma", "spin_density", "temperature", "T1", "T2"],
    "grid": [
        "grid_array",
        "grid_step",
        "grid_shape",
        "grid_voxel",
        "extend_grid_by_length",
    ],
    "cantilever": ["k2f_modulated"],
}

docstring = """\
Simulates a Cornell-style frequency shift magnetic
resonance force microscope experiment considering the time-dependent
nature of the saturation, averaged over multiple pulses and with
small-step approximation.
"""

CermitTDGroup = ExperimentGroup(
    name="CermitTDGroup",
    node_objects=list(STANDARD_NODES) + node_objects,
    experiment_recipes=experiment_recipes,
    experiment_defaults={"components": components},
    doc=docstring,
)
