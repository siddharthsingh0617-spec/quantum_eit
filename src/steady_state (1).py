"""
steady_state.py

Computes the steady-state EIT spectrum: absorption, susceptibility
and refractive index as a function of probe detuning. This is the
same calculation as in the original notebook's "time_evolution" cell
(it loops over delta_p and solves for the steady state at each point).
"""

import numpy as np
from qutip import steadystate

from . import parameters as par
from .operators import sigma_13, sigma_31, sigma_23, sigma_32, p2, p3, make_collapse_ops


def compute_spectrum(
    delta_p=par.delta_p,
    delta_c=par.delta_c,
    omega_p=par.omega_p,
    omega_c=par.omega_c,
    gamma_31=par.gamma_31,
    gamma_32=par.gamma_32,
    gamma_12=par.gamma_12,
):
    """
    Sweep probe detuning and compute the steady-state EIT spectrum.

    Parameters
    ----------
    delta_p : array_like
        Probe detuning values to sweep over.
    delta_c, omega_p, omega_c, gamma_31, gamma_32, gamma_12 : float
        Physical parameters (defaults taken from parameters.py).

    Returns
    -------
    dict with keys:
        "delta_p", "absorption", "chi_real", "chi_imag",
        "n_real", "n_imag"
    """
    c_ops = make_collapse_ops(gamma_31, gamma_32, gamma_12)

    absorption = []
    chi_real = []
    chi_imag = []
    n_real = []
    n_imag = []

    for del_p in delta_p:
        H = (
            -del_p * p3 - (del_p - delta_c) * p2  # hamiltonian
            + (omega_p / 2) * (sigma_31 + sigma_13)
            + (omega_c / 2) * (sigma_32 + sigma_23)
        )

        rho_ss = steadystate(H, c_ops)
        absorption.append(-np.imag(rho_ss[2, 0]))

        # susceptibility
        rho31 = rho_ss[2, 0]
        chi = rho31 / omega_p
        chi_real.append(np.real(chi))
        chi_imag.append(np.imag(chi))

        # refractive index
        n = np.sqrt(1 + chi)
        n_real.append(np.real(n))
        n_imag.append(np.imag(n))

    return {
        "delta_p": delta_p,
        "absorption": absorption,
        "chi_real": chi_real,
        "chi_imag": chi_imag,
        "n_real": n_real,
        "n_imag": n_imag,
    }


def plot_spectrum(spectrum, show=True):
    """Plot absorption vs probe detuning (same plot as the original notebook)."""
    import matplotlib.pyplot as plt

    plt.plot(spectrum["delta_p"], spectrum["absorption"])
    plt.xlabel("probe detuning")
    plt.ylabel("im(rho31)")
    plt.title("eit_spectrum")
    if show:
        plt.show()
