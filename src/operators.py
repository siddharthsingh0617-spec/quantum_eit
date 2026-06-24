

import numpy as np
from qutip import basis


g1 = basis(3, 0)
g2 = basis(3, 1)
e = basis(3, 2)


sigma_13 = g1 * e.dag()  
sigma_31 = e * g1.dag()  
sigma_23 = g2 * e.dag()  
sigma_32 = e * g2.dag()  
sigma_12 = g1 * g2.dag()
sigma_21 = sigma_12.dag()


p1 = g1 * g1.dag()
p2 = g2 * g2.dag()
p3 = e * e.dag()


def make_collapse_ops(gamma_31, gamma_32, gamma_12):
    
    c1 = np.sqrt(gamma_31) * g1 * e.dag()
    c2 = np.sqrt(gamma_32) * g2 * e.dag()
    c3 = np.sqrt(gamma_12) * (g1 * g1.dag() - g2 * g2.dag())
    return [c1, c2, c3]
