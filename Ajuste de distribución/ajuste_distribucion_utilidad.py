import pandas as pd
import numpy as np
import scipy.stats as st
import warnings
from Funcion_ajuste import best_fit_distribution, plot_distribucion_ajustada, simular_montecarlo

data_utilidad = pd.read_csv('Data/Utilidad mensual.csv')

'''best_distribution_utilidad_am, params_utilidad_am = best_fit_distribution(data_utilidad['Utilidad AM'], 200)
print(f'Mejor distribución para Utilidad AM: {best_distribution_utilidad_am}')
print(f'Parámetros de la mejor distribución para Utilidad AM: {params_utilidad_am}')
plot_distribucion_ajustada(data_utilidad, 'Utilidad AM', best_distribution_utilidad_am, params_utilidad_am, nbins=20, titulo='Ajuste de distribución para Utilidad Operativa AM')
sim_utilidad_am = simular_montecarlo(best_distribution_utilidad_am, params_utilidad_am, utilidad=True)
print(f"Simulación para utilidad operativa AM: {sim_utilidad_am}")'''


best_distribution_utilidad_tr, params_utilidad_tr = best_fit_distribution(data_utilidad['Utilidad TR'], 200)
print(f'Mejor distribución para Utilidad TR: {best_distribution_utilidad_tr}')
print(f'Parámetros de la mejor distribución para Utilidad TR: {params_utilidad_tr}')
plot_distribucion_ajustada(data_utilidad, 'Utilidad TR', best_distribution_utilidad_tr, params_utilidad_tr, nbins=20, titulo='Ajuste de distribución para Utilidad Operativa TR')
sim_utilidad_tr = simular_montecarlo(best_distribution_utilidad_tr, params_utilidad_tr, utilidad=True)
print(f"Simulación para utilidad operativa TR: {sim_utilidad_tr}")