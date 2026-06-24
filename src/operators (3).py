"""
operators.py

Defines the 3-level lambda-system states, transition/population
operators, and collapse operators. Same definitions as the original
notebook, just gathered in one place.

Levels:
  g1 -> ground state 1
  g2 -> ground state 2
  e  -> excited state
"""

import numpy as np
from qutip import basis

# ---- basis states ----
g1 = basis(3, 0)
g2 = basis(3, 1)
e = basis(3, 2)

# ---- transition operators ----
sigma_13 = g1 * e.dag()  # takes 3 -> 1
sigma_31 = e * g1.dag()  # takes 1 -> 3
sigma_23 = g2 * e.dag()  # takes 3 -> 2
sigma_32 = e * g2.dag()  # takes 2 -> 3
sigma_12 = g1 * g2.dag()
sigma_21 = sigma_12.dag()

# ---- population operators ----
p1 = g1 * g1.dag()
p2 = g2 * g2.dag()
p3 = e * e.dag()


def make_collapse_ops(gamma_31, gamma_32, gamma_12):
    """
    Build the collapse operators for given decay/dephasing rates.

    Returns
    -------
    list of Qobj : [c1, c2, c3]
    """
    c1 = np.sqrt(gamma_31) * g1 * e.dag()
    c2 = np.sqrt(gamma_32) * g2 * e.dag()
    c3 = np.sqrt(gamma_12) * (g1 * g1.dag() - g2 * g2.dag())
    return [c1, c2, c3]
