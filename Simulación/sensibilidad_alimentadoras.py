import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

data = pd.read_csv('Ingresos Alimentadoras limpio.csv')

cols = ['Efectivo', 'Tarifa Incompleta', 'Overpay', 'Monto Pasajes', 'Monto Tarjeta Gral','Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error', 'Monto Total Efectivo', 'Monto Total Tarjetas']  

df_por_dia = (
   data
   .groupby('Fecha', as_index=False)[cols]
   .sum()
)

cols_a_sumar = ['Efectivo', 'Tarifa Incompleta', 'Monto Tarjeta Gral','Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error']  

df_por_dia['Ingreso_Total'] = df_por_dia[cols_a_sumar].sum(axis=1)

X = df_por_dia[cols_a_sumar]
y = df_por_dia['Ingreso_Total']

model = sm.OLS(y, X).fit()
predictions = model.predict(X)
print(model.summary())