import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from funciones_KPI import preparar_y_agrupar, calcular_kpi, plot_kpi

def main():

    # Gastos Generales

    gastos_generales = pd.read_csv('Data/Gastos.csv')
    gastos_generales['Fecha'] = pd.to_datetime(gastos_generales['Fecha'], format='mixed', dayfirst=True)
    gastos_generales['Gastos_Generales'] = gastos_generales[['Gastos Administrativos', 'Gastos Financieros', \
                               'Gastos no fiscales', 'ISR  Ejercicio', 'ISR Facilidades Administrativas']].sum(axis=1)
    
    # Kilómetros

    data_km = pd.read_csv('Data/Kilometros.csv')
    data_km['Unidad'] = data_km['Unidad'].replace(r'^\s*$', np.nan, regex=True)
    data_km = data_km.dropna(subset=['Unidad'])

    # Preparar datos para KPI

    gastos_generales_anual = preparar_y_agrupar(gastos_generales, 'Fecha', 'Gastos_Generales', 'anual')
    gastos_generales_mensual = preparar_y_agrupar(gastos_generales, 'Fecha', 'Gastos_Generales', 'mensual')

    #KPI GASTO / KILOMETROS REALIZADOS ANUAL Y MENSUAL

    data_km_anual = preparar_y_agrupar(data_km, 'Fecha', 'Km Realizados', 'anual').iloc[:-1]    
    data_km_mensual = preparar_y_agrupar(data_km, 'Fecha', 'Km Realizados', 'mensual').iloc[:-2]


    KPI_GG_KMR_ANUAL = calcular_kpi(gastos_generales_anual, data_km_anual, 'Gastos_Generales','Km Realizados', 'Gasto por Km Realizado')
    KPI_GG_KMR_MENSUAL = calcular_kpi(gastos_generales_mensual, data_km_mensual, 'Gastos_Generales', 'Km Realizados', 'Gasto por Km Realizado')


    # KPI GASTO / KILOMETROS PROGRAMADOS ANUAL Y MENSUAL

    data_km_anual_programados = preparar_y_agrupar(data_km, 'Fecha', 'Km Programados', 'anual').iloc[:-1]
    data_km_mensual_programados = preparar_y_agrupar(data_km, 'Fecha', 'Km Programados', 'mensual').iloc[:-2]

    KPI_GG_KMT_ANUAL = calcular_kpi(gastos_generales_anual, data_km_anual_programados, 'Gastos_Generales', 'Km Programados', 'Gasto por Km Programado')
    KPI_GG_KMT_MENSUAL = calcular_kpi(gastos_generales_mensual, data_km_mensual_programados, 'Gastos_Generales', 'Km Programados', 'Gasto por Km Programado')

    # Gráficas

    plot_kpi(KPI_GG_KMR_ANUAL, 'Periodo', 'Gasto por Km Realizado', 'Gasto por Km Realizado Anual')
    plot_kpi(KPI_GG_KMR_MENSUAL, 'Periodo', 'Gasto por Km Realizado', 'Gasto por Km Realizado Mensual')

    plot_kpi(KPI_GG_KMT_ANUAL, 'Periodo', 'Gasto por Km Programado', 'Gasto por Km Programado Anual')
    plot_kpi(KPI_GG_KMT_MENSUAL, 'Periodo', 'Gasto por Km Programado', 'Gasto por Km Programado Mensual')

if __name__ == "__main__":
    main()