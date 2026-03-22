
import numpy as np
import scipy.stats as st
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from Funcion_ajuste import best_fit_distribution, plot_boxplot, plot_histograma, plot_distribucion_ajustada, simular_montecarlo

# Ingresos Troncal

data = pd.read_csv('Data/Ingresos Troncal distribucion.csv')
data['Fecha'] = pd.to_datetime(data['Fecha'], format='mixed', dayfirst=True, errors='coerce')
data = data.groupby('Fecha')['Ingreso Total'].sum().reset_index()

data['dia_semana'] = data['Fecha'].dt.dayofweek 

df_semana  = data[data['dia_semana'].between(0, 4)].copy()  
df_sabado  = data[data['dia_semana'] == 5].copy()            
df_domingo = data[data['dia_semana'] == 6].copy()  

# Graficas 

#plot_boxplot(data, columna='Ingreso Total', titulo='Distribución de ingresos por día de la semana')
#plot_histograma(df_sabado, df_domingo, columna='Ingreso Total', titulo='Ingresos: Sábado vs Domingo')

# Ajuste de distribución

'''best_distribution_week, best_params_week = best_fit_distribution(df_semana['Ingreso Total'], bins=200, ax=None)
print(f"Mejor distribución para días de semana: {best_distribution_week}")
print(f"Parámetros de la mejor distribución para días de semana: {best_params_week}")
plot_distribucion_ajustada(df_semana, 'Ingreso Total', best_distribution_week, best_params_week, nbins=30, titulo='Ajuste de distribución para días de semana')
sim_week = simular_montecarlo(best_distribution_week, best_params_week)
print(f"Simulación para días de semana: {sim_week}")'''


'''best_distribution_sabado, best_params_sabado = best_fit_distribution(df_sabado['Ingreso Total'], bins=200, ax=None)
print(f"Mejor distribución para sábado: {best_distribution_sabado}")
print(f"Parámetros de la mejor distribución para sábado: {best_params_sabado}")
plot_distribucion_ajustada(df_sabado,'Ingreso Total', best_distribution_sabado, best_params_sabado, nbins=30, titulo='Ajuste de distribución para sábado')
sim_sabado = simular_montecarlo(best_distribution_sabado, best_params_sabado)
print(f"Simulación para sábado: {sim_sabado}")'''

'''best_distribution_domingo, best_params_domingo = best_fit_distribution(df_domingo['Ingreso Total'], bins=200, ax=None)
print(f"Mejor distribución para domingo: {best_distribution_domingo}")
print(f"Parámetros de la mejor distribución para domingo: {best_params_domingo}")
plot_distribucion_ajustada(df_domingo, 'Ingreso Total', best_distribution_domingo, best_params_domingo, nbins=30, titulo='Ajuste de distribución para domingo')
sim_domingo = simular_montecarlo(best_distribution_domingo, best_params_domingo)
print(f"Simulación para domingo: {sim_domingo}")'''
