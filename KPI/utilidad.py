import pandas as pd
import numpy as np
from funciones_KPI import preparar_y_agrupar, dual_subplot

data_utilidad = pd.read_csv('Data/Utilidad mensual.csv')
data_utilidad['Periodo'] = pd.to_datetime(data_utilidad['Periodo']).dt.to_period('M')

data_km = pd.read_csv('Data/Kilometros.csv')
data_km['Unidad'] = data_km['Unidad'].replace(r'^\s*$', np.nan, regex=True)
data_km = data_km.dropna(subset=['Unidad'])

data_km_am = data_km[data_km['Unidad'].str.startswith('AM')]
data_km_tr = data_km[data_km['Unidad'].str.startswith('TM')]

km_prog_mensual_am = preparar_y_agrupar(data_km_am, 'Fecha', 'Km Programados', 'mensual').iloc[:-2]
km_prog_mensual_tr = preparar_y_agrupar(data_km_tr, 'Fecha', 'Km Programados', 'mensual').iloc[:-2]

data = pd.merge(data_utilidad, km_prog_mensual_am, on='Periodo', how='inner')
data = pd.merge(data, km_prog_mensual_tr, on='Periodo', how='inner')
data = data.rename(columns={'Km Programados_x': 'Km Programados AM', 'Km Programados_y': 'Km Programados TR'})

data['Utilidad AM por Km'] = data['Utilidad AM'] / data['Km Programados AM']
data['Utilidad TR por Km'] = data['Utilidad TR'] / data['Km Programados TR']


dual_subplot(data['Utilidad AM por Km'], data['Utilidad TR por Km'], data['Utilidad AM por Km'], data['Utilidad TR por Km'],
                 data['Periodo'], 'Mes','Utilidad por Km', 10, 
                 'Utilidad por Km Realizado Mensual AM', 
                 'Utilidad por Km Realizado Mensual TR',
                 'Utilidad por Km AM', 'Utilidad por Km TR', 'Utilidad por Km AM', 'Utilidad por Km TR')
