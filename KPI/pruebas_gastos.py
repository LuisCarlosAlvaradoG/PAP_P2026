import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Bajar datos

df = pd.read_csv('Data/Gastos.csv')
df['Fecha'] = pd.to_datetime(df['Fecha'], format='mixed', dayfirst=True)
df['Gastos_Generales'] = df[['Gastos Administrativos', 'Gastos Financieros', \
                               'Gastos no fiscales', 'ISR  Ejercicio', 'ISR Facilidades Administrativas']].sum(axis=1)


'''df['Periodo'] = df['Fecha'].dt.to_period('M')
df_mensual = df.groupby('Periodo')['Gastos_Generales'].sum().reset_index()


data = pd.read_csv('Data/Kilometros.csv')
data['Fecha'] = pd.to_datetime(data['Fecha'], format='mixed', dayfirst=True)
data['Periodo'] = data['Fecha'].dt.to_period('M')
data_km = data.groupby('Periodo')['Km Realizados'].sum().reset_index()

df_kpi = df_mensual.merge(data_km, on='Periodo')
df_kpi['Gasto por Km Realizado'] = df_kpi['Gastos_Generales'] / df_kpi['Km Realizados']'''


df['Periodo'] = df['Fecha'].dt.year
df_anual = df.groupby('Periodo')['Gastos_Generales'].sum().reset_index()

data = pd.read_csv('Data/Kilometros.csv')
data['Fecha'] = pd.to_datetime(data['Fecha'], format='mixed', dayfirst=True)
data['Periodo'] = data['Fecha'].dt.year
data_km = data.groupby('Periodo')['Km Realizados'].sum().reset_index()

df_kpi = df_anual.merge(data_km, on='Periodo')
df_kpi['Gasto por Km Realizado'] = df_kpi['Gastos_Generales'] / df_kpi['Km Realizados']



plt.figure(figsize=(12, 6))
plt.plot(df_kpi['Periodo'].astype(str), df_kpi['Gasto por Km Realizado'], marker='o')
plt.title('Gasto por Km Realizado')
plt.xlabel('Periodo')
plt.ylabel('Gasto por Km Realizado')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()