import numpy as np
import scipy.stats as st
import warnings
import pandas as pd
from Funcion_ajuste import best_fit_distribution, plot_distribucion_ajustada, simular_montecarlo


data = pd.read_csv('Data/Kilometros.csv')
data['Unidad'] = data['Unidad'].replace(r'^\s*$', np.nan, regex=True)
data = data.dropna(subset=['Unidad'])
data['Fecha'] = pd.to_datetime(data['Fecha'], format='%d/%m/%Y')

data_km_am = data[data['Unidad'].str.startswith('AM')]
data_km_tr = data[data['Unidad'].str.startswith('TM')]

data_km_am = data_km_am.groupby('Fecha')['Km Programados'].sum().reset_index().iloc[:-1]
data_km_tr = data_km_tr.groupby('Fecha')['Km Programados'].sum().reset_index().iloc[:-1]

'''best_distribution_km_am, best_params_km_am = best_fit_distribution(data_km_am['Km Programados'], bins=200, ax=None)
print(f"Mejor distribución para Kilómetros Programados AM: {best_distribution_km_am}")
print(f"Parámetros de la mejor distribución para Kilómetros Programados AM: {best_params_km_am}")
plot_distribucion_ajustada(data_km_am, 'Km Programados', best_distribution_km_am, best_params_km_am, nbins=30, titulo='Ajuste de distribución para Kilómetros Programados AM')
sim_kmp_am = simular_montecarlo(best_distribution_km_am, best_params_km_am)
print(f"Simulación para Kilómetros Programados AM: {sim_kmp_am}")'''

'''best_distribution_km_tr, best_params_km_tr = best_fit_distribution(data_km_tr['Km Programados'], bins=200, ax=None)
print(f"Mejor distribución para Kilómetros Programados TM: {best_distribution_km_tr}")
print(f"Parámetros de la mejor distribución para Kilómetros Programados TM: {best_params_km_tr}")
plot_distribucion_ajustada(data_km_tr, 'Km Programados', best_distribution_km_tr, best_params_km_tr, nbins=30, titulo='Ajuste de distribución para Kilómetros Programados TM')
sim_kmp_tr = simular_montecarlo(best_distribution_km_tr, best_params_km_tr)
print(f"Simulación para Kilómetros Programados TM: {sim_kmp_tr}")'''