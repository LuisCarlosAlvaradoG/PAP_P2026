import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def preparar_y_agrupar_ingresos(df, columna_fecha, columna_valor, periodo):

    df[columna_fecha] = pd.to_datetime(df[columna_fecha], format='mixed', dayfirst=True)

    df['Periodo'] = df[columna_fecha].dt.to_period('M')
    df_mensual = df.groupby('Periodo')[columna_valor].sum().reset_index()

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

def plot_kpi_4(kpi_a, kpi_b, kpi_c=None, kpi_d=None, x=None,
             titulo='Comparación de KPIs',
             xlabel='Período',
             ylabel='Valor',
             label_a='KPI A',
             label_b='KPI B',
             label_c='KPI C',
             label_d='KPI D',
             dtick=None):

    custom_purples = [
        "#4A148C", 
        "#6A1B9A", 
        "#9C27B0", 
        "#CE93D8", 
    ]

    if x is None:
        x = list(range(len(kpi_a)))
    else:
        x = [str(v) for v in x]

    if xlabel.lower() == 'mes':
        meses = {
            '01': 'ENE', '02': 'FEB', '03': 'MAR', '04': 'ABR',
            '05': 'MAY', '06': 'JUN', '07': 'JUL', '08': 'AGO',
            '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DIC'
        }
        def formato_tick(p):
            año, mes = p.split('-')
            return f"{meses[mes]}\n{año}" if mes == '01' else meses[mes]
        x_labels = [formato_tick(v) for v in x]
    else:
        x_labels = x

    series = [
        (kpi_a, custom_purples[0], label_a),
        (kpi_b, custom_purples[1], label_b),
        (kpi_c, custom_purples[2], label_c),
        (kpi_d, custom_purples[3], label_d),
    ]

    fig = go.Figure()

    for kpi, color, label in series:
        if kpi is not None:
            fig.add_trace(go.Scatter(
                x=x, y=kpi, mode='lines+markers', name=label,
                line=dict(color=color, width=2),
                marker=dict(color=color, size=8),
            ))

    fig.update_layout(
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(color='#4A148C', size=16, weight='bold')),
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        height=700, width=1400,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        plot_bgcolor='#FAF5FF',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True, gridcolor='#E8D9F0',
            tickmode='array',
            tickvals=x,
            ticktext=x_labels,
            tickangle=-90,
            automargin=True,
            fixedrange=False,
        ),
        yaxis=dict(showgrid=True, gridcolor='#E8D9F0', dtick=dtick),
    )

    return fig


def plot_kpi_2(kpi_a, kpi_b, x=None,
             titulo='Comparación de KPIs',
             xlabel='Período',
             ylabel='Valor',
             label_a='KPI A',
             label_b='KPI B',
             dtick=None):

    custom_purples = ["#4A148C", "#CE93D8"]

    if x is None:
        x = list(range(len(kpi_a)))
    else:
        x = [str(v) for v in x]

    if xlabel.lower() == 'mes':
        meses = {
            '01': 'ENE', '02': 'FEB', '03': 'MAR', '04': 'ABR',
            '05': 'MAY', '06': 'JUN', '07': 'JUL', '08': 'AGO',
            '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DIC'
        }
        def formato_tick(p):
            año, mes = p.split('-')
            return f"{meses[mes]}\n{año}" if mes == '01' else meses[mes]
        x_labels = [formato_tick(v) for v in x]
    else:
        x_labels = x

    series = [
        (kpi_a, custom_purples[0], label_a),
        (kpi_b, custom_purples[1], label_b),
    ]

    fig = go.Figure()

    for kpi, color, label in series:
        fig.add_trace(go.Scatter(
            x=x, y=kpi, mode='lines+markers', name=label,
            line=dict(color=color, width=2),
            marker=dict(color=color, size=8),
        ))

    fig.update_layout(
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(color='#4A148C', size=16, weight='bold')),
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        height=700, width=1400,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        plot_bgcolor='#FAF5FF',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True, gridcolor='#E8D9F0',
            tickmode='array',
            tickvals=x,
            ticktext=x_labels,
            tickangle=0,
            automargin=True,
            fixedrange=False,
        ),
        yaxis=dict(showgrid=True, gridcolor='#E8D9F0', dtick=dtick),
    )

    return fig

