# Cargando las Librerías:
# ======================

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
st.markdown("<h2 style='text-align: left;color: #39A8E0;'>CONVIVENCIA CIUDADANA - MORTALIDAD</h2>", unsafe_allow_html=True)
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# RECUPERACION DE DATOS DESDE EL SESION_STATE
#-------------------------------------------------------------------------------
# Se definen los datos desde el estado de la sesion
df_mt2=st.session_state.get('df_mt2')
df_pob2=st.session_state.get('df_pob2')
P_Colores=st.session_state.get('P_Colores')
#-------------------------------------------------------------------------------
# FILTROS
#-------------------------------------------------------------------------------
# 1. Crear un selector para el departamento
depto_sel=st.pills("Departamento", df_pob2['departamento'].unique(), 
                     selection_mode="single",default='Meta')
df_mt2_f = df_mt2[df_mt2["departamento"] == depto_sel]

col1, col2 = st.columns([3,7])

with col1:
  # 2. Crear un selector para que el usuario elija uno o varios grupos
  grupos = df_mt2_f['grupo'].unique().tolist()
  grupo_sel = st.selectbox("Selecciona un grupo de evento", grupos)
  df_mt2_f = df_mt2_f[df_mt2["grupo"] == grupo_sel]
  
with col2:
  # 3. Crear un selector para el evento
  eventos = df_mt2_f['Enfermedad_Evento'].unique().tolist()
  eventos.insert(0, "Todos")
  evento_sel = st.selectbox("Seleccione el evento de interes", eventos)

#-------------------------------------------------------------------------------
# Contenido Mortalidad
#-------------------------------------------------------------------------------

# 2. Filtrar el DataFrame según la selección del usuario

if evento_sel != "Todos":
  df_mt2_f = df_mt2_f[df_mt2_f["Enfermedad_Evento"] == evento_sel]

df_pob2_f = df_pob2.copy()
df_pob2_f=df_pob2_f[df_pob2_f['departamento']==depto_sel]
total_pob=df_pob2_f['Total'].sum()

df_mt2_ft=df_mt2_f.groupby(['anio','sexo'])['Total'].sum().reset_index()

col1, col2 = st.columns(2)
with col1:
  G_bar=osm.diag_barras_apil(df_mt2_f,'nombre_cat_edad','Total','sexo','Casos por edad',P_Colores)
  st.plotly_chart(G_bar, use_container_width=True)
with col2:
  G_Lineas=osm.diag_lineas(df_mt2_ft,'anio','Total','sexo','Tendencia por años','N. Casos')
  st.plotly_chart(G_Lineas, use_container_width=True)

    
   
