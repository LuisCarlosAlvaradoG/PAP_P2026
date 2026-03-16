import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

data = pd.read_csv('Ingresos Troncal limpio.csv')
cols = ['Efectivo', 'Overpay', 'Monto Pasajes', 'Monto Tarjeta Gral','Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error', 'Monto Total Efectivo', 'Monto Total Tarjetas']  

df_por_dia = (
   data
   .groupby('Fecha', as_index=False)[cols]
   .sum()
)

cols_a_sumar = ['Efectivo', 'Monto Tarjeta Gral','Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error']  

df_por_dia['Ingreso_Total'] = df_por_dia[cols_a_sumar].sum(axis=1)

df_por_dia['Fecha'] = pd.to_datetime(df_por_dia['Fecha'])

x = df_por_dia[cols_a_sumar]
y = df_por_dia['Ingreso_Total']

model = sm.OLS(y, x).fit()
predictions = model.predict(x)
print(model.summary())