def single_plot(
    y1, y2,
    x,
    xlabel,
    ylabel,
    grid_step,
    title,
    legend1, legend2
):
    custom_purples = ["#4A148C", "#CE93D8"]

    x = [str(v) for v in x]

    if xlabel.lower() == 'mes':
        meses = {
            '01': 'ENE', '02': 'FEB', '03': 'MAR', '04': 'ABR',
            '05': 'MAY', '06': 'JUN', '07': 'JUL', '08': 'AGO',
            '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DIC'
        }
        def formato_tick(p):
            año, mes = p.split('-')
            return f"{meses[mes]}\n{año}" if mes == '01' else meses[mes]
        x_labels = [formato_tick(v) for v in x]
    else:
        x_labels = x

    fig = go.Figure()

    # --- Línea 1 (oscura) ---
    fig.add_trace(go.Scatter(
        x=x, y=y1, mode='lines+markers', name=legend1,
        line=dict(color=custom_purples[0], width=2),
        marker=dict(color=custom_purples[0], size=8),
    ))

    fig.add_trace(go.Scatter(
        x=x, y=y2, mode='lines+markers', name=legend2,
        line=dict(color=custom_purples[1], width=2),
        marker=dict(color=custom_purples[1], size=8),
    ))

    axis_style = dict(
        showgrid=True,
        gridcolor='#E8D9F0',
        tickmode='array',
        tickvals=x,
        ticktext=x_labels,
        tickangle=-90,
        automargin=True,
        type='category',
        tickfont=dict(size=9)
    )

    fig.update_layout(
        height=500,
        width=700,
        plot_bgcolor='#FAF5FF',
        paper_bgcolor='white',
        title=dict(text=title, x=0.5, xanchor='center', font=dict(color='#4A148C', size=14, weight='bold')),
        legend=dict(
            orientation='h',
            xanchor='center',
            x=0.5,
            y=1.15,
        ),
        xaxis=dict(**axis_style, title_text=xlabel),
        yaxis=dict(title_text=ylabel, dtick=grid_step, showgrid=True, gridcolor='#E8D9F0'),
    )

    fig.update_xaxes(title_text=xlabel)
    fig.update_yaxes(title_text=ylabel)

    return fig
    

def dual_subplot(
    y1a, y1b,
    y2a, y2b,
    x,
    xlabel,
    ylabel,
    grid_step,
    title1, title2,
    legend1a, legend1b,
    legend2a, legend2b
):

    custom_purples = ["#4A148C", "#CE93D8"]

    x = [str(v) for v in x]

    if xlabel.lower() == 'mes':
        meses = {
            '01': 'ENE', '02': 'FEB', '03': 'MAR', '04': 'ABR',
            '05': 'MAY', '06': 'JUN', '07': 'JUL', '08': 'AGO',
            '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DIC'
        }
        def formato_tick(p):
            año, mes = p.split('-')
            return f"{meses[mes]}\n{año}" if mes == '01' else meses[mes]
        x_labels = [formato_tick(v) for v in x]
    else:
        x_labels = x

    fig = make_subplots(
        rows=1, cols=2,
        horizontal_spacing=0.12
    )

    # --- Gráfica 1 ---
    fig.add_trace(go.Scatter(
        x=x, y=y1a, mode='lines+markers', name=legend1a,
        line=dict(color=custom_purples[0], width=2),
        marker=dict(color=custom_purples[0], size=8),
        legend='legend',
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=x, y=y1b, mode='lines+markers', name=legend1b,
        line=dict(color=custom_purples[1], width=2),
        marker=dict(color=custom_purples[1], size=8),
        legend='legend',
    ), row=1, col=1)

    # --- Gráfica 2 ---
    fig.add_trace(go.Scatter(
        x=x, y=y2a, mode='lines+markers', name=legend2a,
        line=dict(color=custom_purples[0], width=2),
        marker=dict(color=custom_purples[0], size=8),
        legend='legend2',
    ), row=1, col=2)

    fig.add_trace(go.Scatter(
        x=x, y=y2b, mode='lines+markers', name=legend2b,
        line=dict(color=custom_purples[1], width=2),
        marker=dict(color=custom_purples[1], size=8),
        legend='legend2',
    ), row=1, col=2)

    axis_style = dict(
        showgrid=True,
        gridcolor='#E8D9F0',
        tickmode='array',
        tickvals=x,
        ticktext=x_labels,
        tickangle=-90,
        automargin=True,
        type='category',
        tickfont=dict(size=9)
    )

    fig.update_layout(
        height=500,
        width=1400,
        plot_bgcolor='#FAF5FF',
        paper_bgcolor='white',
        annotations=[
            dict(text=title1, x=0.22, y=1.30, xref='paper', yref='paper',
                 showarrow=False, font=dict(size=14, color='#4A148C', weight='bold'), xanchor='center'),
            dict(text=title2, x=0.78, y=1.30, xref='paper', yref='paper',
                 showarrow=False, font=dict(size=14, color='#4A148C', weight='bold'), xanchor='center'),
        ],
        legend=dict(
            orientation='h', xanchor='center', x=0.22, y=1.18,
        ),
        legend2=dict(
            orientation='h', xanchor='center', x=0.78, y=1.18,
        ),
        xaxis =dict(**axis_style, title_text=xlabel),
        xaxis2=dict(**axis_style, title_text=xlabel),
        yaxis =dict(title_text=ylabel, dtick=grid_step, showgrid=True, gridcolor='#E8D9F0'),
        yaxis2=dict(title_text=ylabel, dtick=grid_step, showgrid=True, gridcolor='#E8D9F0'),
    )

    fig.update_xaxes(title_text=xlabel)
    fig.update_yaxes(title_text=ylabel)

    return fig