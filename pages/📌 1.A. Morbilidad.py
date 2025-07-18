# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 22:44:41 2025

@author: cesar
"""

# dashboard_morbilidad.py

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize import numerize
from streamlit_extras.metric_cards import style_metric_cards

# Configuración inicial
df = pd.read_excel('Tasas_Morbilidad_25MB.xlsx', sheet_name='Hoja1')
df['anio'] = df['anio'].astype(str)

st.set_page_config(page_title="📊 Dashboard de Morbilidad", page_icon="🧠", layout="wide")

# Estilo personalizado
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Título general
st.markdown("""
<h1 style='text-align: center; color: #3A3A3A;'>📈 MORBILIDAD: Tratamiento Estadístico, KPI y Tendencias</h1>
""", unsafe_allow_html=True)

# Menú de navegación elegante
with st.sidebar:
    selected = option_menu(
        menu_title="Navegación",
        options=["📊 KPI", "📉 Tendencias", "📍 Mapa", "📥 Datos"],
        icons=["speedometer", "bar-chart-line", "geo-alt", "table"],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "5px", "background-color": "#f8f9fa"},
            "icon": {"color": "#0d6efd", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px"},
            "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
        }
    )

# Filtros elegantes
st.sidebar.markdown("### Filtros")
anio = st.sidebar.selectbox("Selecciona Año", options=["Todos"] + sorted(df['anio'].dropna().unique().tolist()))  
departamento = st.sidebar.selectbox("Departamento", options=["Todos"] + sorted(df['departamento'].dropna().unique().tolist()))
municipio = st.sidebar.selectbox("Municipio", options=["Todos"] + sorted(df['municipio'].dropna().unique().tolist()))

# Aplicar filtros
df_filtrado = df.copy()
if departamento != "Todos":
    df_filtrado = df_filtrado[df_filtrado['departamento'] == departamento]
if municipio != "Todos":
    df_filtrado = df_filtrado[df_filtrado['municipio'] == municipio]
if anio:
    df_filtrado = df_filtrado[df_filtrado['anio'] == anio]

# Secciones del dashboard
if selected == "📊 KPI":
    st.subheader("Indicadores Clave de Morbilidad")
    col1, col2, col3 = st.columns(3)
    col1.metric("Casos Totales", numerize.numerize(df_filtrado["casos"].sum()), "↗︎")
    col2.metric("Tasa Promedio", f"{df_filtrado['tasa_morbilidad'].mean():.2f}")
    col3.metric("Número de Municipios", df_filtrado["municipio"].nunique())

    style_metric_cards(
        background_color="#F0F2F6",
        border_left_color="#0d6efd",
        border_color="#e6e6e6"
    )

elif selected == "📉 Tendencias":
    st.subheader("Tendencia Anual de la Tasa de Morbilidad")
    tendencia = df_filtrado.groupby('anio').mean(numeric_only=True).reset_index()
    fig = px.line(tendencia, x='anio', y='tasa_morbilidad', title='Tasa de Morbilidad Anual')
    st.plotly_chart(fig, use_container_width=True)

elif selected == "📍 Mapa":
    st.subheader("Mapa Interactivo de Morbilidad")
    if 'latitud' in df_filtrado.columns and 'longitud' in df_filtrado.columns:
        st.map(df_filtrado[['latitud', 'longitud']].dropna())
    else:
        st.warning("No hay coordenadas disponibles para mostrar el mapa.")

elif selected == "📥 Datos":
    st.subheader("Datos Detallados")
    st.dataframe(df_filtrado)
