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
#import numpy as np
import modulo_osm as osm

# ----------------------------------------------------------
# Definicion de colores
P_Colores = {
"Azul_cl": "#39A8E0",
"Gris": "#9D9D9C",
"Verde": "#009640",
"Naranja": "#F28F1C",
"Azul_os": "#2A3180",
"Rojo": "#E5352B",
"Morado":"#662681"}
st.session_state['P_Colores']=P_Colores
#-------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Convivencia Ciudadana", layout="wide")
st.markdown("<h2 style='text-align: center;color: #39A8E0;'>CONVIVENCIA CIUDADANA</h2>", unsafe_allow_html=True)

#-------------------------------------------------------------------------------

st.markdown("""
        <h3 style='text-align: center; color: #39A8E0;'>Introducción </h3>
        <hr style="height:2px;border-width:0;color:gray;background-color:gray">
    """, unsafe_allow_html=True)

st.markdown("""
        <div style="text-align: justify; font-size: 18px; color: #000000;">
        La convivencia ciudadana es la capacidad de los ciudadanos para vivir juntos en armonía, respetando normas comunes y resolviendo conflictos de manera pacífica, lo cual es esencial para garantizar entornos seguros y el bienestar social. Esta sección examina indicadores clave que reflejan la realidad social y de salud en la región de Orinoquía, permitiendo entender mejor los factores que afectan la calidad de vida y el tejido social. Al analizar diferentes dimensiones —morbilidad, mortalidad y delitos reportados— se facilita la toma de decisiones informadas para promover una convivencia más segura, inclusiva y saludable.
        </div>
    """, unsafe_allow_html=True)

st.markdown("##")

#-------------------------------------------------------------------------------
# LECTURA Y PREPARACION DE FUENTES DE DATOS
#-------------------------------------------------------------------------------

#@st.cache_data  # Esta linea permite acceder al df desde la memoria cache

df_mb2 = osm.bd_morbilidad('Morbilidad2')
st.session_state['df_mb2'] = df_mb2

df_mt2 = osm.bd_mortalidad('Mortalidad2')
st.session_state['df_mt2'] = df_mt2

df_pob2 = osm.bd_poblacion('Pob2',2024)
df_pob2=df_pob2[df_pob2['region']=='Orinoquía'].reset_index(drop=True)
st.session_state['df_pob2'] = df_pob2

df_dlt = osm.bd_ponal()
st.session_state['df_dlt'] = df_dlt
    
#-------------------------------------------------------------------------------
# Barra lateral de opciones
st.sidebar.header('Filtros')
anios=df_pob2['anio'].unique()  #  Se escoge los años de mortalidad por ser el conjunto mas reducido
anio_sel = st.sidebar.segmented_control("Año", anios, selection_mode="single",default=anios.max())
depto_sel=st.sidebar.pills("Departamento", df_pob2['departamento'].unique(), selection_mode="single",default='Meta')
#-------------------------------------------------------------------------------

st.header("Eventos asociados a Convivencia Ciudadana")
st.write("Esta sección presenta datos de eventos asociados a la convivencia ciudadana \
en terminos generales de acuerdo a los grupos de eventos tanto en morbilidad como en mortalidad. ")



#---------------------------------------------------------------------------
# T
#---------------------------------------------------------------------------    


total_pob = df_pob2[(df_pob2['anio']==anio_sel) & (df_pob2['departamento']==depto_sel)]['Total'].sum()

df_mb2_f=df_mb2[(df_mb2['anio']==anio_sel) & (df_mb2['departamento']==depto_sel)]
df_mt2_f=df_mt2[(df_mt2['anio']==anio_sel) & (df_mt2['departamento']==depto_sel)]

#st.dataframe(df_mb2_f)
#st.dataframe(df_mt2_f)
col1, col2, col3 = st.columns([1, 2, 1])  # columnas con proporciones

with col2:    
    tabla_grupos_mb=osm.tabla_grupo(df_mb2_f,total_pob,'grupo','Total')
    tabla_grupos_mt=osm.tabla_grupo(df_mt2_f,total_pob,'grupo','Total')

    st.markdown("""<h4 style='text-align: center; color: #39A8E0;'>Morbilidad </h4>""",
      unsafe_allow_html=True)
    st.dataframe(tabla_grupos_mb,width=500)
    
    st.markdown("##")
    
    st.markdown("""
    <h4 style='text-align: center; color: #39A8E0;'>Mortalidad </h4>""", 
      unsafe_allow_html=True)
    st.dataframe(tabla_grupos_mt,width=500)

#-------------------------------------------------------------------------------

st.markdown("##")
df_dlt2=df_dlt[(df_dlt['anio']==anio_sel) & (df_dlt['departamento']==depto_sel)]
tabla_delitos=osm.tabla_grupo(df_dlt2,total_pob,'desc_delito','Total')

col1, col2, col3 = st.columns([1, 3, 1])  # columnas con proporciones

with col2:
    st.markdown("""<h4 style='text-align: center; color: #39A8E0;'>Delitos registrados por la Policia Nacional </h4>""",
      unsafe_allow_html=True)
    st.dataframe(tabla_delitos,width=700)

