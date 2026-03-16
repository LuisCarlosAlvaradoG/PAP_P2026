
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import gennorm


"""
data = pd.read_csv('Ingresos Alimentadoras limpio.csv')

cols = ['Efectivo', 'Tarifa Incompleta', 'Overpay', 'Monto Pasajes', 'Monto Tarjeta Gral','Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error', 'Monto Total Efectivo', 'Monto Total Tarjetas']  

df_por_dia = (
   data
   .groupby('Fecha', as_index=False)[cols]
   .sum()
)

cols_a_sumar = ['Efectivo', 'Tarifa Incompleta', 'Monto Tarjeta Gral','Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error']  

df_por_dia['Ingreso_Total'] = df_por_dia[cols_a_sumar].sum(axis=1)

ingresos_totales = df_por_dia['Ingreso_Total'].values

plt.hist(ingresos_totales, bins=30, edgecolor='black')
plt.title('Histograma de Ingresos Totales')
plt.xlabel('Monto Ingresos Totales')
plt.ylabel('Frecuencia')
plt.show()
"""

data = pd.read_csv('Ingresos Alimentadoras IQR.csv')
ingresos = data['Ingreso_Total']

plt.hist(ingresos, bins=30, edgecolor='black', color = 'skyblue', density=True, alpha=0.6)

# Crear valores para la curva
x = np.linspace(ingresos.min(), ingresos.max(), 1000)
pdf = gennorm.pdf(x, 5.604727975412163, loc=227566.34490851156, scale=107012.69421016643)

# Graficar curva gennorm
plt.plot(x, pdf, 'r-', lw=2, color = "navy", label=f'Gennorm fit')

# Añadir títulos y leyenda
plt.xlabel('Ingresos Totales')
plt.ylabel('Densidad')
plt.legend()
plt.show()
