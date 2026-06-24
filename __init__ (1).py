"""
eit package

A small modular EIT (Electromagnetically Induced Transparency)
simulation package, split out of the original notebook:

    parameters.py   - default physical constants
    operators.py    - states, transition/population/collapse operators
    steady_state.py - probe-detuning sweep -> absorption/chi/n spectrum
    dynamics.py     - probe/control pulse shapes + storage & retrieval
    eit_node.py     - EITNode class (quantum memory node)
"""

from .eit_node import EITNode
from .steady_state import compute_spectrum, plot_spectrum
from .dynamics import run_storage_retrieval, plot_storage_retrieval

__all__ = [
    "EITNode",
    "compute_spectrum",
    "plot_spectrum",
    "run_storage_retrieval",
    "plot_storage_retrieval",
]
