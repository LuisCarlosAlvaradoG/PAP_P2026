import numpy as np
import scipy.stats as st

"""
params = (
    np.float64(2.6321632796234953),  
    np.float64(25.392706331696388), 
    np.float64(-1736.749193049455),  
    np.float64(322135.7981926289)    
)

N = 1_000_000

sim_ingresos = st.mielke.rvs(
    params[0], 
    params[1], 
    loc=params[2],
    scale=params[3],
    size=N
)

sim_ingresos = sim_ingresos[sim_ingresos > 0]

print("Esperado:", sim_ingresos.mean())
print("P5:", np.percentile(sim_ingresos, 5))
print("P50:", np.percentile(sim_ingresos, 50))
print("P95:", np.percentile(sim_ingresos, 95))

"""


params = (
    np.float64(5.604727975412163),       
    np.float64(227566.34490851156),    
    np.float64(107012.69421016643)      
)

N = 1_000_000

sim_ingresos = st.gennorm.rvs(
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