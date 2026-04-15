import streamlit as st
import pandas as pd
import numpy as np
from funciones_KPI import preparar_y_agrupar_ingresos, preparar_y_agrupar, calcular_kpi, dual_subplot, single_plot

st.set_page_config(layout="wide", page_title="Dashboard Macrobus", initial_sidebar_state="expanded")

# Título
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h1 style='color: #4A148C; font-size: 2.5rem; margin-bottom: 0.5rem;'>Dashboard de KPIs</h1>
    <p style='color: #6A1B9A; font-size: 1rem;'>Macrobus | Troncal - Alimentadoras</p>
    <div style='width: 100px; height: 3px; background: linear-gradient(90deg, #6A1B9A, #CE93D8); margin: 0 auto;'></div>
</div>
""", unsafe_allow_html=True)

# CSS
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #F3E5F5 100%);
        border-radius: 1.2rem; padding: 1.5rem 1.2rem; margin-bottom: 1rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05); border: 1px solid rgba(106,27,154,0.1);
        transition: all 0.3s ease; position: relative; overflow: hidden;
    }

    .kpi-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #6A1B9A, #9C27B0);
    }
    .kpi-card:hover { transform: translateY(-4px); box-shadow: 0 12px 28px rgba(106,27,154,0.15); }
    .kpi-label { font-size: 0.75rem; font-weight: 700; color: #7B1FA2; text-transform: uppercase; margin-bottom: 0.75rem; }
    .kpi-value {
        font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #4A148C 0%, #6A1B9A 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .kpi-unit { font-size: 0.75rem; color: #8E24AA; border-top: 1px solid #E1BEE7; padding-top: 0.5rem; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #4A3776 0%, #311B92 100%); }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stFileUploader label { color: #E1BEE7 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #ffffff !important; }
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #ffffff 0%, #F3E5F5 100%);
        border-radius: 0.75rem; padding: 0.75rem 1.5rem; font-weight: 600;
        color: #6A1B9A; border: 1px solid #E1BEE7;
    }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #6A1B9A 0%, #4A148C 100%) !important; color: white !important; }
    .stSubheader { color: #4A148C !important; border-bottom: 2px solid #E1BEE7 !important; }
    .custom-hr { margin: 2rem 0; background: linear-gradient(90deg, transparent, #CE93D8 20%, #CE93D8 80%, transparent); height: 1px; }
    .stAlert { border-left: 4px solid #6A1B9A; background-color: #F3E5F5; }
    .stPlotlyChart { background-color: white !important; border-radius: 1rem !important; padding: 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<div style='text-align: center; margin-bottom: 2rem;'><div style='font-size: 2.5rem;'></div><h2 style='color: white;'>LOGO MACROBUS</h2><p style='color: #E1BEE7;'>Troncal - Alimentadoras</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Carga de Archivos")
    file_alimentadoras = st.file_uploader("Ingresos Alimentadoras", type=["csv"])
    file_troncal = st.file_uploader("Ingresos Troncal", type=["csv"])
    file_km = st.file_uploader("Kilómetros", type=["csv"])
    file_costos = st.file_uploader("Gastos", type=["csv"])
    file_utilidad = st.file_uploader("Utilidad Mensual", type=["csv"])

# Funciones
def filtrar_kpi(df, periodos):
    if not periodos:
        return df
    return df[df["Periodo"].astype(str).isin([str(p) for p in periodos])]

def filtrar_por_años(df, años):
    if not años:
        return df
    años_str = [str(a) for a in años]
    return df[df["Periodo"].astype(str).str[:4].isin(años_str)]

# Procesamiento
if file_alimentadoras and file_troncal and file_km and file_costos and file_utilidad:
    
    # Ingresos
    data_alimentadoras = pd.read_csv(file_alimentadoras)
    cols_sum = ['Efectivo', 'Tarifa Incompleta', 'Monto Tarjeta Gral', 'Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error']
    data_alimentadoras['Ingreso_Total'] = data_alimentadoras[cols_sum].sum(axis=1)

    data_troncal = pd.read_csv(file_troncal)
    data_troncal['Ingreso_Total'] = data_troncal[cols_sum[:1] + cols_sum[2:6]].sum(axis=1)
    
    # Kilómetros
    data_km = pd.read_csv(file_km)
    data_km['Unidad'] = data_km['Unidad'].replace(r'^\s*$', np.nan, regex=True)
    data_km = data_km.dropna(subset=['Unidad'])
    data_km_alimentadoras = data_km[data_km['Unidad'].str.startswith('AM', na=False)]
    data_km_troncal = data_km[data_km['Unidad'].str.startswith('TM', na=False)]
    
    # Costos
    data_costos = pd.read_csv(file_costos)
    data_costos['Fecha'] = pd.to_datetime(data_costos['Fecha'], format='mixed', dayfirst=True)
    data_costos['Costos Operativos'] = data_costos[['Costo de Venta (Refacciones)', 'Gastos de Operación', 'Gastos de Mantenimiento']].sum(axis=1)
    data_costos_operativos = data_costos[['Fecha', 'Costos Operativos']].copy()
    data_costos_operativos['Costos OP Alimentadoras'] = data_costos_operativos['Costos Operativos'] * (81/155)
    data_costos_operativos['Costos OP Troncal'] = data_costos_operativos['Costos Operativos'] * (74/155)
    
    # Utilidad
    data_utilidad = pd.read_csv(file_utilidad)
    data_utilidad['Periodo'] = pd.to_datetime(data_utilidad['Periodo']).dt.to_period('M')
    
    # Agrupaciones
    # Ingresos
    ingresos_anual_alimentadoras = preparar_y_agrupar_ingresos(data_alimentadoras, 'Fecha', 'Ingreso_Total', 'anual').iloc[:-1]
    ingresos_mensual_alimentadoras = preparar_y_agrupar_ingresos(data_alimentadoras, 'Fecha', 'Ingreso_Total', 'mensual').iloc[:-2]
    ingresos_anual_troncal = preparar_y_agrupar_ingresos(data_troncal, 'Fecha', 'Ingreso_Total', 'anual').iloc[:-1]
    ingresos_mensual_troncal = preparar_y_agrupar_ingresos(data_troncal, 'Fecha', 'Ingreso_Total', 'mensual').iloc[:-2]
    
    # Kilómetros Reales
    km_real_anual_alimentadoras = preparar_y_agrupar(data_km_alimentadoras, 'Fecha', 'Km Realizados', 'anual')
    km_real_anual_troncal = preparar_y_agrupar(data_km_troncal, 'Fecha', 'Km Realizados', 'anual')
    km_real_mensual_alimentadoras = preparar_y_agrupar(data_km_alimentadoras, 'Fecha', 'Km Realizados', 'mensual')
    km_real_mensual_troncal = preparar_y_agrupar(data_km_troncal, 'Fecha', 'Km Realizados', 'mensual')
    
    # Kilómetros Programados
    km_prog_anual_alimentadoras = preparar_y_agrupar(data_km_alimentadoras, 'Fecha', 'Km Programados', 'anual')
    km_prog_anual_troncal = preparar_y_agrupar(data_km_troncal, 'Fecha', 'Km Programados', 'anual')
    km_prog_mensual_alimentadoras = preparar_y_agrupar(data_km_alimentadoras, 'Fecha', 'Km Programados', 'mensual')
    km_prog_mensual_troncal = preparar_y_agrupar(data_km_troncal, 'Fecha', 'Km Programados', 'mensual')
    
    # Costos
    costos_anual_alimentadoras = preparar_y_agrupar(data_costos_operativos, 'Fecha', 'Costos OP Alimentadoras', 'anual')
    costos_anual_troncal = preparar_y_agrupar(data_costos_operativos, 'Fecha', 'Costos OP Troncal', 'anual')
    costos_mensual_alimentadoras = preparar_y_agrupar(data_costos_operativos, 'Fecha', 'Costos OP Alimentadoras', 'mensual')
    costos_mensual_troncal = preparar_y_agrupar(data_costos_operativos, 'Fecha', 'Costos OP Troncal', 'mensual')
    
    # KPIs
    # Troncal - Anual - Reales
    KPI_INGRESO_KM_REAL_ANUAL_TRONCAL = calcular_kpi(ingresos_anual_troncal, km_real_anual_troncal, 'Ingreso_Total', 'Km Realizados', 'Ingreso')
    KPI_COSTO_KM_REAL_ANUAL_TRONCAL = calcular_kpi(costos_anual_troncal, km_real_anual_troncal, 'Costos OP Troncal', 'Km Realizados', 'Costo')
    
    # Troncal - Anual - Programados
    KPI_INGRESO_KM_PROG_ANUAL_TRONCAL = calcular_kpi(ingresos_anual_troncal, km_prog_anual_troncal, 'Ingreso_Total', 'Km Programados', 'Ingreso')
    KPI_COSTO_KM_PROG_ANUAL_TRONCAL = calcular_kpi(costos_anual_troncal, km_prog_anual_troncal, 'Costos OP Troncal', 'Km Programados', 'Costo')
    
    # Alimentadoras - Anual - Reales
    KPI_INGRESO_KM_REAL_ANUAL_ALIMENTADORAS = calcular_kpi(ingresos_anual_alimentadoras, km_real_anual_alimentadoras, 'Ingreso_Total', 'Km Realizados', 'Ingreso')
    KPI_COSTO_KM_REAL_ANUAL_ALIMENTADORAS = calcular_kpi(costos_anual_alimentadoras, km_real_anual_alimentadoras, 'Costos OP Alimentadoras', 'Km Realizados', 'Costo')
    
    # Alimentadoras - Anual - Programados
    KPI_INGRESO_KM_PROG_ANUAL_ALIMENTADORAS = calcular_kpi(ingresos_anual_alimentadoras, km_prog_anual_alimentadoras, 'Ingreso_Total', 'Km Programados', 'Ingreso')
    KPI_COSTO_KM_PROG_ANUAL_ALIMENTADORAS = calcular_kpi(costos_anual_alimentadoras, km_prog_anual_alimentadoras, 'Costos OP Alimentadoras', 'Km Programados', 'Costo')
    
    # Troncal - Mensual - Reales
    KPI_INGRESO_KM_REAL_MENSUAL_TRONCAL = calcular_kpi(ingresos_mensual_troncal, km_real_mensual_troncal, 'Ingreso_Total', 'Km Realizados', 'Ingreso')
    KPI_COSTO_KM_REAL_MENSUAL_TRONCAL = calcular_kpi(costos_mensual_troncal, km_real_mensual_troncal, 'Costos OP Troncal', 'Km Realizados', 'Costo')
    
    # Troncal - Mensual - Programados
    KPI_INGRESO_KM_PROG_MENSUAL_TRONCAL = calcular_kpi(ingresos_mensual_troncal, km_prog_mensual_troncal, 'Ingreso_Total', 'Km Programados', 'Ingreso')
    KPI_COSTO_KM_PROG_MENSUAL_TRONCAL = calcular_kpi(costos_mensual_troncal, km_prog_mensual_troncal, 'Costos OP Troncal', 'Km Programados', 'Costo')
    
    # Alimentadoras - Mensual - Reales
    KPI_INGRESO_KM_REAL_MENSUAL_ALIMENTADORAS = calcular_kpi(ingresos_mensual_alimentadoras, km_real_mensual_alimentadoras, 'Ingreso_Total', 'Km Realizados', 'Ingreso')
    KPI_COSTO_KM_REAL_MENSUAL_ALIMENTADORAS = calcular_kpi(costos_mensual_alimentadoras, km_real_mensual_alimentadoras, 'Costos OP Alimentadoras', 'Km Realizados', 'Costo')
    
    # Alimentadoras - Mensual - Programados
    KPI_INGRESO_KM_PROG_MENSUAL_ALIMENTADORAS = calcular_kpi(ingresos_mensual_alimentadoras, km_prog_mensual_alimentadoras, 'Ingreso_Total', 'Km Programados', 'Ingreso')
    KPI_COSTO_KM_PROG_MENSUAL_ALIMENTADORAS = calcular_kpi(costos_mensual_alimentadoras, km_prog_mensual_alimentadoras, 'Costos OP Alimentadoras', 'Km Programados', 'Costo')
    
    # Utilidad
    KPI_UTILIDAD_KM_PROG_MENSUAL_ALIMENTADORAS = calcular_kpi(data_utilidad, km_prog_mensual_alimentadoras, 'Utilidad AM', 'Km Programados', 'Utilidad')
    KPI_UTILIDAD_KM_PROG_MENSUAL_TRONCAL = calcular_kpi(data_utilidad, km_prog_mensual_troncal, 'Utilidad TR', 'Km Programados', 'Utilidad')
    
    # Pestañas
    tab1, tab2, tab3 = st.tabs(["KPIs Principales", "Sistema Troncal", "Sistema Alimentadoras"])
    
    with tab1:
        st.markdown("### Indicadores Anuales")
        col1, col2, col3, col4 = st.columns(4)
        
        ultimo_ingreso_tr = KPI_INGRESO_KM_REAL_ANUAL_TRONCAL['Ingreso'].iloc[-1] if not KPI_INGRESO_KM_REAL_ANUAL_TRONCAL.empty else 0
        ultimo_costo_tr = KPI_COSTO_KM_REAL_ANUAL_TRONCAL['Costo'].iloc[-1] if not KPI_COSTO_KM_REAL_ANUAL_TRONCAL.empty else 0
        ultimo_ingreso_am = KPI_INGRESO_KM_REAL_ANUAL_ALIMENTADORAS['Ingreso'].iloc[-1] if not KPI_INGRESO_KM_REAL_ANUAL_ALIMENTADORAS.empty else 0
        ultimo_costo_am = KPI_COSTO_KM_REAL_ANUAL_ALIMENTADORAS['Costo'].iloc[-1] if not KPI_COSTO_KM_REAL_ANUAL_ALIMENTADORAS.empty else 0
        ultimo_year_tr = KPI_INGRESO_KM_REAL_ANUAL_TRONCAL['Periodo'].iloc[-1] if not KPI_INGRESO_KM_REAL_ANUAL_TRONCAL.empty else "N/D"
        ultimo_year_am = KPI_INGRESO_KM_REAL_ANUAL_ALIMENTADORAS['Periodo'].iloc[-1] if not KPI_INGRESO_KM_REAL_ANUAL_ALIMENTADORAS.empty else "N/D"
        
        with col1:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Ingreso por KM Realizado</div><div class='kpi-value'>${ultimo_ingreso_tr:.2f}</div><div class='kpi-unit'>TRONCAL | AÑO: {ultimo_year_tr}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Costo Operativo por KM Realizado</div><div class='kpi-value'>${ultimo_costo_tr:.2f}</div><div class='kpi-unit'>TRONCAL | AÑO: {ultimo_year_tr}</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Ingreso por KM Realizado</div><div class='kpi-value'>${ultimo_ingreso_am:.2f}</div><div class='kpi-unit'>ALIMENTADORAS | AÑO: {ultimo_year_am}</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Costo Operativo por KM Realizado</div><div class='kpi-value'>${ultimo_costo_am:.2f}</div><div class='kpi-unit'>ALIMENTADORAS | AÑO: {ultimo_year_am}</div></div>", unsafe_allow_html=True)
            
        st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
        
        st.markdown("### Indicadores Mensuales")
        mes_ingreso_tr = KPI_INGRESO_KM_REAL_MENSUAL_TRONCAL['Ingreso'].iloc[-1] if not KPI_INGRESO_KM_REAL_MENSUAL_TRONCAL.empty else 0
        mes_costo_tr = KPI_COSTO_KM_REAL_MENSUAL_TRONCAL['Costo'].iloc[-1] if not KPI_COSTO_KM_REAL_MENSUAL_TRONCAL.empty else 0
        mes_ingreso_am = KPI_INGRESO_KM_REAL_MENSUAL_ALIMENTADORAS['Ingreso'].iloc[-1] if not KPI_INGRESO_KM_REAL_MENSUAL_ALIMENTADORAS.empty else 0
        mes_costo_am = KPI_COSTO_KM_REAL_MENSUAL_ALIMENTADORAS['Costo'].iloc[-1] if not KPI_COSTO_KM_REAL_MENSUAL_ALIMENTADORAS.empty else 0
        ultimo_periodo = KPI_INGRESO_KM_REAL_MENSUAL_TRONCAL['Periodo'].iloc[-1] if not KPI_INGRESO_KM_REAL_MENSUAL_TRONCAL.empty else "N/D"
        
        
        col1m, col2m, col3m, col4m = st.columns(4)
        with col1m:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Ingreso por KM Realizado</div><div class='kpi-value'>${mes_ingreso_tr:.2f}</div><div class='kpi-unit'>TRONCAL | PERIODO: {ultimo_periodo}</div></div>", unsafe_allow_html=True)
        with col2m:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Costo Operativo por KM Realizado</div><div class='kpi-value'>${mes_costo_tr:.2f}</div><div class='kpi-unit'>TRONCAL | PERIODO: {ultimo_periodo}</div></div>", unsafe_allow_html=True)
        with col3m:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Ingreso por KM Realizado</div><div class='kpi-value'>${mes_ingreso_am:.2f}</div><div class='kpi-unit'>ALIMENTADORAS | PERIODO: {ultimo_periodo}</div></div>", unsafe_allow_html=True)
        with col4m:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Costo Operativo por KM Realizado</div><div class='kpi-value'>${mes_costo_am:.2f}</div><div class='kpi-unit'>ALIMENTADORAS | PERIODO: {ultimo_periodo}</div></div>", unsafe_allow_html=True)
    
    
    with tab2:
        st.markdown("### Análisis Troncal")
        
        st.subheader("Evolución Anual")
        años = sorted(KPI_INGRESO_KM_REAL_ANUAL_TRONCAL['Periodo'].astype(str).unique())
        años_sel = st.multiselect("Seleccionar años", años, default=años, key="filtro_tr_anual")
        
        d_ingreso_real = filtrar_kpi(KPI_INGRESO_KM_REAL_ANUAL_TRONCAL, años_sel)
        d_costo_real = filtrar_kpi(KPI_COSTO_KM_REAL_ANUAL_TRONCAL, años_sel)
        d_ingreso_prog = filtrar_kpi(KPI_INGRESO_KM_PROG_ANUAL_TRONCAL, años_sel)
        d_costo_prog = filtrar_kpi(KPI_COSTO_KM_PROG_ANUAL_TRONCAL, años_sel)
        
        fig = dual_subplot(d_ingreso_real['Ingreso'], d_costo_real['Costo'], d_ingreso_prog['Ingreso'], d_costo_prog['Costo'],
                          d_ingreso_real['Periodo'], 'Año', 'Monto por KM', 10,
                          'Ingreso vs Costo (Real)', 'Ingreso vs Costo (Programado)',
                          'Ingresos', 'Costos', 'Ingresos', 'Costos')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
        
        st.subheader("Evolución Mensual")
        años_mensuales = sorted(set(KPI_INGRESO_KM_REAL_MENSUAL_TRONCAL['Periodo'].astype(str).str[:4]))
        años_sel_mensual = st.multiselect("Seleccionar años", años_mensuales, default=años_mensuales, key="filtro_tr_mensual")
        
        d_ingreso_real_m = filtrar_por_años(KPI_INGRESO_KM_REAL_MENSUAL_TRONCAL, años_sel_mensual)
        d_costo_real_m = filtrar_por_años(KPI_COSTO_KM_REAL_MENSUAL_TRONCAL, años_sel_mensual)
        d_ingreso_prog_m = filtrar_por_años(KPI_INGRESO_KM_PROG_MENSUAL_TRONCAL, años_sel_mensual)
        d_costo_prog_m = filtrar_por_años(KPI_COSTO_KM_PROG_MENSUAL_TRONCAL, años_sel_mensual)
        
        if not d_ingreso_real_m.empty:
            fig = dual_subplot(d_ingreso_real_m['Ingreso'], d_costo_real_m['Costo'], d_ingreso_prog_m['Ingreso'], d_costo_prog_m['Costo'],
                              d_ingreso_real_m['Periodo'], 'Mes', 'Monto por KM', 7,
                              'Ingreso vs Costo (Real)', 'Ingreso vs Costo (Programado)',
                              'Ingresos', 'Costos', 'Ingresos', 'Costos')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
        
        st.subheader("Utilidad por Km Programado")
        años_util = sorted(set(KPI_UTILIDAD_KM_PROG_MENSUAL_TRONCAL['Periodo'].astype(str).str[:4]))
        años_sel_util = st.multiselect("Seleccionar años", años_util, default=años_util, key="filtro_util_tr")
        
        d_utilidad_tr = filtrar_por_años(KPI_UTILIDAD_KM_PROG_MENSUAL_TRONCAL, años_sel_util)
        d_utilidad_am = filtrar_por_años(KPI_UTILIDAD_KM_PROG_MENSUAL_ALIMENTADORAS, años_sel_util)
        
        if not d_utilidad_tr.empty:
            fig = single_plot(d_utilidad_am['Utilidad'], d_utilidad_tr['Utilidad'], d_utilidad_tr['Periodo'],
                             'Mes', 'Utilidad por Km Programado', 10,
                             'Utilidad por Km Programado Mensual - Troncal',
                             'Alimentadoras', 'Troncal')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Análisis Alimentadoras")
        
        st.subheader("Evolución Anual")
        años = sorted(KPI_INGRESO_KM_REAL_ANUAL_ALIMENTADORAS['Periodo'].astype(str).unique())
        años_sel = st.multiselect("Seleccionar años", años, default=años, key="filtro_am_anual")
        
        d_ingreso_real = filtrar_kpi(KPI_INGRESO_KM_REAL_ANUAL_ALIMENTADORAS, años_sel)
        d_costo_real = filtrar_kpi(KPI_COSTO_KM_REAL_ANUAL_ALIMENTADORAS, años_sel)
        d_ingreso_prog = filtrar_kpi(KPI_INGRESO_KM_PROG_ANUAL_ALIMENTADORAS, años_sel)
        d_costo_prog = filtrar_kpi(KPI_COSTO_KM_PROG_ANUAL_ALIMENTADORAS, años_sel)
        
        fig = dual_subplot(d_ingreso_real['Ingreso'], d_costo_real['Costo'], d_ingreso_prog['Ingreso'], d_costo_prog['Costo'],
                          d_ingreso_real['Periodo'], 'Año', 'Monto por KM', 10,
                          'Ingreso vs Costo (Real)', 'Ingreso vs Costo (Programado)',
                          'Ingresos', 'Costos', 'Ingresos', 'Costos')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
        
        st.subheader("Evolución Mensual")
        años_mensuales = sorted(set(KPI_INGRESO_KM_REAL_MENSUAL_ALIMENTADORAS['Periodo'].astype(str).str[:4]))
        años_sel_mensual = st.multiselect("Seleccionar años", años_mensuales, default=años_mensuales, key="filtro_am_mensual")
        
        d_ingreso_real_m = filtrar_por_años(KPI_INGRESO_KM_REAL_MENSUAL_ALIMENTADORAS, años_sel_mensual)
        d_costo_real_m = filtrar_por_años(KPI_COSTO_KM_REAL_MENSUAL_ALIMENTADORAS, años_sel_mensual)
        d_ingreso_prog_m = filtrar_por_años(KPI_INGRESO_KM_PROG_MENSUAL_ALIMENTADORAS, años_sel_mensual)
        d_costo_prog_m = filtrar_por_años(KPI_COSTO_KM_PROG_MENSUAL_ALIMENTADORAS, años_sel_mensual)
        
        if not d_ingreso_real_m.empty:
            fig = dual_subplot(d_ingreso_real_m['Ingreso'], d_costo_real_m['Costo'], d_ingreso_prog_m['Ingreso'], d_costo_prog_m['Costo'],
                              d_ingreso_real_m['Periodo'], 'Mes', 'Monto por KM', 3,
                              'Ingreso vs Costo (Real)', 'Ingreso vs Costo (Programado)',
                              'Ingresos', 'Costos', 'Ingresos', 'Costos')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
        
        st.subheader("Utilidad por Km Programado")
        años_util = sorted(set(KPI_UTILIDAD_KM_PROG_MENSUAL_ALIMENTADORAS['Periodo'].astype(str).str[:4]))
        años_sel_util = st.multiselect("Seleccionar años", años_util, default=años_util, key="filtro_util_am")
        
        d_utilidad_am = filtrar_por_años(KPI_UTILIDAD_KM_PROG_MENSUAL_ALIMENTADORAS, años_sel_util)
        d_utilidad_tr = filtrar_por_años(KPI_UTILIDAD_KM_PROG_MENSUAL_TRONCAL, años_sel_util)
        
        if not d_utilidad_am.empty:
            fig = single_plot(d_utilidad_am['Utilidad'], d_utilidad_tr['Utilidad'], d_utilidad_am['Periodo'],
                             'Mes', 'Utilidad por Km Programado', 10,
                             'Utilidad por Km Programado Mensual - Alimentadoras',
                             'Alimentadoras', 'Troncal')
            st.plotly_chart(fig, use_container_width=True)

else:
    st.markdown("""
    <div style='margin-top: 3rem; text-align: center;'>
        <div style='display: inline-block; background: white; border-radius: 1.5rem; padding: 3rem 4rem; max-width: 650px; width: 100%; box-shadow: 0 20px 40px rgba(106,27,154,0.1); border: 1px solid #E1BEE7;'>
            <h2 style='color: #4A148C; margin-bottom: 0.5rem; font-weight: 600;'>Dashboard de KPIs</h2>
            <p style='color: #6A1B9A; margin-bottom: 2rem; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px;'>Macrobus</p>
            <div style='background: linear-gradient(90deg, #6A1B9A, #CE93D8); height: 2px; width: 60px; margin: 0 auto 2rem auto;'></div>
            <p style='color: #4A148C; margin-bottom: 1.5rem; font-weight: 500;'>Carga los archivos CSV para visualizar los indicadores</p>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; text-align: left; margin-bottom: 1.5rem;'>
                <div style='background: #F8F5FA; padding: 0.75rem 1rem; border-radius: 0.5rem; border-left: 3px solid #6A1B9A;'><span style='font-weight: 700; color: #4A148C;'>Ingresos</span><br><span style='font-size: 0.8rem; color: #7B1FA2;'>Alimentadoras</span></div>
                <div style='background: #F8F5FA; padding: 0.75rem 1rem; border-radius: 0.5rem; border-left: 3px solid #6A1B9A;'><span style='font-weight: 700; color: #4A148C;'>Ingresos</span><br><span style='font-size: 0.8rem; color: #7B1FA2;'>Troncal</span></div>
                <div style='background: #F8F5FA; padding: 0.75rem 1rem; border-radius: 0.5rem; border-left: 3px solid #6A1B9A;'><span style='font-weight: 700; color: #4A148C;'>Kilómetros</span><br><span style='font-size: 0.8rem; color: #7B1FA2;'>Realizados y Programados</span></div>
                <div style='background: #F8F5FA; padding: 0.75rem 1rem; border-radius: 0.5rem; border-left: 3px solid #6A1B9A;'><span style='font-weight: 700; color: #4A148C;'>Gastos</span><br><span style='font-size: 0.8rem; color: #7B1FA2;'>Costos Operativos</span></div>
                <div style='background: #F8F5FA; padding: 0.75rem 1rem; border-radius: 0.5rem; border-left: 3px solid #6A1B9A; grid-column: span 2;'><span style='font-weight: 700; color: #4A148C;'>Utilidad Mensual</span><br><span style='font-size: 0.8rem; color: #7B1FA2;'>Por sistema</span></div>
            </div>
    </div>
    """, unsafe_allow_html=True)