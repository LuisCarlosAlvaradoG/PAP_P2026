import pandas as pd
import numpy as np
import plotly.graph_objects as go

df = pd.read_csv("Data/Ingresos Alimentadoras limpio.csv")

X = df[[
    "Efectivo", "Tarifa Incompleta",
    "Monto Tarjeta Gral", "Monto Tarjeta Per",
    "Monto Tarjeta Bpd", "Recargas", "Recargas Error"
]]

cov_matrix = X.cov()


contribuciones = cov_matrix.sum(axis=1)
var_Y = contribuciones.sum()
porcentajes = (contribuciones / var_Y) * 100

resultado = pd.DataFrame({
    "Contribucion_absoluta": contribuciones,
    "Contribucion_pct": porcentajes
}).sort_values("Contribucion_pct", ascending=False)


def wrap_text(text, width=12):
    words = text.split()
    lines = []
    current = ""
    
    for w in words:
        if len((current + " " + w).strip()) <= width:
            current = (current + " " + w).strip()
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    
    return "<br>".join(lines)

resultado.index = [wrap_text(str(i), width=12) for i in resultado.index]

custom_blues = [
    "#1B3A6B", "#2E6DB4", "#3D85C8", "#5BA3D9",
    "#74B5E3", "#92C4E8", "#B5D8F2", "#D8EBF7",
]
colores = custom_blues[:len(resultado)]


fig = go.Figure()

fig.add_trace(go.Bar(
    x=resultado.index,
    y=resultado["Contribucion_pct"],
    marker=dict(color=colores),
    text=[f"{v:.1f}%" for v in resultado["Contribucion_pct"]],
    textposition="outside",
    textfont=dict(size=13),
))

fig.update_layout(
    height=500,
    width=700,
    plot_bgcolor="#E5ECF6",
    paper_bgcolor="white",
    title=dict(
        text="Descomposición de varianza — Ingreso Total",
        x=0.5,
        xanchor="center"
    ),
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=11),
        showgrid=True,
        gridcolor="white",
    ),
    yaxis=dict(
    title=dict(
        text="Contribución a Varianza (Y)",
        font=dict(size=12)  
    ),
    ticksuffix="%",
    range=[0, resultado["Contribucion_pct"].max() * 1.2],
    showgrid=True,
    gridcolor="white",
    ))


fig.show()