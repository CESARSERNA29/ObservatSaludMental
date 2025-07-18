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

#from streamlit-aggrid import AgGrid, GridOptionsBuilder
# from pandas_profiling import ProfileReport
# st.set_option('deprecation.showPyplotGlobalUse', False)
# from numerize.numerize import numerize
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

@st.cache_data  # Esta linea permite acceder al df desde la memoria cache

# ------------------------------------------------------------------------------
# Tablas para Morbilidad
# ------------------------------------------------------------------------------
def bd_morbilidad():
    df = pd.read_excel('data/Vistas_DB.xlsx',sheet_name='V_Morbilidad')
    # Convertir año a categórica
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df['grupo'] = df['grupo'].str.strip()  
    df['departamento']=df['departamento'].str.strip()
    df['departamento']=pd.Categorical(df['departamento'])
    df['anio'] = df['anio'].astype(str)
    df=df[df['componente']=='Conv. Ciudadana']
    df=df.drop(['cie10','componente'],axis=1)
    return df
# ------------------------------------------------------------------------------
# Tablas para Mortalidad
# ------------------------------------------------------------------------------
def bd_mortalidad():
    df = pd.read_excel('data/Vistas_DB.xlsx',sheet_name='V_Mortalidad')
    # Convertir año a categórica
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df['grupo'] = df['grupo'].str.strip()  
    df['departamento']=df['departamento'].str.strip()
    df['departamento']=pd.Categorical(df['departamento'])
    df['anio'] = df['anio'].astype(str)
    df=df[df['componente']=='Conv. Ciudadana']
    df=df.drop(['componente'],axis=1)
    return df
# ------------------------------------------------------------------------------
# Tablas Población
# ------------------------------------------------------------------------------
def bd_poblacion():
    df = pd.read_excel('data/Vistas_DB.xlsx',sheet_name='V_Poblacion')
    # Convertir año a categórica
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df=df[df['anio']<=2024]
    df['departamento']=pd.Categorical(df['departamento'])
    
    return df
# ------------------------------------------------------------------------------
# Tablas Delitos Policia Nacional
# ------------------------------------------------------------------------------
def bd_ponal():
    df = pd.read_excel('data/Vistas_DB.xlsx',sheet_name='V_Delitos')
    # Convertir año a categórica
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df['departamento']=pd.Categorical(df['departamento'])
    
    return df
#-------------------------------------------------------------------------------
# Lectura de datos y disposicion en la sesion

if 'df_mb' not in st.session_state:
    df_mb = bd_morbilidad()
    st.session_state['df_mb'] = df_mb

if 'df_mt' not in st.session_state:
    df_mt = bd_mortalidad()
    st.session_state['df_mt'] = df_mt

if 'df_pob' not in st.session_state:
    df_pob = bd_poblacion()
    st.session_state['df_pob'] = df_pob

if 'df_dlt' not in st.session_state:
    df_dlt = bd_ponal()
    st.session_state['df_dlt'] = df_dlt
#-------------------------------------------------------------------------------

# Barra lateral de opciones
st.sidebar.image("data/logo1.png")
#-------------------------------------------------------------------------------

st.header("Eventos asociados a Convivencia Ciudadana")
st.write("Esta sección presenta datos de eventos asociados a la convivencia ciudadana \
en terminos generales de acuerdo a los grupos de eventos tanto en morbilidad como en mortalidad. ")



#---------------------------------------------------------------------------
# Tabla de frecuencia de muertes asocciadas a grupos de enfermedades de 
# Salud mental
#---------------------------------------------------------------------------    

df_pob2=df_pob[df_pob['region']=='Orinoquía'].reset_index(drop=True)
st.session_state['df_pob2'] = df_pob2
total_pob = df_pob2['pob10'].sum()


tabla_grupos_mb=osm.tabla_grupo(df_mb,total_pob,'grupo','cant')
tabla_grupos_mt=osm.tabla_grupo(df_mt,total_pob,'grupo','cant')
col1, col2, col3 = st.columns([1, 2, 1])  # columnas con proporciones

with col2:
    st.markdown("""<h4 style='text-align: center; color: #39A8E0;'>Morbilidad </h4>""",
      unsafe_allow_html=True)
    st.dataframe(tabla_grupos_mb,width=500)
    
    st.markdown("##")
    
    st.markdown("""
    <h4 style='text-align: center; color: #39A8E0;'>Mortalidad </h4>""", 
      unsafe_allow_html=True)
    st.dataframe(tabla_grupos_mt,width=500)

#-------------------------------------------------------------------------------

def tabla_dlt2(df,total_pob):
  df=df[df['region']=='Orinoquía']
  tabla = pd.pivot_table(df,values='cant',index='desc_delito',aggfunc='sum',fill_value=0).reset_index()
  tabla.reset_index(drop=True)
  # Calcular el total de casos
  total_casos = tabla['cant'].sum()

  # Agregar columna de porcentaje
  tabla['(%)'] = (tabla['cant'] / total_casos * 100).round(2)
  tabla['Tasa'] = (tabla['cant'] / total_pob).round(2)
  
  tabla = tabla.rename(columns={'desc_delito':'Delito','cant':'Número de Casos',
                                'Tasa':'Tasa x 10000 Hab.'})
  
  # Aplicar estilo para centrar solo las columnas 'Número de Casos' y '(%)'
  tabla = tabla.style\
        .set_properties(
            subset=['Número de Casos', '(%)', 'Tasa x 10000 Hab.'],
            **{'text-align': 'center'}
        )\
        .set_table_styles(
            [{'selector': 'th', 'props': [('text-align', 'center')]}]
        )\
        .format({
            '(%)': '{:.2f}',
            'Tasa x 10000 Hab.': '{:.2f}',
            'Número de Casos': '{:,.0f}'
        })
  
  return(tabla)

st.markdown("##")

tabla_delitos=tabla_dlt2(df_dlt,total_pob)
col1, col2, col3 = st.columns([1, 3, 1])  # columnas con proporciones

with col2:
    st.markdown("""<h4 style='text-align: center; color: #39A8E0;'>Delitos registrados por la Policia Nacional </h4>""",
      unsafe_allow_html=True)
    st.dataframe(tabla_delitos,width=700)

