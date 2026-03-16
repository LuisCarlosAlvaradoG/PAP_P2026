import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from funciones_KPI import preparar_y_agrupar_ingresos, preparar_y_agrupar, calcular_kpi, plot_kpi



def main():

    ## Ingresos Alimentadoras

    data_alimentadoras = pd.read_csv('Data/Ingresos Alimentadoras limpio.csv')
    cols_a_sumar_alimentadoras = ['Efectivo', 'Tarifa Incompleta', 'Monto Tarjeta Gral','Monto Tarjeta Per','Monto Tarjeta Bpd', 'Recargas', 'Recargas Error']
    data_alimentadoras['Ingreso_Total'] = data_alimentadoras[cols_a_sumar_alimentadoras].sum(axis=1)
    df_anual_alimentadoras = data_alimentadoras.copy()
    df_mensual_alimentadoras = data_alimentadoras.copy()

    ## Ingresos Troncal

    data_troncal = pd.read_csv('Data/Ingresos Troncal limpio.csv')
    cols_a_sumar_troncal = ['Efectivo', 'Monto Tarjeta Gral','Monto Tarjeta Per','Monto Tarjeta Bpd', 'Recargas', 'Recargas Error']
    data_troncal['Ingreso_Total'] = data_troncal[cols_a_sumar_troncal].sum(axis=1)
    df_anual_troncal = data_troncal.copy()
    df_mensual_troncal = data_troncal.copy()

    ## Kilómetros 

    data_km = pd.read_csv('Data/Kilometros.csv')
    data_km['Unidad'] = data_km['Unidad'].replace(r'^\s*$', np.nan, regex=True)
    data_km = data_km.dropna(subset=['Unidad']) ## !!!!!!!!! IMPORTANTE MENCIONAR A LUIS; ELIMINAMOS DATOS QUE NO SABIAMOS

    data_km_am = data_km[data_km['Unidad'].str.startswith('AM')]
    data_km_tr = data_km[data_km['Unidad'].str.startswith('TM')]


    # Preparar ingresos para KPI

    ingresos_anual_alimentadoras = preparar_y_agrupar_ingresos(df_anual_alimentadoras, 'Fecha', 'Ingreso_Total', 'anual')
    ingresos_mensual_alimentadoras = preparar_y_agrupar_ingresos(df_mensual_alimentadoras, 'Fecha', 'Ingreso_Total', 'mensual')

    ingresos_anual_troncal = preparar_y_agrupar_ingresos(df_anual_troncal, 'Fecha', 'Ingreso_Total', 'anual')
    ingresos_mensual_troncal = preparar_y_agrupar_ingresos(df_mensual_troncal, 'Fecha', 'Ingreso_Total', 'mensual')

    
    # KPI INGRESO / KILOMETROS REALIZADOS ANUAL

    km_real_anual_am = preparar_y_agrupar(data_km_am, 'Fecha', 'Km Realizados', 'anual')
    km_real_anual_tr = preparar_y_agrupar(data_km_tr, 'Fecha', 'Km Realizados', 'anual')

    KPI_IN_KMR_ANUAL_AM = calcular_kpi(ingresos_anual_alimentadoras, km_real_anual_am, 'Ingreso_Total', 'Km Realizados', 'Ingreso por Km Realizado')
    KPI_IN_KMR_ANUAL_TR = calcular_kpi(ingresos_anual_troncal, km_real_anual_tr, 'Ingreso_Total', 'Km Realizados', 'Ingreso por Km Realizado')


    # KPI INGRESO / KILOMETROS PROGRAMADOS ANUAL

    km_tot_anual_am = preparar_y_agrupar(data_km_am, 'Fecha', 'Km Programados', 'anual')
    km_tot_anual_tr = preparar_y_agrupar(data_km_tr, 'Fecha', 'Km Programados', 'anual')

    KPI_IN_KMT_ANUAL_AM = calcular_kpi(ingresos_anual_alimentadoras, km_tot_anual_am, 'Ingreso_Total', 'Km Programados', 'Ingreso por Km Programado')
    KPI_IN_KMT_ANUAL_TR = calcular_kpi(ingresos_anual_troncal, km_tot_anual_tr, 'Ingreso_Total', 'Km Programados', 'Ingreso por Km Programado') 

    # KPI INGRESO / KILOMETROS REALIZADOS MENSUAL

    km_real_mensual_am = preparar_y_agrupar(data_km_am, 'Fecha', 'Km Realizados', 'mensual')
    km_real_mensual_tr = preparar_y_agrupar(data_km_tr, 'Fecha', 'Km Realizados', 'mensual')

    KPI_IN_KMR_MENSUAL_AM = calcular_kpi(ingresos_mensual_alimentadoras, km_real_mensual_am, 'Ingreso_Total', 'Km Realizados', 'Ingreso por Km Realizado')
    KPI_IN_KMR_MENSUAL_TR = calcular_kpi(ingresos_mensual_troncal, km_real_mensual_tr, 'Ingreso_Total', 'Km Realizados', 'Ingreso por Km Realizado')


    # KPI INGRESO / KILOMETROS PROGRAMADOS MENSUAL

    km_tot_mensual_am = preparar_y_agrupar(data_km_am, 'Fecha', 'Km Programados', 'mensual')
    km_tot_mensual_tr = preparar_y_agrupar(data_km_tr, 'Fecha', 'Km Programados', 'mensual')

    KPI_IN_KMT_MENSUAL_AM = calcular_kpi(ingresos_mensual_alimentadoras, km_tot_mensual_am, 'Ingreso_Total', 'Km Programados', 'Ingreso por Km Programado')
    KPI_IN_KMT_MENSUAL_TR = calcular_kpi(ingresos_mensual_troncal, km_tot_mensual_tr, 'Ingreso_Total', 'Km Programados', 'Ingreso por Km Programado')
    
    # Gráficos

    plot_kpi(KPI_IN_KMR_ANUAL_AM, 'Periodo', 'Ingreso por Km Realizado', 'Ingreso por Km Realizado Anual')
    plot_kpi(KPI_IN_KMT_ANUAL_AM, 'Periodo', 'Ingreso por Km Programado', 'Ingreso por Km Programado Anual')
    plot_kpi(KPI_IN_KMR_MENSUAL_AM, 'Periodo', 'Ingreso por Km Realizado', 'Ingreso por Km Realizado Mensual')
    plot_kpi(KPI_IN_KMT_MENSUAL_AM, 'Periodo', 'Ingreso por Km Programado', 'Ingreso por Km Programado Mensual')

    plot_kpi(KPI_IN_KMR_ANUAL_TR, 'Periodo', 'Ingreso por Km Realizado', 'Ingreso por Km Realizado Anual')
    plot_kpi(KPI_IN_KMT_ANUAL_TR, 'Periodo', 'Ingreso por Km Programado', 'Ingreso por Km Programado Anual')
    plot_kpi(KPI_IN_KMR_MENSUAL_TR, 'Periodo', 'Ingreso por Km Realizado', 'Ingreso por Km Realizado Mensual')
    plot_kpi(KPI_IN_KMT_MENSUAL_TR, 'Periodo', 'Ingreso por Km Programado', 'Ingreso por Km Programado Mensual')


if __name__ == "__main__":
    main()