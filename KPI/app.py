import streamlit as st
import pandas as pd
import numpy as np
from funciones_KPI import preparar_y_agrupar_ingresos, preparar_y_agrupar, calcular_kpi, dual_subplot, single_plot

st.set_page_config(layout="wide", page_title="Dashboard Macrobus", initial_sidebar_state="expanded")

st._config.set_option('theme.primaryColor', '#7B52B8')
st._config.set_option('theme.backgroundColor', '#ffffff')
st._config.set_option('theme.textColor', '#2E1F5E')

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div class='dash-title' style='text-align: center; margin-bottom: 1rem;'>
            <h1 style='color: #4A148C; font-size: 3.5rem; margin-bottom: 0.25rem;'>Dashboard de KPI's</h1>
            <p style='color: #7B52B8; font-size: 2rem; font-weight: 700;'>Macrobus</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <div style='width: 100px; height: 3px; background-color: #7B52B8; margin: 0 auto;'></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #EDE7F6 100%);
        border-radius: 1.2rem; padding: 1.5rem 1.2rem; margin-bottom: 1rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05); border: 1px solid rgba(123,82,184,0.2);
        transition: all 0.3s ease; position: relative; overflow: hidden;
    }
    .kpi-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #7B52B8, #B48FD4);
    }
    .kpi-card:hover { transform: translateY(-4px); box-shadow: 0 12px 28px rgba(123,82,184,0.25); }
    .kpi-label { font-size: 0.75rem; font-weight: 700; color: #7B52B8; text-transform: uppercase; margin-bottom: 0.75rem; }
    .kpi-value {
        font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #5E3D9C 0%, #8B62C4 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .kpi-unit { font-size: 0.75rem; color: #B48FD4; border-top: 1px solid #D9C2F0; padding-top: 0.5rem; }
    .trend-up { color: #4CAF50; font-size: 0.75rem; font-weight: 600; }
    .trend-down { color: #F44336; font-size: 0.75rem; font-weight: 600; }
    .trend-neutral { color: #FF9800; font-size: 0.75rem; font-weight: 600; }
    .trend-no-data { color: #9E9E9E; font-size: 0.75rem; font-weight: 600; }

    [data-testid="stSidebar"] { background-color: #4A3776; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stFileUploader label { color: #C9B8E8 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #ffffff !important; }
    [data-testid="stSidebar"] .stMarkdown h3 { color: #ffffff !important; }
    [data-testid="stSidebar"] details {
        background: rgba(255,255,255,0.08);
        border-radius: 0.75rem;
        border: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 0.75rem;
    }
    [data-testid="stSidebar"] details summary {
        background: rgba(255,255,255,0.05);
        border-radius: 0.75rem;
        padding: 0.5rem 0.75rem;
        font-weight: 600;
        color: #C9B8E8;
    }
    [data-testid="stSidebar"] details summary:hover { background: rgba(255,255,255,0.1); }
    [data-testid="stSidebar"] .streamlit-expanderContent { padding: 0.75rem; color: #C9B8E8; }
    [data-testid="stSidebar"] .stFileUploader {
        background: rgba(255,255,255,0.05);
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin-top: 0.5rem;
    }
    [data-testid="stSidebar"] .stFileUploader label { color: #C9B8E8 !important; font-weight: 500; }
    [data-testid="stSidebar"] .stFileUploader div[data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] .stFileUploader div[data-baseweb="notification"],
    [data-testid="stSidebar"] .stFileUploader .e1ewe7hr3,
    [data-testid="stSidebar"] .stFileUploader .e1b2p2ww5,
    [data-testid="stSidebar"] .stFileUploader .uploadedFileName,
    [data-testid="stSidebar"] .stFileUploader [data-testid="stFileUploaderFile"],
    [data-testid="stSidebar"] .stFileUploader [data-testid="stFileUploaderDeleteBtn"],
    [data-testid="stSidebar"] .stFileUploader small,
    [data-testid="stSidebar"] .stFileUploader [class*="uploadedFile"],
    [data-testid="stSidebar"] .stFileUploader > div > div:last-child > div {
        display: none !important;
    }
    .custom-file-display {
        background: rgba(255,255,255,0.15);
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin-top: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .custom-file-name { color: white; font-size: 0.8rem; display: flex; align-items: center; gap: 0.5rem; }
    .kpi-card-utilidad-positive {
        background: linear-gradient(135deg, #E8F5E9 0%, #A5D6A7 100%);
        border: 1px solid #66BB6A;
    }
    .kpi-card-utilidad-positive::before { background: linear-gradient(90deg, #2E7D32, #81C784); }
    .kpi-card-utilidad-positive .kpi-value {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .kpi-card-utilidad-positive .kpi-label { color: #1B5E20; }
    .kpi-card-utilidad-positive .kpi-unit { color: #2E7D32; border-top-color: #81C784; }
    .kpi-card-utilidad-negative {
        background: linear-gradient(135deg, #FFEBEE 0%, #EF9A9A 100%);
        border: 1px solid #EF5350;
    }
    .kpi-card-utilidad-negative::before { background: linear-gradient(90deg, #C62828, #EF5350); }
    .kpi-card-utilidad-negative .kpi-value {
        background: linear-gradient(135deg, #B71C1C 0%, #C62828 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .kpi-card-utilidad-negative .kpi-label { color: #C62828; }
    .kpi-card-utilidad-negative .kpi-unit { color: #C62828; border-top-color: #EF9A9A; }
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #ffffff 0%, #EDE7F6 100%);
        border-radius: 0.75rem; padding: 0.75rem 1.5rem; font-weight: 600;
        color: #7B52B8; border: 1px solid #D9C2F0;
    }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #7B52B8 0%, #5E3D9C 100%) !important; color: white !important; }
    .stMarkdown h3 { color: #7B52B8 !important; font-weight: 600; }
    .stSubheader { color: #7B52B8 !important; border-bottom: 2px solid #D9C2F0 !important; }
    .custom-hr { margin: 2rem 0; background: linear-gradient(90deg, transparent, #B48FD4 20%, #B48FD4 80%, transparent); height: 1px; }
    .stPlotlyChart { background-color: white !important; border-radius: 1rem !important; padding: 0.5rem !important; }

    .stTabs [data-baseweb="tab-highlight"] { background-color: #7B52B8 !important; }
    .stTabs [data-baseweb="tab-border"] { background-color: #D9C2F0 !important; }
    .stSlider [data-baseweb="slider"] [role="slider"] { background-color: #7B52B8 !important; border-color: #7B52B8 !important; }
    .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] { color: #7B52B8 !important; }
    .stMultiSelect [data-baseweb="select"] span { background-color: #7B52B8 !important; color: white !important; }
    .stMultiSelect [data-baseweb="tag"] { background-color: #7B52B8 !important; }
    [data-baseweb="option"]:hover { background-color: #EDE7F6 !important; }
    :root { --primary-color: #7B52B8 !important; }

    @media (max-width: 768px) {
        .dash-title h1 { font-size: 2rem !important; }
        .dash-title p { font-size: 1.3rem !important; }
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            width: 100% !important;
            flex: 0 0 100% !important;
            min-width: 100% !important;
        }
        .kpi-value { font-size: 1.4rem !important; }
        .kpi-card { padding: 1rem 0.75rem !important; }
        .stTabs [data-baseweb="tab"] {
            padding: 0.4rem 0.5rem !important;
            font-size: 0.68rem !important;
        }
        .welcome-card { padding: 1.5rem 1.25rem !important; }
        .welcome-grid { grid-template-columns: 1fr !important; }
        .error-card { padding: 1.25rem !important; }
    }
</style>
""", unsafe_allow_html=True)

for key in ['file_alimentadoras', 'file_troncal', 'file_km', 'file_costos', 'file_utilidad']:
    if key not in st.session_state:
        st.session_state[key] = None

# Sidebar
with st.sidebar:
    st.image("KPI/logo_macro.png", use_container_width=True)

    st.markdown("""
        <div style='background: rgba(255,255,255,0.08); border-radius: 0.75rem; padding: 1.2rem; margin-bottom: 1rem;'>
            <p style='color: white; font-size: 1rem; line-height: 1.8; text-align: center; margin: 0 auto; font-weight: 700;'>Plataforma de monitoreo y análisis de indicadores financieros y operativos de Macrobus. Visualiza ingresos, costos y utilidades por kilómetro para los sistemas Troncal y Alimentadoras.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("# Carga de Archivos")
    
    # INGRESOS
    with st.expander("**INGRESOS**", expanded=False):
        st.markdown("**Alimentadoras**")
        file_alimentadoras = st.file_uploader("CSV Ingresos Alimentadoras", type=["csv"], key="upload_alimentadoras", label_visibility="collapsed")
        if file_alimentadoras:
            st.session_state.file_alimentadoras = file_alimentadoras
            st.markdown(f"<div class='custom-file-display'><div class='custom-file-name'>{file_alimentadoras.name}</div></div>", unsafe_allow_html=True)
        elif st.session_state.file_alimentadoras:
            st.markdown(f"<div class='custom-file-display'><div class='custom-file-name'>{st.session_state.file_alimentadoras.name}</div></div>", unsafe_allow_html=True)
        
        st.markdown("**Troncal**")
        file_troncal = st.file_uploader("CSV Ingresos Troncal", type=["csv"], key="upload_troncal", label_visibility="collapsed")
        if file_troncal:
            st.session_state.file_troncal = file_troncal
            st.markdown(f"<div class='custom-file-display'><div class='custom-file-name'>{file_troncal.name}</div></div>", unsafe_allow_html=True)
        elif st.session_state.file_troncal:
            st.markdown(f"<div class='custom-file-display'><div class='custom-file-name'>{st.session_state.file_troncal.name}</div></div>", unsafe_allow_html=True)
    
    # KILÓMETROS
    with st.expander("**KILÓMETROS**", expanded=False):
        st.markdown("**Km Realizados y Programados**")
        file_km = st.file_uploader("CSV Kilómetros", type=["csv"], key="upload_km", label_visibility="collapsed")
        if file_km:
            st.session_state.file_km = file_km
            st.markdown(f"<div class='custom-file-display'><div class='custom-file-name'>{file_km.name}</div></div>", unsafe_allow_html=True)
        elif st.session_state.file_km:
            st.markdown(f"<div class='custom-file-display'><div class='custom-file-name'>{st.session_state.file_km.name}</div></div>", unsafe_allow_html=True)
    
    # COSTOS
    with st.expander("**COSTOS**", expanded=False):
        st.markdown("**Costos Operativos**")
        file_costos = st.file_uploader("CSV Gastos", type=["csv"], key="upload_costos", label_visibility="collapsed")
        if file_costos:
            st.session_state.file_costos = file_costos
            st.markdown(f"<div class='custom-file-display'><div class='custom-file-name'>{file_costos.name}</div></div>", unsafe_allow_html=True)
        elif st.session_state.file_costos:
            st.markdown(f"<div class='custom-file-display'><div class='custom-file-name'>{st.session_state.file_costos.name}</div></div>", unsafe_allow_html=True)
    
    # UTILIDAD
    with st.expander("**UTILIDAD**", expanded=False):
        st.markdown("**Utilidad Mensual**")
        file_utilidad = st.file_uploader("CSV Utilidad", type=["csv"], key="upload_utilidad", label_visibility="collapsed")
        if file_utilidad:
            st.session_state.file_utilidad = file_utilidad
            st.markdown(f"<div class='custom-file-display'><div class='custom-file-name'>{file_utilidad.name}</div></div>", unsafe_allow_html=True)
        elif st.session_state.file_utilidad:
            st.markdown(f"<div class='custom-file-display'><div class='custom-file-name'>{st.session_state.file_utilidad.name}</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")

# Funciones
def formatear_periodo(periodo_str):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    try:
        año, mes = periodo_str.split('-')
        return f"{meses[int(mes)-1]} {año}"
    except:
        return periodo_str

def calcular_cambio(valor_actual, valor_anterior):
    if valor_anterior and valor_anterior != 0:
        return ((valor_actual - valor_anterior) / abs(valor_anterior)) * 100
    return None

def crear_tarjeta_kpi(titulo, valor, periodo, sistema, tipo_medida, cambio=None, es_utilidad=False, valor_utilidad=None):
    if es_utilidad and valor_utilidad is not None:
        clase_extra = "kpi-card-utilidad-positive" if valor_utilidad >= 0 else "kpi-card-utilidad-negative"
    else:
        clase_extra = ""

    if cambio is not None:
        simbolo = "▲" if cambio > 0 else "▼" if cambio < 0 else ""
        texto_tendencia = f"{simbolo} {'' if cambio>0 else ''}{cambio:.1f}%"
        tendencia_clase = "trend-up" if cambio > 0 else "trend-down" if cambio < 0 else "trend-neutral"
    else:
        texto_tendencia = "Sin datos previos"
        tendencia_clase = "trend-no-data"

    valor_formateado = f"${abs(valor):,.2f}"
    if es_utilidad and valor_utilidad is not None and valor_utilidad < 0:
        valor_formateado = f"-{valor_formateado}"
    
    return f"""
    <div class='kpi-card {clase_extra}'>
        <div class='kpi-label'>{titulo} | {sistema}</div>
        <div class='kpi-value'>{valor_formateado}</div>
        <div class='kpi-unit'>| {tipo_medida}: {periodo}</div>
        <div style='margin-top: 8px;'><span class='{tendencia_clase}'>vs período anterior: {texto_tendencia}</span></div>
    </div>
    """

def filtrar_por_rango(df, inicio, fin):
    if df.empty or not inicio or not fin:
        return df
    return df[df["Periodo"].astype(str).between(inicio, fin)]

archivos_cargados = all([st.session_state[f"file_{tipo}"] for tipo in ["alimentadoras", "troncal", "km", "costos", "utilidad"]])

if archivos_cargados:
    try:
        # Cargar y procesar datos
        data_alimentadoras = pd.read_csv(st.session_state.file_alimentadoras)
        data_troncal = pd.read_csv(st.session_state.file_troncal)
        data_km = pd.read_csv(st.session_state.file_km)
        data_costos = pd.read_csv(st.session_state.file_costos)
        data_utilidad = pd.read_csv(st.session_state.file_utilidad)
        
        # Columnas para ingresos
        cols_ingreso = ['Efectivo', 'Tarifa Incompleta', 'Monto Tarjeta Gral', 'Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error']
        data_alimentadoras['Ingreso_Total'] = data_alimentadoras[cols_ingreso].sum(axis=1)
        data_troncal['Ingreso_Total'] = data_troncal[cols_ingreso[:1] + cols_ingreso[2:6]].sum(axis=1)
        
        # Procesar kilómetros
        data_km = data_km.dropna(subset=['Unidad'])
        data_km_alimentadoras = data_km[data_km['Unidad'].str.startswith('AM', na=False)]
        data_km_troncal = data_km[data_km['Unidad'].str.startswith('TM', na=False)]
        
        # Procesar costos
        data_costos['Fecha'] = pd.to_datetime(data_costos['Fecha'], format='mixed', dayfirst=True)
        data_costos['Costos Operativos'] = data_costos[['Costo de Venta (Refacciones)', 'Gastos de Operación', 'Gastos de Mantenimiento']].sum(axis=1)
        data_costos_operativos = data_costos[['Fecha', 'Costos Operativos']].copy()
        data_costos_operativos['Costos OP Alimentadoras'] = data_costos_operativos['Costos Operativos'] * (81/155)
        data_costos_operativos['Costos OP Troncal'] = data_costos_operativos['Costos Operativos'] * (74/155)
        
        # Procesar utilidad
        data_utilidad['Periodo'] = pd.to_datetime(data_utilidad['Periodo']).dt.to_period('M')
        
        # Agrupar datos
        def agrupar_ingresos(df, frecuencia):
            return preparar_y_agrupar_ingresos(df, 'Fecha', 'Ingreso_Total', frecuencia).iloc[:-1 if frecuencia == 'anual' else -2]
        
        ingresos_anual_alimentadoras = agrupar_ingresos(data_alimentadoras, 'anual')
        ingresos_mensual_alimentadoras = agrupar_ingresos(data_alimentadoras, 'mensual')
        ingresos_anual_troncal = agrupar_ingresos(data_troncal, 'anual')
        ingresos_mensual_troncal = agrupar_ingresos(data_troncal, 'mensual')
        
        def agrupar(df, columna, frecuencia):
            return preparar_y_agrupar(df, 'Fecha', columna, frecuencia)
        
        km_real_anual_alimentadoras = agrupar(data_km_alimentadoras, 'Km Realizados', 'anual')
        km_real_mensual_alimentadoras = agrupar(data_km_alimentadoras, 'Km Realizados', 'mensual')
        km_real_anual_troncal = agrupar(data_km_troncal, 'Km Realizados', 'anual')
        km_real_mensual_troncal = agrupar(data_km_troncal, 'Km Realizados', 'mensual')
        
        km_prog_anual_alimentadoras = agrupar(data_km_alimentadoras, 'Km Programados', 'anual')
        km_prog_mensual_alimentadoras = agrupar(data_km_alimentadoras, 'Km Programados', 'mensual')
        km_prog_anual_troncal = agrupar(data_km_troncal, 'Km Programados', 'anual')
        km_prog_mensual_troncal = agrupar(data_km_troncal, 'Km Programados', 'mensual')
        
        costos_anual_alimentadoras = agrupar(data_costos_operativos, 'Costos OP Alimentadoras', 'anual')
        costos_mensual_alimentadoras = agrupar(data_costos_operativos, 'Costos OP Alimentadoras', 'mensual')
        costos_anual_troncal = agrupar(data_costos_operativos, 'Costos OP Troncal', 'anual')
        costos_mensual_troncal = agrupar(data_costos_operativos, 'Costos OP Troncal', 'mensual')
        
        # KPIs
        def calcular_kpis(ingresos, costos, km_real, km_prog, sistema):
            return {
                'ingreso_km_real': calcular_kpi(ingresos, km_real, 'Ingreso_Total', 'Km Realizados', 'Ingreso'),
                'costo_km_real': calcular_kpi(costos, km_real, f'Costos OP {sistema}', 'Km Realizados', 'Costo'),
                'ingreso_km_prog': calcular_kpi(ingresos, km_prog, 'Ingreso_Total', 'Km Programados', 'Ingreso'),
                'costo_km_prog': calcular_kpi(costos, km_prog, f'Costos OP {sistema}', 'Km Programados', 'Costo')
            }
        
        kpis_troncal = calcular_kpis(ingresos_anual_troncal, costos_anual_troncal, km_real_anual_troncal, km_prog_anual_troncal, 'Troncal')
        kpis_troncal_mensual = calcular_kpis(ingresos_mensual_troncal, costos_mensual_troncal, km_real_mensual_troncal, km_prog_mensual_troncal, 'Troncal')
        kpis_am = calcular_kpis(ingresos_anual_alimentadoras, costos_anual_alimentadoras, km_real_anual_alimentadoras, km_prog_anual_alimentadoras, 'Alimentadoras')
        kpis_am_mensual = calcular_kpis(ingresos_mensual_alimentadoras, costos_mensual_alimentadoras, km_real_mensual_alimentadoras, km_prog_mensual_alimentadoras, 'Alimentadoras')

        utilidad_tr = calcular_kpi(data_utilidad, km_prog_mensual_troncal, 'Utilidad TR', 'Km Programados', 'Utilidad')
        utilidad_am = calcular_kpi(data_utilidad, km_prog_mensual_alimentadoras, 'Utilidad AM', 'Km Programados', 'Utilidad')
        
        # Periodos
        periodos_tr = sorted(kpis_troncal_mensual['ingreso_km_real']['Periodo'].astype(str).unique())
        periodos_am = sorted(kpis_am_mensual['ingreso_km_real']['Periodo'].astype(str).unique())
        
        tab1, tab2, tab3, tab4 = st.tabs(["KPI's Principales", "Sistema Troncal", "Sistema Alimentadoras", "Comparación de Utilidades"])
        
        with tab1:
            st.markdown("### Indicadores de Utilidad Mensual")
            if not utilidad_tr.empty and not utilidad_am.empty:
                col1, col2 = st.columns(2)
                ult_periodo = utilidad_tr['Periodo'].iloc[-1]
                
                for col, df, nombre in [(col1, utilidad_tr, "TRONCAL"), (col2, utilidad_am, "ALIMENTADORAS")]:
                    ult_valor = df['Utilidad'].iloc[-1]
                    cambio = calcular_cambio(ult_valor, df['Utilidad'].iloc[-2] if len(df) > 1 else None)
                    col.markdown(crear_tarjeta_kpi("Utilidad por KM Programado", abs(ult_valor), str(ult_periodo), nombre, "PERIODO", cambio, True, ult_valor), unsafe_allow_html=True)
            
            st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
            st.markdown("### Indicadores Anuales")
            
            if not kpis_troncal['ingreso_km_real'].empty:
                cols = st.columns(4)
                ult_year = kpis_troncal['ingreso_km_real']['Periodo'].iloc[-1]
                
                datos = [
                    (kpis_troncal['ingreso_km_real']['Ingreso'].iloc[-1], kpis_troncal['ingreso_km_real']['Ingreso'].iloc[-2] if len(kpis_troncal['ingreso_km_real']) > 1 else None, "Ingreso por KM Realizado", "TRONCAL"),
                    (kpis_troncal['costo_km_real']['Costo'].iloc[-1], kpis_troncal['costo_km_real']['Costo'].iloc[-2] if len(kpis_troncal['costo_km_real']) > 1 else None, "Costo Operativo por KM Realizado", "TRONCAL"),
                    (kpis_am['ingreso_km_real']['Ingreso'].iloc[-1], kpis_am['ingreso_km_real']['Ingreso'].iloc[-2] if len(kpis_am['ingreso_km_real']) > 1 else None, "Ingreso por KM Realizado", "ALIMENTADORAS"),
                    (kpis_am['costo_km_real']['Costo'].iloc[-1], kpis_am['costo_km_real']['Costo'].iloc[-2] if len(kpis_am['costo_km_real']) > 1 else None, "Costo Operativo por KM Realizado", "ALIMENTADORAS")
                ]
                
                for col, (valor, anterior, titulo, sistema) in zip(cols, datos):
                    cambio = calcular_cambio(valor, anterior)
                    col.markdown(crear_tarjeta_kpi(titulo, valor, ult_year, sistema, "AÑO", cambio), unsafe_allow_html=True)
            
            st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
            st.markdown("### Indicadores Mensuales")
            
            if not kpis_troncal_mensual['ingreso_km_real'].empty:
                cols = st.columns(4)
                ult_periodo = kpis_troncal_mensual['ingreso_km_real']['Periodo'].iloc[-1]
                
                datos_mensuales = [
                    (kpis_troncal_mensual['ingreso_km_real']['Ingreso'].iloc[-1], kpis_troncal_mensual['ingreso_km_real']['Ingreso'].iloc[-2] if len(kpis_troncal_mensual['ingreso_km_real']) > 1 else None, "Ingreso por KM Realizado", "TRONCAL"),
                    (kpis_troncal_mensual['costo_km_real']['Costo'].iloc[-1], kpis_troncal_mensual['costo_km_real']['Costo'].iloc[-2] if len(kpis_troncal_mensual['costo_km_real']) > 1 else None, "Costo Operativo por KM Realizado", "TRONCAL"),
                    (kpis_am_mensual['ingreso_km_real']['Ingreso'].iloc[-1], kpis_am_mensual['ingreso_km_real']['Ingreso'].iloc[-2] if len(kpis_am_mensual['ingreso_km_real']) > 1 else None, "Ingreso por KM Realizado", "ALIMENTADORAS"),
                    (kpis_am_mensual['costo_km_real']['Costo'].iloc[-1], kpis_am_mensual['costo_km_real']['Costo'].iloc[-2] if len(kpis_am_mensual['costo_km_real']) > 1 else None, "Costo Operativo por KM Realizado", "ALIMENTADORAS")
                ]
                
                for col, (valor, anterior, titulo, sistema) in zip(cols, datos_mensuales):
                    cambio = calcular_cambio(valor, anterior)
                    col.markdown(crear_tarjeta_kpi(titulo, valor, str(ult_periodo), sistema, "PERIODO", cambio), unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### Análisis Troncal")
            st.markdown("###### Evolución Anual")
            años = sorted(kpis_troncal['ingreso_km_real']['Periodo'].astype(str).unique())
            años_sel = st.multiselect("Seleccionar años", años, default=años, key="filtro_tr_anual")
            
            def filtrar_kpis(kpis_dict, años_sel):
                return {k: v[v["Periodo"].astype(str).isin([str(a) for a in años_sel])] for k, v in kpis_dict.items()}
            
            kpis_tr_filtrados = filtrar_kpis(kpis_troncal, años_sel)
            
            fig = dual_subplot(
                kpis_tr_filtrados['ingreso_km_real']['Ingreso'], kpis_tr_filtrados['costo_km_real']['Costo'],
                kpis_tr_filtrados['ingreso_km_prog']['Ingreso'], kpis_tr_filtrados['costo_km_prog']['Costo'],
                kpis_tr_filtrados['ingreso_km_real']['Periodo'], 'Año', 'Monto por KM', 10,
                'Ingreso vs Costo Operativo por KM Realizado', 'Ingreso vs Costo Operativo por KM Programado',
                'Ingresos', 'Costos', 'Ingresos', 'Costos'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
            
            st.markdown("###### Evolución Mensual")
            if periodos_tr:
                opciones = {p: formatear_periodo(p) for p in periodos_tr}
                lista_opciones = list(opciones.values())
                seleccion = st.select_slider("Seleccionar rango de meses", options=lista_opciones, value=(lista_opciones[0], lista_opciones[-1]), key="rango_tr_mensual")
                
                idx_inicio, idx_fin = lista_opciones.index(seleccion[0]), lista_opciones.index(seleccion[1])
                periodo_inicio, periodo_fin = periodos_tr[idx_inicio], periodos_tr[idx_fin]
                
                datos_filtrados = {k: filtrar_por_rango(v, periodo_inicio, periodo_fin) for k, v in kpis_troncal_mensual.items()}
                
                if not datos_filtrados['ingreso_km_real'].empty:
                    fig = dual_subplot(
                        datos_filtrados['ingreso_km_real']['Ingreso'], datos_filtrados['costo_km_real']['Costo'],
                        datos_filtrados['ingreso_km_prog']['Ingreso'], datos_filtrados['costo_km_prog']['Costo'],
                        datos_filtrados['ingreso_km_real']['Periodo'], 'Mes', 'Monto por KM', 7,
                        'Ingreso vs Costo Operativo por KM Realizado', 'Ingreso vs Costo Operativo por KM Programado',
                        'Ingresos', 'Costos', 'Ingresos', 'Costos'
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown("### Análisis Alimentadoras")
            st.markdown("###### Evolución Anual")
            años = sorted(kpis_am['ingreso_km_real']['Periodo'].astype(str).unique())
            años_sel = st.multiselect("Seleccionar años", años, default=años, key="filtro_am_anual")
            
            kpis_am_filtrados = filtrar_kpis(kpis_am, años_sel)
            
            fig = dual_subplot(
                kpis_am_filtrados['ingreso_km_real']['Ingreso'], kpis_am_filtrados['costo_km_real']['Costo'],
                kpis_am_filtrados['ingreso_km_prog']['Ingreso'], kpis_am_filtrados['costo_km_prog']['Costo'],
                kpis_am_filtrados['ingreso_km_real']['Periodo'], 'Año', 'Monto por KM', 10,
                'Ingreso vs Costo Operativo por KM Realizado', 'Ingreso vs Costo Operativo por KM Programado',
                'Ingresos', 'Costos', 'Ingresos', 'Costos'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
            
            st.markdown("###### Evolución Mensual")
            if periodos_am:
                opciones = {p: formatear_periodo(p) for p in periodos_am}
                lista_opciones = list(opciones.values())
                seleccion = st.select_slider("Seleccionar rango de meses", options=lista_opciones, value=(lista_opciones[0], lista_opciones[-1]), key="rango_am_mensual")
                
                idx_inicio, idx_fin = lista_opciones.index(seleccion[0]), lista_opciones.index(seleccion[1])
                periodo_inicio, periodo_fin = periodos_am[idx_inicio], periodos_am[idx_fin]
                
                datos_filtrados = {k: filtrar_por_rango(v, periodo_inicio, periodo_fin) for k, v in kpis_am_mensual.items()}
                
                if not datos_filtrados['ingreso_km_real'].empty:
                    fig = dual_subplot(
                        datos_filtrados['ingreso_km_real']['Ingreso'], datos_filtrados['costo_km_real']['Costo'],
                        datos_filtrados['ingreso_km_prog']['Ingreso'], datos_filtrados['costo_km_prog']['Costo'],
                        datos_filtrados['ingreso_km_real']['Periodo'], 'Mes', 'Monto por KM', 3,
                        'Ingreso vs Costo Operativo por KM Realizado', 'Ingreso vs Costo Operativo por KM Programado',
                        'Ingresos', 'Costos', 'Ingresos', 'Costos'
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.markdown("### Comparación de Utilidades")
            periodos_utilidad = sorted(utilidad_tr['Periodo'].astype(str).unique())
            if periodos_utilidad:
                opciones = {p: formatear_periodo(p) for p in periodos_utilidad}
                lista_opciones = list(opciones.values())
                seleccion = st.select_slider("Seleccionar rango de meses", options=lista_opciones, value=(lista_opciones[0], lista_opciones[-1]), key="rango_utilidad")
                
                idx_inicio, idx_fin = lista_opciones.index(seleccion[0]), lista_opciones.index(seleccion[1])
                periodo_inicio, periodo_fin = periodos_utilidad[idx_inicio], periodos_utilidad[idx_fin]
                
                utilidad_combinada = pd.DataFrame({
                    'Periodo': utilidad_tr['Periodo'].astype(str),
                    'Troncal': utilidad_tr['Utilidad'],
                    'Alimentadoras': utilidad_am['Utilidad']
                })
                utilidad_filtrada = filtrar_por_rango(utilidad_combinada, periodo_inicio, periodo_fin)
                
                if not utilidad_filtrada.empty:
                    fig = single_plot(
                        utilidad_filtrada['Alimentadoras'], utilidad_filtrada['Troncal'],
                        utilidad_filtrada['Periodo'], 'Mes', 'Utilidad por KM Programado', 10,
                        'Comparación de Utilidades por KM Programado', 'Alimentadoras', 'Troncal'
                    )
                    st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.markdown("""
        <div style="margin-top: 2rem; text-align: center;">
            <div class="error-card" style="display: inline-block; background: #FFF5F5; border-radius: 1.5rem; padding: 2rem 3rem; max-width: 600px; width: 100%; border: 1px solid #F4C2C2;">
                <p style="color: #C62828; font-size: 1.7rem; font-weight: 700; margin-bottom: 0.75rem;">ERROR AL PROCESAR LOS ARCHIVOS</p>
                <p style="color: #7B1C1C; font-size: 1rem; font-weight: 700; line-height: 1.6; margin-bottom: 0.75rem;">Uno o más archivos no tienen el formato correcto. Por favor verifica que estás subiendo el archivo correspondiente a cada sección.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    archivos_cargados_count = sum([
        1 for key in ['file_alimentadoras', 'file_troncal', 'file_km', 'file_costos', 'file_utilidad']
        if st.session_state[key] is not None
    ])
    progreso = int(archivos_cargados_count / 5 * 100)

    barra = f"<div style=\"background: linear-gradient(90deg, #5E4B8A, #9C7FBF); height: 8px; border-radius: 1rem; width: {progreso}%;\"></div>"
    contador = f"<span style=\"font-size: 0.75rem; font-weight: 700; color: #5E4B8A;\">{archivos_cargados_count} / 5</span>"

    st.markdown("""
    <div style="margin-top: 3rem; text-align: center;">
        <div class="welcome-card" style="display: inline-block; background: white; border-radius: 1.5rem; padding: 3rem 4rem; max-width: 650px; width: 100%; box-shadow: 0 20px 40px rgba(94,75,138,0.1); border: 1px solid #D4C5ED;">
            <p style="color: #5E4B8A; margin-bottom: 1.5rem; font-weight: 700; font-size: 1.1rem;">Carga los archivos CSV para visualizar los indicadores</p>
            <div style="margin-bottom: 1.5rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="font-size: 0.75rem; font-weight: 700; color: #9C7FBF;">Archivos cargados</span>
                    """ + contador + """
                </div>
                <div style="background: #EDE7F6; border-radius: 1rem; height: 8px; width: 100%;">
                    """ + barra + """
                </div>
            </div>
            <div class="welcome-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; text-align: left; margin-bottom: 1.5rem;">
                <div style="background: #F5F0FA; padding: 0.75rem 1rem; border-radius: 0.5rem; border-left: 3px solid #5E4B8A;"><span style="font-weight: 700; color: #4A3776;">Ingresos</span><br><span style="font-size: 0.8rem; color: #9C7FBF;">Alimentadoras</span></div>
                <div style="background: #F5F0FA; padding: 0.75rem 1rem; border-radius: 0.5rem; border-left: 3px solid #5E4B8A;"><span style="font-weight: 700; color: #4A3776;">Ingresos</span><br><span style="font-size: 0.8rem; color: #9C7FBF;">Troncal</span></div>
                <div style="background: #F5F0FA; padding: 0.75rem 1rem; border-radius: 0.5rem; border-left: 3px solid #5E4B8A;"><span style="font-weight: 700; color: #4A3776;">Kilómetros</span><br><span style="font-size: 0.8rem; color: #9C7FBF;">Realizados y Programados</span></div>
                <div style="background: #F5F0FA; padding: 0.75rem 1rem; border-radius: 0.5rem; border-left: 3px solid #5E4B8A;"><span style="font-weight: 700; color: #4A3776;">Gastos</span><br><span style="font-size: 0.8rem; color: #9C7FBF;">Costos Operativos</span></div>
                <div style="background: #F5F0FA; padding: 0.75rem 1rem; border-radius: 0.5rem; border-left: 3px solid #5E4B8A; grid-column: span 2;"><span style="font-weight: 700; color: #4A3776;">Utilidad Mensual</span><br><span style="font-size: 0.8rem; color: #9C7FBF;">Por sistema</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)