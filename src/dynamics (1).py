"""
dynamics.py

Time-domain storage & retrieval simulation: a Gaussian probe pulse
and a control field that switches off (storage) then back on
(retrieval). Same physics as the original notebook's
probe_coeff / control_coeff / mesolve cells, wrapped into a single
reusable function: run_storage_retrieval().
"""

import numpy as np
from qutip import mesolve

from . import parameters as par
from .operators import (
    g1, e, sigma_13, sigma_31, sigma_23, sigma_32,
    sigma_12, make_collapse_ops,
)


def probe_coeff(t, args):
    """Gaussian probe pulse, centered at t0 with width sigma."""
    Omega_p = args["Omega_p"]
    t0 = args.get("t0", 4)
    sigma = args.get("sigma", 2)
    return Omega_p * np.exp(-(t - t0) ** 2 / (2 * sigma ** 2))


def control_coeff(t, args):
    """Control field: on, then off during storage, then back on for retrieval."""
    Omega0 = args["Omega0"]
    t_store = args.get("t_store", 4)
    t_retrieve = args.get("t_retrieve", 10)
    tau = args.get("tau", 0.3)

    off_switch = (1 - np.tanh((t - t_store) / tau)) / 2
    on_switch = (1 + np.tanh((t - t_retrieve) / tau)) / 2
    return Omega0 * (off_switch + on_switch)


def build_hamiltonian(Delta=0.0):
    """Hamiltonian in the rotating frame, with time-dependent probe/control terms."""
    H0 = Delta * (e * e.dag())
    H = [
        H0,
        [-(sigma_13 + sigma_31) / 2, probe_coeff],
        [-(sigma_23 + sigma_32) / 2, control_coeff],
    ]
    return H


def run_storage_retrieval(
    Omega_p=0.02,
    Omega0=5,
    gamma_12=par.gamma_12,
    gamma_31=par.gamma_31,
    gamma_32=par.gamma_32,
    Delta=0.0,
    t_max=20,
    n_times=2000,
    t0=4,
    sigma=2,
    t_store=4,
    t_retrieve=10,
    tau=0.3,
):
    """
    Run the storage & retrieval simulation.

    Same calculation as the original notebook (mesolve with the
    probe/control pulse shapes), bundled into one function so it can
    be reused by EITNode and called with different parameters.

    Returns
    -------
    dict with keys:
        "times", "rho12" (spin-wave coherence), "rho13" (optical
        coherence), "excited" (excited state population), "result"
        (raw qutip Result object)
    """
    c_ops = make_collapse_ops(gamma_31, gamma_32, gamma_12)
    H = build_hamiltonian(Delta=Delta)

    args = {
        "Omega_p": Omega_p,
        "Omega0": Omega0,
        "t0": t0,
        "sigma": sigma,
        "t_store": t_store,
        "t_retrieve": t_retrieve,
        "tau": tau,
    }

    times = np.linspace(0, t_max, n_times)
    rho0 = g1 * g1.dag()

    result = mesolve(
        H,
        rho0,
        times,
        c_ops,
        e_ops=[sigma_12, sigma_13, e * e.dag()],
        args=args,
    )

    rho12 = result.expect[0]
    rho13 = result.expect[1]
    excited = np.real(result.expect[2])

    return {
        "times": times,
        "rho12": rho12,
        "rho13": rho13,
        "excited": excited,
        "result": result,
    }


def plot_storage_retrieval(sim, show=True):
    """Plot spin-wave coherence, optical coherence and excited population."""
    import matplotlib.pyplot as plt

    times = sim["times"]

    plt.figure(figsize=(8, 4))
    plt.plot(times, np.abs(sim["rho12"]), label="rho12")
    plt.xlabel("time")
    plt.ylabel("spin wave")
    plt.legend()
    if show:
        plt.show()

    plt.plot(times, np.abs(sim["rho13"]))
    plt.xlabel("time")
    plt.ylabel("optical coherence |rho13|")
    if show:
        plt.show()

    plt.plot(times, sim["excited"])
    plt.xlabel("time")
    plt.ylabel("excited population")
    if show:
        plt.show()
