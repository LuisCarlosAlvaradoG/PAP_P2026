import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_gastos = pd.read_csv('Data/Gastos.csv')
data_gastos['Fecha'] = pd.to_datetime(data_gastos['Fecha'], format='mixed', dayfirst=True)
data_gastos_op = data_gastos[['Fecha','Gastos de Operación']]


data_km = pd.read_csv('Data/Kilometros.csv')
data_km['Unidad'] = data_km['Unidad'].replace(r'^\s*$', np.nan, regex=True)
data_km = data_km.dropna(subset=['Unidad'])
data_km['Fecha'] = pd.to_datetime(data_km['Fecha'], format='mixed', dayfirst=True)


data_km_am_tr = data_km.groupby('Fecha')['Km Realizados'].sum().reset_index()

data_km_am = data_km[data_km['Unidad'].str.startswith('AM')]
data_km_am = data_km_am.groupby('Fecha')['Km Realizados'].sum().reset_index()
data_km_am = data_km_am.rename(columns={'Km Realizados': 'Km_AM'})

data_km_tr = data_km[data_km['Unidad'].str.startswith('TM')]
data_km_tr = data_km_tr.groupby('Fecha')['Km Realizados'].sum().reset_index()
data_km_tr = data_km_tr.rename(columns={'Km Realizados': 'Km_TR'})

data_completo = data_km_am.merge(data_km_tr, on='Fecha', how='outer')
data_completo = data_completo.merge(data_km_am_tr, on='Fecha', how='outer').iloc[:-2]

data_gastos_km = data_completo.merge(data_gastos_op, on='Fecha', how='outer')

# p = 76 / 155

data_gastos_km["Gastos OP AM"] = data_gastos_km["Gastos de Operación"] * (data_gastos_km["Km_AM"] / data_gastos_km["Km Realizados"])
data_gastos_km["Gastos OP TR"] = data_gastos_km["Gastos de Operación"] * (data_gastos_km["Km_TR"] / data_gastos_km["Km Realizados"])


KPI_OP_AM = data_gastos_km["Gastos OP AM"] / data_gastos_km["Km_AM"]
KPI_OP_TR = data_gastos_km["Gastos OP TR"] / data_gastos_km["Km_TR"]


plt.figure(figsize=(12, 6))
plt.plot(data_gastos_km['Fecha'].astype(str), KPI_OP_AM, marker='o', label='Gasto por Km Realizado AM')
plt.plot(data_gastos_km['Fecha'].astype(str), KPI_OP_TR, marker='o', label='Gasto por Km Realizado TR')
plt.title('Gasto por Km Realizado AM y TR')     
plt.xlabel('Fecha')
plt.ylabel('Gasto por Km Realizado')
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
