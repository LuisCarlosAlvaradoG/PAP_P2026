import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import norm


data = pd.read_csv('Ingresos Troncal limpio.csv')

cols = ['Efectivo', 'Overpay', 'Monto Pasajes', 'Monto Tarjeta Gral','Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error', 'Monto Total Efectivo', 'Monto Total Tarjetas']  

df_por_dia = (
   data
   .groupby('Fecha', as_index=False)[cols]
   .sum()
)

cols_a_sumar = ['Efectivo', 'Monto Tarjeta Gral','Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error']  

df_por_dia['Ingreso_Total'] = df_por_dia[cols_a_sumar].sum(axis=1)

ingresos_totales = df_por_dia['Ingreso_Total'].values

count, bins, ignored = plt.hist(ingresos_totales, bins=30, density=True, alpha=0.6, color='skyblue', edgecolor='black')


mu, sigma = ingresos_totales.mean(), ingresos_totales.std()
x = np.linspace(min(ingresos_totales), max(ingresos_totales), 100)
plt.plot(x, norm.pdf(x, mu, sigma), color='navy', lw=2, label='Normal fit')


plt.xlabel('Monto Ingresos Totales')
plt.ylabel('Densidad')
plt.legend()
plt.show()


"""
data = pd.read_csv('Ingresos Troncal IQR.csv')

plt.hist(data['Ingreso_Total'], bins=30, edgecolor='black')
plt.title('Histograma de Ingresos Totales')
plt.xlabel('Monto Ingresos Totales')
plt.ylabel('Frecuencia')
plt.show()
"""