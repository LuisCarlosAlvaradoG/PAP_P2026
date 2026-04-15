import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from funciones_KPI import preparar_y_agrupar_ingresos, preparar_y_agrupar, calcular_kpi, dual_subplot

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
    data_km = data_km.dropna(subset=['Unidad'])

    data_km_am = data_km[data_km['Unidad'].str.startswith('AM')]
    data_km_tr = data_km[data_km['Unidad'].str.startswith('TM')]

    # Costos Operativos
    data_costos = pd.read_csv('Data/Gastos.csv')

    data_costos['Fecha'] = pd.to_datetime(data_costos['Fecha'], format='mixed', dayfirst=True)
    data_costos['Costos Operativos'] = data_costos[['Costo de Venta (Refacciones)', 'Gastos de Operación', 'Gastos de Mantenimiento']].sum(axis=1)
    data_costos['Costos generales'] = data_costos.iloc[:, 6:11].sum(axis=1)
    data_costos_operativos = data_costos[['Fecha', 'Costos Operativos']]
    data_costos_generales = data_costos[['Fecha', 'Costos generales']]
    
    # Utilidad
    data_utilidad = pd.read_csv('Data/Utilidad mensual.csv')
    data_utilidad['Periodo'] = pd.to_datetime(data_utilidad['Periodo']).dt.to_period('M')
    
    

    # Preparar ingresos para KPI

    ingresos_anual_alimentadoras = preparar_y_agrupar_ingresos(df_anual_alimentadoras, 'Fecha', 'Ingreso_Total', 'anual').iloc[:-1]
    ingresos_mensual_alimentadoras = preparar_y_agrupar_ingresos(df_mensual_alimentadoras, 'Fecha', 'Ingreso_Total', 'mensual').iloc[:-2]
    ingresos_anual_troncal = preparar_y_agrupar_ingresos(df_anual_troncal, 'Fecha', 'Ingreso_Total', 'anual').iloc[:-1]
    ingresos_mensual_troncal = preparar_y_agrupar_ingresos(df_mensual_troncal, 'Fecha', 'Ingreso_Total', 'mensual').iloc[:-2]

    # Preparar kilómetros para KPI
    km_real_anual_am = preparar_y_agrupar(data_km_am, 'Fecha', 'Km Realizados', 'anual')
    km_real_anual_tr = preparar_y_agrupar(data_km_tr, 'Fecha', 'Km Realizados', 'anual')
    km_prog_anual_am = preparar_y_agrupar(data_km_am, 'Fecha', 'Km Programados', 'anual')
    km_prog_anual_tr = preparar_y_agrupar(data_km_tr, 'Fecha', 'Km Programados', 'anual')
    km_real_mensual_am = preparar_y_agrupar(data_km_am, 'Fecha', 'Km Realizados', 'mensual')
    km_real_mensual_tr = preparar_y_agrupar(data_km_tr, 'Fecha', 'Km Realizados', 'mensual')
    km_prog_mensual_am = preparar_y_agrupar(data_km_am, 'Fecha', 'Km Programados', 'mensual')
    km_prog_mensual_tr = preparar_y_agrupar(data_km_tr, 'Fecha', 'Km Programados', 'mensual')

    # Preparar costos para KPI

    costos_generales_anual = preparar_y_agrupar(data_costos_generales, 'Fecha', 'Costos generales', 'anual')
    costos_generales_mensual = preparar_y_agrupar(data_costos_generales, 'Fecha', 'Costos generales', 'mensual')

    data_costos_operativos['Costos OP AM'] = data_costos_operativos['Costos Operativos'] * (81/155)
    data_costos_operativos['Costos OP TR'] = data_costos_operativos['Costos Operativos'] * (74/155)

    costos_operativos_anuales_am = preparar_y_agrupar(data_costos_operativos, 'Fecha', 'Costos OP AM', 'anual')
    costos_operativos_anuales_tr = preparar_y_agrupar(data_costos_operativos, 'Fecha', 'Costos OP TR', 'anual')
    costos_operativos_mensuales_am = preparar_y_agrupar(data_costos_operativos, 'Fecha', 'Costos OP AM', 'mensual')
    costos_operativos_mensuales_tr = preparar_y_agrupar(data_costos_operativos, 'Fecha', 'Costos OP TR', 'mensual')
    costos_operativos_mensuales_am_M = data_costos_operativos[['Fecha', 'Costos OP AM']]
    costos_operativos_mensuales_tr_M = data_costos_operativos[['Fecha', 'Costos OP TR']]

    # KPI INGRESO / KILOMETROS  

    KPI_IN_KMR_ANUAL_TR = calcular_kpi(ingresos_anual_troncal, km_real_anual_tr, 'Ingreso_Total', 'Km Realizados', 'Ingreso por Km Realizado')
    KPI_IN_KMP_ANUAL_TR = calcular_kpi(ingresos_anual_troncal, km_prog_anual_tr, 'Ingreso_Total', 'Km Programados', 'Ingreso por Km Programado')
    KPI_IN_KMR_ANUAL_AM = calcular_kpi(ingresos_anual_alimentadoras, km_real_anual_am, 'Ingreso_Total', 'Km Realizados', 'Ingreso por Km Realizado')
    KPI_IN_KMP_ANUAL_AM = calcular_kpi(ingresos_anual_alimentadoras, km_prog_anual_am, 'Ingreso_Total', 'Km Programados', 'Ingreso por Km Programado')

    KPI_IN_KMR_MENSUAL_TR = calcular_kpi(ingresos_mensual_troncal, km_real_mensual_tr, 'Ingreso_Total', 'Km Realizados', 'Ingreso por Km Realizado')
    KPI_IN_KMP_MENSUAL_TR = calcular_kpi(ingresos_mensual_troncal, km_prog_mensual_tr, 'Ingreso_Total', 'Km Programados', 'Ingreso por Km Programado')
    KPI_IN_KMR_MENSUAL_AM = calcular_kpi(ingresos_mensual_alimentadoras, km_real_mensual_am, 'Ingreso_Total', 'Km Realizados', 'Ingreso por Km Realizado')
    KPI_IN_KMP_MENSUAL_AM = calcular_kpi(ingresos_mensual_alimentadoras, km_prog_mensual_am, 'Ingreso_Total', 'Km Programados', 'Ingreso por Km Programado')


    # KPI COSTO GENERAL / KILOMETROS

    KPI_CG_KMR_ANUAL_TR = calcular_kpi(costos_generales_anual, km_real_anual_tr, 'Costos generales', 'Km Realizados', 'Costo General por Km Realizado')
    KPI_CG_KMP_ANUAL_TR = calcular_kpi(costos_generales_anual, km_prog_anual_tr, 'Costos generales', 'Km Programados', 'Costo General por Km Programado')
    KPI_CG_KMR_ANUAL_AM = calcular_kpi(costos_generales_anual, km_real_anual_am, 'Costos generales', 'Km Realizados', 'Costo General por Km Realizado')
    KPI_CG_KMP_ANUAL_AM = calcular_kpi(costos_generales_anual, km_prog_anual_am, 'Costos generales', 'Km Programados', 'Costo General por Km Programado')

    # KPI COSTO OPERATIVO / KILOMETROS

    KPI_CO_KMR_ANUAL_TR = calcular_kpi(costos_operativos_anuales_tr, km_real_anual_tr, 'Costos OP TR', 'Km Realizados', 'Costo Operativo por Km Realizado')
    KPI_CO_KMP_ANUAL_TR = calcular_kpi(costos_operativos_anuales_tr, km_prog_anual_tr, 'Costos OP TR', 'Km Programados', 'Costo Operativo por Km Programado')
    KPI_CO_KMR_ANUAL_AM = calcular_kpi(costos_operativos_anuales_am, km_real_anual_am, 'Costos OP AM', 'Km Realizados', 'Costo Operativo por Km Realizado')
    KPI_CO_KMP_ANUAL_AM = calcular_kpi(costos_operativos_anuales_am, km_prog_anual_am, 'Costos OP AM', 'Km Programados', 'Costo Operativo por Km Programado')

    KPI_CO_KMR_MENSUAL_TR = calcular_kpi(costos_operativos_mensuales_tr, km_real_mensual_tr, 'Costos OP TR', 'Km Realizados', 'Costo Operativo por Km Realizado')
    KPI_CO_KMP_MENSUAL_TR = calcular_kpi(costos_operativos_mensuales_tr, km_prog_mensual_tr, 'Costos OP TR', 'Km Programados', 'Costo Operativo por Km Programado')
    KPI_CO_KMR_MENSUAL_AM = calcular_kpi(costos_operativos_mensuales_am, km_real_mensual_am, 'Costos OP AM', 'Km Realizados', 'Costo Operativo por Km Realizado')
    KPI_CO_KMP_MENSUAL_AM = calcular_kpi(costos_operativos_mensuales_am, km_prog_mensual_am, 'Costos OP AM', 'Km Programados', 'Costo Operativo por Km Programado')

    #KPI UTILIDAD / KILOMETROS
    KPI_UT_KMR_MENSUAL_AM = calcular_kpi(data_utilidad, km_prog_mensual_am, 'Utilidad AM', 'Km Programados', 'Utilidad por Km Programado')
    KPI_UT_KMR_MENSUAL_TR = calcular_kpi(data_utilidad, km_prog_mensual_tr, 'Utilidad TR', 'Km Programados', 'Utilidad por Km Programado')
    
    # Graficas

    dual_subplot(KPI_IN_KMR_ANUAL_TR['Ingreso por Km Realizado'], KPI_CO_KMR_ANUAL_TR['Costo Operativo por Km Realizado'] ,
                 KPI_IN_KMP_ANUAL_TR['Ingreso por Km Programado'], KPI_CO_KMP_ANUAL_TR['Costo Operativo por Km Programado'], 
                KPI_IN_KMR_ANUAL_TR['Periodo'], 'Año','Monto por KM', 10, 
                'Ingreso vs Costo Operativo por Km Realizado Anual Troncal', 
                'Ingreso vs Costo Operativo por Km Programado Anual Troncal',
                'Ingresos', 'Costos', 'Ingresos', 'Costos')
    
    '''dual_subplot(KPI_IN_KMR_ANUAL_AM['Ingreso por Km Realizado'], KPI_CO_KMR_ANUAL_AM['Costo Operativo por Km Realizado'] ,
                 KPI_IN_KMP_ANUAL_AM['Ingreso por Km Programado'], KPI_CO_KMP_ANUAL_AM['Costo Operativo por Km Programado'], 
                KPI_IN_KMR_ANUAL_AM['Periodo'], 'Año','Monto por KM', 10, 
                'Ingreso vs Costo Operativo por Km Realizado Anual Alimentadoras', 
                'Ingreso vs Costo Operativo por Km Programado Anual Alimentadoras',
                'Ingresos', 'Costos', 'Ingresos', 'Costos')'''
    
    '''dual_subplot(KPI_IN_KMR_MENSUAL_TR['Ingreso por Km Realizado'], KPI_CO_KMR_MENSUAL_TR['Costo Operativo por Km Realizado'] ,
                 KPI_IN_KMP_MENSUAL_TR['Ingreso por Km Programado'], KPI_CO_KMP_MENSUAL_TR['Costo Operativo por Km Programado'], 
                KPI_IN_KMR_MENSUAL_TR['Periodo'], 'Mes','Monto por KM', 7, 
                'Ingreso vs Costo Operativo por Km Realizado Mensual Troncal', 
                'Ingreso vs Costo Operativo por Km Programado Mensual Troncal',
                'Ingresos', 'Costos', 'Ingresos', 'Costos')'''
    
    '''dual_subplot(KPI_IN_KMR_MENSUAL_AM['Ingreso por Km Realizado'], KPI_CO_KMR_MENSUAL_AM['Costo Operativo por Km Realizado'] ,
                 KPI_IN_KMP_MENSUAL_AM['Ingreso por Km Programado'], KPI_CO_KMP_MENSUAL_AM['Costo Operativo por Km Programado'], 
                KPI_IN_KMR_MENSUAL_AM['Periodo'], 'Mes','Monto por KM', 3, 
                'Ingreso vs Costo Operativo por Km Realizado Mensual Alimentadoras', 
                'Ingreso vs Costo Operativo por Km Programado Mensual Alimentadoras',
                'Ingresos', 'Costos', 'Ingresos', 'Costos')'''
                

    '''single_plot(KPI_UT_KMR_MENSUAL_AM['Utilidad por Km Programado'], KPI_UT_KMR_MENSUAL_TR['Utilidad por Km Programado'], 
                KPI_UT_KMR_MENSUAL_AM['Periodo'], 'Mes', 'Utilidad por Km Programado', 10, 'Utilidad por Km Programado Mensual',
                'Alimentadoras', 'Troncal')'''



if __name__ == "__main__":
    main()