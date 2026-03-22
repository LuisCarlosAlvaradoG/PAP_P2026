import pandas as pd
import numpy as np
import scipy.stats as st
import warnings
from Funcion_ajuste import best_fit_distribution, plot_distribucion_ajustada, simular_montecarlo

data_costos = pd.read_csv('Data/Gastos.csv')

data_costos['Fecha'] = pd.to_datetime(data_costos['Fecha'], format='mixed', dayfirst=True)
data_costos['Costos Operativos'] = data_costos[['Costo de Venta (Refacciones)', 'Gastos de Operación', 'Gastos de Mantenimiento']].sum(axis=1)
data_costos['Costos generales'] = data_costos.iloc[:, 6:11].sum(axis=1)
data_costos_operativos = data_costos[['Fecha', 'Costos Operativos']]
data_costos_generales = data_costos[['Fecha', 'Costos generales']]

data_costos_operativos['Costos OP AM'] = data_costos_operativos['Costos Operativos'] * (81/155)
data_costos_operativos['Costos OP TR'] = data_costos_operativos['Costos Operativos'] * (74/155)

'''best_distribution_costos_g, best_params_costos_g = best_fit_distribution(data_costos_generales['Costos generales'], bins=200, ax=None)
print(f"Mejor distribución para Costos generales: {best_distribution_costos_g}")
print(f"Parámetros de la mejor distribución para Costos generales: {best_params_costos_g}")
plot_distribucion_ajustada(data_costos_generales, 'Costos generales', best_distribution_costos_g, best_params_costos_g, nbins=30, titulo='Ajuste de distribución para Costos generales')
sim_gastos_g = simular_montecarlo(best_distribution_costos_g, best_params_costos_g)
print(f"Simulación para gastos generales : {sim_gastos_g}")'''


'''best_distribution_costos_op_am, best_params_costos_op_am = best_fit_distribution(data_costos_operativos['Costos OP AM'], bins=200, ax=None)
print(f"Mejor distribución para Costos Operativos AM: {best_distribution_costos_op_am}")
print(f"Parámetros de la mejor distribución para Costos Operativos AM: {best_params_costos_op_am}")
plot_distribucion_ajustada(data_costos_operativos, 'Costos OP AM', best_distribution_costos_op_am, best_params_costos_op_am, nbins=30, titulo='Ajuste de distribución para Costos Operativos AM')
sim_gastos_op_am = simular_montecarlo(best_distribution_costos_op_am, best_params_costos_op_am)
print(f"Simulación para gastos operativos AM: {sim_gastos_op_am}")'''


'''best_distribution_costos_op_tr, best_params_costos_op_tr = best_fit_distribution(data_costos_operativos['Costos OP TR'], bins=200, ax=None)
print(f"Mejor distribución para Costos Operativos TM: {best_distribution_costos_op_tr}")
print(f"Parámetros de la mejor distribución para Costos Operativos TM: {best_params_costos_op_tr}")
plot_distribucion_ajustada(data_costos_operativos, 'Costos OP TR', best_distribution_costos_op_tr, best_params_costos_op_tr, nbins=30, titulo='Ajuste de distribución para Costos Operativos TR')
sim_gastos_op_tr = simular_montecarlo(best_distribution_costos_op_tr, best_params_costos_op_tr)
print(f"Simulación para gastos operativos TR: {sim_gastos_op_tr}")'''