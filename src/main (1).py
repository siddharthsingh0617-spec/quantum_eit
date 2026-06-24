"""
main.py

Runs the same things the original notebook did, using the modular
eit package:

  1. Steady-state EIT spectrum (absorption vs probe detuning) + plot
  2. Storage & retrieval dynamics (spin-wave, optical coherence,
     excited population) + plot
  3. Builds an EITNode, stores a pulse in it, and prints the resulting
     memory state

Run with:  python main.py
"""

from eit import (
    EITNode,
    compute_spectrum,
    plot_spectrum,
    run_storage_retrieval,
    plot_storage_retrieval,
)


def main():
    # ---- 1. steady-state EIT spectrum ----
    print("Computing steady-state EIT spectrum...")
    spectrum = compute_spectrum()
    plot_spectrum(spectrum, show=False)
    print("First 10 points (delta_p, chi_real, chi_imag, n_real, n_imag, absorption):")
    for i in range(10):
        print(
            spectrum["delta_p"][i],
            spectrum["chi_real"][i],
            spectrum["chi_imag"][i],
            spectrum["n_real"][i],
            spectrum["n_imag"][i],
            spectrum["absorption"][i],
        )

    # ---- 2. storage & retrieval dynamics ----
    print("\nRunning storage & retrieval simulation...")
    sim = run_storage_retrieval(Omega_p=0.02, Omega0=5)
    plot_storage_retrieval(sim, show=False)

    # ---- 3. EITNode usage ----
    print("\nCreating an EITNode and storing a pulse...")
    node = EITNode("node_1", Omega_p=0.05, Omega0=5.0, gamma_12=0.01)
    node.store()
    print(node)


if __name__ == "__main__":
    main()
