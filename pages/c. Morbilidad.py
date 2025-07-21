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
st.markdown("<h2 style='text-align: left;color: #39A8E0;'>CONVIVENCIA CIUDADANA - MORBILIDAD</h2>", unsafe_allow_html=True)

#-------------------------------------------------------------------------------

#st.markdown("""
#        <h3 style='text-align: center; color: #39A8E0;'>MORBILIDAD </h3>
#        <hr style="height:2px;border-width:0;color:gray;background-color:gray">
#    """, unsafe_allow_html=True)

#st.markdown("""
#        <div style="text-align: justify; font-size: 18px; color: #444444;">
#        Esta sección presenta datos de morbilidad, para enfermedades y problemas\ 
#        de salud que afectan a la población relacionada con factores que influyen\ 
#        en la convivencia social, incluyendo problemáticas de salud mental y\ 
#       condiciones asociadas. La información permite identificar las principales \
#        afectaciones en salud que pueden incidir en dinámicas sociales y el \
#        bienestar colectivo.
#        </div>""", unsafe_allow_html=True)



#-------------------------------------------------------------------------------
# LECTURA Y PREPARACION DE FUENTES DE DATOS
#-------------------------------------------------------------------------------
#df_mb = osm.bd_morbilidad('Morbilidad')
#st.session_state['df_mb'] = df_mb

#df_pob = osm.bd_poblacion('Pob',2024)
#df_pob=df_pob[df_pob['region']=='Orinoquía'].reset_index(drop=True)
#st.session_state['df_pob'] = df_pob
#-------------------------------------------------------------------------------
# Se definen los datos desde el estado de la sesion
#-------------------------------------------------------------------------------
df_mb2=st.session_state.get('df_mb2')
df_pob2=st.session_state.get('df_pob2')
P_Colores=st.session_state.get('P_Colores')
#-------------------------------------------------------------------------------

# Barra lateral de opciones
st.sidebar.header('Filtros')

# 1. Crear un selector para que el usuario elija uno o varios grupos
grupos = df_mb2['grupo'].unique().tolist()
grupo_sel = st.sidebar.pills("Selecciona un grupo de evento", grupos,selection_mode="single",default='Agresiones')


# 2. Crear un selector para el departamento
depto_sel=st.sidebar.pills("Departamento", df_pob2['departamento'].unique(), selection_mode="single",default='Meta')

df_mb2_f = df_mb2[(df_mb2["departamento"] == depto_sel) & (df_mb2["grupo"] == grupo_sel)]

# 3. Crear un selector para el evento
eventos = df_mb2_f['Enfermedad_Evento'].unique().tolist()
eventos.insert(0, "Todos")
evento_sel = st.sidebar.selectbox("Seleccione el evento de interes", eventos)
#-------------------------------------------------------------------------------
# Contenido Morbilidad
#-------------------------------------------------------------------------------


# 2. Filtrar el DataFrame según la selección del usuario

if evento_sel != "Todos":
  df_mb2_f = df_mb2_f[df_mb2_f["Enfermedad_Evento"] == evento_sel]


#st.dataframe(df_mb2_f)

df_pob2_f = df_pob2.copy()
df_pob2_f=df_pob2_f[df_pob2_f['departamento']==depto_sel]
total_pob=df_pob2_f['Total'].sum()

df_mb2_ft=df_mb2_f.groupby(['anio','sexo'])['Total'].sum().reset_index()

col1, col2 = st.columns(2)
with col1:
  G_bar=osm.diag_barras_apil(df_mb2_f,'nombre_cat_edad','Total','sexo','Casos por evento')
  st.plotly_chart(G_bar, use_container_width=True)
with col2:
  G_Lineas=osm.diag_lineas(df_mb2_ft,'anio','Total','sexo','CASOS DE MORBILIDAD','Numero de eventos')
  st.plotly_chart(G_Lineas, use_container_width=True)
  #tabla_morbil=osm.tabla_grupo(df_mb_f,total_pob,'departamento','Total')
  #st.dataframe(tabla_morbil,width=500)
 


#df_mb_f2=df_mb_f.copy()
#df_mb_f3=df_mb_f.copy()
#df_mb_f3.drop('Total',axis=1)
#df_mb_f3 = df_mb_f3.melt(
#    id_vars=['anio','psss','nombre_cat_edad','region','departamento','i_mpio',
#             'municipio','capitulo','grupo','Enfermedad_Evento','Detalle'], 
#    value_vars=['Hombres', 'Mujeres'], 
#    var_name='sexo',
#    value_name='cant')
#df_mb_f2=df_mb_f.groupby('nombre_cat_edad')['Total'].sum().reset_index()
#st.dataframe(df_mb_f3)


