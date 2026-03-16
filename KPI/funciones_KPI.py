import pandas as pd
import matplotlib.pyplot as plt

def preparar_y_agrupar_ingresos(df, columna_fecha, columna_valor, periodo):

    df[columna_fecha] = pd.to_datetime(df[columna_fecha], format='mixed', dayfirst=True)

    # agrupar primero por mes
    df['Periodo'] = df[columna_fecha].dt.to_period('M')
    df_mensual = df.groupby('Periodo')[columna_valor].sum().reset_index()

    # quitar primeros 6 meses
    df_mensual = df_mensual.iloc[6:]

    if periodo == "mensual":
        return df_mensual

    elif periodo == "anual":
        df_mensual['Año'] = df_mensual['Periodo'].dt.year
        df_anual = df_mensual.groupby('Año')[columna_valor].sum().reset_index()
        df_anual = df_anual.rename(columns={'Año': 'Periodo'})
        return df_anual
    

def preparar_y_agrupar(df, columna_fecha, columna_valor, periodo):
    
    df[columna_fecha] = pd.to_datetime(df[columna_fecha], format='mixed', dayfirst=True)
    
    if periodo == "anual":
        df['Periodo'] = df[columna_fecha].dt.year
    elif periodo == "mensual":
        df['Periodo'] = df[columna_fecha].dt.to_period('M')
        
    df_agrupado = df.groupby('Periodo')[columna_valor].sum().reset_index()
    
    return df_agrupado


def calcular_kpi(df_valor, df_km, col_valor, col_km, nombre_kpi):
    df = df_valor.merge(df_km, on='Periodo')
    df[nombre_kpi] = df[col_valor] / df[col_km]
    return df

def plot_kpi(kpi_data, x_col, y_col, title):
    plt.figure(figsize=(12, 6))
    plt.plot(kpi_data[x_col].astype(str), kpi_data[y_col], marker='o')
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()

    