"""
parameters.py

Default physical parameters for the 3-level lambda EIT system.
Kept identical to the values used in the original notebook so results
match exactly. Edit these defaults, or pass overrides into the
functions in steady_state.py / dynamics.py.
"""

import numpy as np

# Rabi frequencies
omega_p = 0.5      # probe Rabi frequency
omega_c = 5         # control Rabi frequency

# Decay / dephasing rates
gamma_12 = 0.001    # ground-state coherence dephasing
gamma_31 = 0.5       # |3> -> |1> spontaneous decay
gamma_32 = 0.5       # |3> -> |2> spontaneous decay

# Detunings
delta_c = 0                          # control detuning
delta_p = np.linspace(-10, 10, 400)  # probe detuning sweep
