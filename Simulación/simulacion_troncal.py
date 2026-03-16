import scipy.stats as st
import numpy as np


mu = 1428590.098622531       
sigma = 364674.8926162206 

N = 1_000_000

sim_ingresos = st.norm.rvs(
    loc=mu,
    scale=sigma,
    size=N
)

sim_ingresos = sim_ingresos[sim_ingresos > 0]

print("Esperado:", sim_ingresos.mean())
print("P5:", np.percentile(sim_ingresos, 5))
print("P50:", np.percentile(sim_ingresos, 50))
print("P95:", np.percentile(sim_ingresos, 95))


"""
params = (
    np.float64(28632.824931487827),       
    np.float64(-113839859.0105288),       
    np.float64(115296111.91153952)  
)

N = 1_000_000

sim_ingresos = st.nakagami.rvs(
    params[0],             
    loc=params[1],
    scale=params[2],
    size=N
)

sim_ingresos = sim_ingresos[sim_ingresos > 0]

print("Esperado:", sim_ingresos.mean())
print("P5:", np.percentile(sim_ingresos, 5))
print("P50:", np.percentile(sim_ingresos, 50))
print("P95:", np.percentile(sim_ingresos, 95))
"""