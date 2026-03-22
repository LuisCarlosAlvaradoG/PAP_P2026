
import numpy as np
import scipy.stats as st
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy import stats


def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    DISTRIBUTIONS = [st.genexpon,st.lognorm,st.lomax,st.nct, st.maxwell,st.mielke,st.nakagami, st.weibull_min, st.powerlognorm,st.norm, st.uniform, st.poisson]
    #DISTRIBUTIONS = [st.norm, st.uniform ]

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params)


def plot_boxplot(data, columna='Ingreso_Total', titulo='Distribución de ingresos por día de la semana'):
    
    custom_blues = [
        "#1B3A6B", "#2E6DB4", "#3D85C8", "#5BA3D9",
        "#74B5E3", "#92C4E8", "#B5D8F2", "#D8EBF7",
    ]
    dias_nombre = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    fig = go.Figure()

    for i, nombre in enumerate(dias_nombre):
        datos_dia = data[data['dia_semana'] == i][columna]
        fig.add_trace(go.Box(
            y=datos_dia,
            name=nombre,
            marker_color=custom_blues[i],
            line=dict(color=custom_blues[i], width=1.5),
            fillcolor=custom_blues[i],
            opacity=0.85,
            boxmean=True,
        ))

    fig.update_layout(
        title=dict(text=titulo, font=dict(color='#1B3A6B')),
        yaxis_title='Ingresos',
        xaxis_title='Día',
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor='white', showline=False),
    )

    fig.add_shape(
        type='rect', xref='paper', yref='paper',
        x0=0, y0=0, x1=1, y1=1,
        fillcolor='#E5ECF6', line_width=0, layer='below',
    )

    fig.show()


def plot_histograma(df_sabado, df_domingo, columna='Ingreso_Total', titulo='Ingresos: Sábado vs Domingo'):

    custom_blues = [
        "#1B3A6B", "#2E6DB4", "#3D85C8", "#5BA3D9",
        "#74B5E3", "#92C4E8", "#B5D8F2", "#D8EBF7",
    ]

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=df_sabado[columna],
        name='Sábado',
        marker_color=custom_blues[1],
        opacity=0.70,
        nbinsx=30,
    ))

    fig.add_trace(go.Histogram(
        x=df_domingo[columna],
        name='Domingo',
        marker_color=custom_blues[4],
        opacity=0.70,
        nbinsx=30,
    ))

    fig.update_layout(
        barmode='overlay',
        title=dict(text=titulo, font=dict(color='#1B3A6B')),
        xaxis_title='Ingresos',
        yaxis_title='Frecuencia',
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor='white', showline=False),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02,
            xanchor='right', x=1,
            font=dict(color='#1B3A6B')
        ),
    )

    fig.add_shape(
        type='rect', xref='paper', yref='paper',
        x0=0, y0=0, x1=1, y1=1,
        fillcolor='#E5ECF6', line_width=0, layer='below',
    )

    fig.show()

    
def plot_distribucion_ajustada(data, columna, distribucion, params, nbins=30, titulo='Distribución ajustada', xlabel='Valor', ylabel='Frecuencia'):

    custom_blues = ["#1B3A6B", "#2E6DB4", "#3D85C8", "#5BA3D9",
                    "#74B5E3", "#92C4E8", "#B5D8F2", "#D8EBF7"]

    valores = data[columna].dropna()
    dist = getattr(stats, distribucion)

    # Escalar el PDF a frecuencias
    n = len(valores)
    bin_width = (valores.max() - valores.min()) / nbins
    x_line = np.linspace(valores.min(), valores.max(), 300)
    y_line = dist.pdf(x_line, *params) * n * bin_width

    fig = go.Figure()

    # Histograma en frecuencias reales
    fig.add_trace(go.Histogram(
        x=valores,
        name='Histograma',
        marker_color=custom_blues[2],
        opacity=0.70,
        nbinsx=nbins,
    ))

    # Línea escalada a frecuencias
    fig.add_trace(go.Scatter(
        x=x_line,
        y=y_line,
        mode='lines',
        name=f'Dist. {distribucion}',
        line=dict(color=custom_blues[0], width=2.5),
    ))

    fig.update_layout(
        height=500,
        width=800,
        title=dict(text=titulo, font=dict(color='#1B3A6B')),
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor='white', showline=False),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02,
            xanchor='right', x=1,
            font=dict(color='#1B3A6B')
        ),
    )

    fig.add_shape(
        type='rect', xref='paper', yref='paper',
        x0=0, y0=0, x1=1, y1=1,
        fillcolor='#E5ECF6', line_width=0, layer='below',
    )

    fig.show()

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
    

def simular_montecarlo(distribucion: str, params: tuple, utilidad=False) -> dict:
    
    dist = getattr(stats, distribucion, None)
    if dist is None:
        raise ValueError(f"Distribución '{distribucion}' no encontrada en scipy.stats.")

    *shape_args, loc, scale = params

    sim = dist.rvs(*shape_args, loc=loc, scale=scale, size=1_000_000)

    # Solo filtra negativos si NO es utilidad
    if not utilidad:
        sim = sim[sim > 0]

    return {
        "esperado": sim.mean(),
        "P5":  np.percentile(sim, 5),
        "P50": np.percentile(sim, 50),
        "P95": np.percentile(sim, 95),
    }