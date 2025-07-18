# Cargando las Librerías:
# ==============================================================================

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import numpy as np
import modulo_osm as osm

#-------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Convivencia Ciudadana", layout="wide")
st.markdown("<h2 style='text-align: center;color: #39A8E0;'>CONVIVENCIA CIUDADANA</h2>", unsafe_allow_html=True)
st.markdown("##")
#-------------------------------------------------------------------------------

st.markdown("""
        <h3 style='text-align: center; color: #39A8E0;'>MORBILIDAD </h3>
        <hr style="height:2px;border-width:0;color:gray;background-color:gray">
    """, unsafe_allow_html=True)

st.markdown("""
        <div style="text-align: justify; font-size: 18px; color: #444444;">
        Esta sección presenta datos de morbilidad, para enfermedades y problemas\ 
        de salud que afectan a la población relacionada con factores que influyen\ 
        en la convivencia social, incluyendo problemáticas de salud mental y\ 
        condiciones asociadas. La información permite identificar las principales \
        afectaciones en salud que pueden incidir en dinámicas sociales y el \
        bienestar colectivo.
        </div>""", unsafe_allow_html=True)

st.markdown("##")
#-------------------------------------------------------------------------------
# Se definen los datos desde el estado de la sesion
df_mb=st.session_state.get('df_mb')
df_pob2=st.session_state.get('df_pob2')
#-------------------------------------------------------------------------------

# Barra lateral de opciones
st.sidebar.image("data/logo1.png")
#-------------------------------------------------------------------------------

# Contenido Morbilidad


col1, col2 =st.columns(2)

with col1:
  
  # 1. Crear un selector para que el usuario elija uno o varios grupos
  grupos = df_mb['grupo'].unique().tolist()
  grupos.insert(0, "Todos")
  grupo_sel = st.selectbox("Selecciona un grupo de evento", grupos)

with col2:
  
  # 1. Crear un selector para el departamento
  deptos = df_mb['departamento'].unique().tolist()
  deptos.insert(0, "Todos")
  depto_sel = st.selectbox("Seleccione el departamento de interes", deptos)
  

# 2. Filtrar el DataFrame según la selección del usuario
df_mb_f = df_mb.copy()
if depto_sel == "Todos" and grupo_sel=="Todos":
  df_mb_f = df_mb.copy()
elif depto_sel != "Todos" and grupo_sel=="Todos":
    df_mb_f = df_mb_f[df_mb_f["departamento"] == depto_sel]
elif depto_sel == "Todos" and grupo_sel!="Todos":
    df_mb_f = df_mb_f[df_mb_f["grupo"] == grupo_sel]
else:
    df_mb_f = df_mb_f[(df_mb_f["departamento"] == depto_sel) & (df_mb_f["grupo"] == grupo_sel)]


st.dataframe(df_mb_f)

df_pob2_f = df_pob2.copy()
if depto_sel != "Todos":
  df_pob2_f=df_pob2_f[df_pob2_f['departamento']==depto_sel]
total_pob=df_pob2_f['pob10'].sum()

col1, col2 = st.columns(2)
with col1:
  st.write('algo')

with col2:
  
  tabla_morbil=osm.tabla_grupo(df_mb_f,total_pob,'nombre_cat_edad','cant')
  st.dataframe(tabla_morbil,width=500)
 
# 1. Crear un selector para el evento
eventos = df_mb_f['Enfermedad_Evento'].unique().tolist()
eventos.insert(0, "Todos")
evento_sel = st.selectbox("Seleccione el evento de interes", eventos)

df_mb_f2=df_mb_f
col1, col2 = st.columns(2)

with col1:
  osm.diag_lineas(df_mb_f2,'Numero de eventos')

with col2:
  tabla_evento=osm.tabla_grupo(df_mb_f2,total_pob,'nombre_cat_edad','cant')
  st.dataframe(tabla_evento,width=500)
