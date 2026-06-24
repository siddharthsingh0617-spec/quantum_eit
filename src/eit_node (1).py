"""
eit_node.py

EITNode: a small class representing one EIT-based quantum memory
node. This completes the EITNode sketch from the original notebook
(it referenced run_storage_retrieval, which is now defined in
dynamics.py).

Usage
-----
    from eit import EITNode

    node = EITNode("node_1", Omega_p=0.05, Omega0=5.0, gamma_12=0.01)
    node.store()
    print(node.memory_state)   # final spin-wave coherence rho12 after storage/retrieval
"""

from .dynamics import run_storage_retrieval


class EITNode:
    """
    A single EIT quantum-memory node.

    Parameters
    ----------
    node_id : str or int
        Identifier for this node.
    Omega_p : float
        Probe Rabi frequency (pulse amplitude).
    Omega0 : float
        Control Rabi frequency.
    gamma_12 : float
        Ground-state coherence dephasing rate (memory decay).
    """

    def __init__(self, node_id, Omega_p=0.05, Omega0=5.0, gamma_12=0.01):
        self.node_id = node_id
        self.Omega_p = Omega_p
        self.Omega0 = Omega0
        self.gamma_12 = gamma_12
        self.memory_state = None   # final rho12 coherence stored in this node
        self.last_result = None    # full simulation output, for inspection/plotting

    def store(self, **kwargs):
        """
        Run a storage & retrieval simulation for this node and save the
        resulting spin-wave coherence (rho12) as the node's memory state.

        Extra keyword args (t_max, n_times, t0, sigma, t_store,
        t_retrieve, tau, Delta) are passed through to
        run_storage_retrieval to override its defaults.
        """
        result = run_storage_retrieval(
            Omega_p=self.Omega_p,
            Omega0=self.Omega0,
            gamma_12=self.gamma_12,
            **kwargs,
        )
        rho12 = result["rho12"]
        self.memory_state = rho12[-1]
        self.last_result = result
        return self.memory_state

    def retrieve(self):
        """Return the currently stored memory state (rho12 coherence)."""
        if self.memory_state is None:
            raise RuntimeError(
                f"Node '{self.node_id}' has no stored memory yet. Call store() first."
            )
        return self.memory_state

    def __repr__(self):
        return (
            f"EITNode(node_id={self.node_id!r}, Omega_p={self.Omega_p}, "
            f"Omega0={self.Omega0}, gamma_12={self.gamma_12}, "
            f"memory_state={self.memory_state})"
        )
