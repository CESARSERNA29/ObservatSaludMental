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

# ----------------------------------------------------------
# Definicion de colores
# 0."Azul_os", 1."Rojo", 2."Azul_cl", 3."Gris", 4."Verde", 5."Naranja", 6."Morado"
P_Colores = ["#2A3180","#E5352B","#39A8E0","#9D9D9C","#009640","#F28F1C","#662681"]
st.session_state['P_Colores']=P_Colores
#-------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Convivencia Ciudadana", layout="wide")
st.markdown("<h2 style='text-align: left;color: #39A8E0;'>CONVIVENCIA CIUDADANA - MORBILIDAD</h2>", unsafe_allow_html=True)

#-------------------------------------------------------------------------------
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
df_mb2 = osm.bd_morbilidad('Morbilidad2')

df_pob2 = osm.bd_poblacion('Pob2',2024)
df_pob2=df_pob2[df_pob2['region']=='Orinoquía'].reset_index(drop=True)

df_mb3 = osm.bd_morbilidad('Morbilidad3')
#st.session_state['df_mb3'] = df_mb3

df_pob3 = osm.bd_poblacion('Pob3',2024)
#df_pob=df_pob[df_pob['region']=='Orinoquía'].reset_index(drop=True)
#st.session_state['df_pob3'] = df_pob3

#-------------------------------------------------------------------------------
# FILTROS
#-------------------------------------------------------------------------------


col1, col2 = st.columns([4,6])

with col1:
  # 1. Botones por departamento
  depto_sel=st.pills("Departamento", df_pob2['departamento'].unique(), 
                       selection_mode="single",default='Meta')
  df_mb2_f = df_mb2[df_mb2["departamento"] == depto_sel]
  
    # 2. Crear un selector para que el usuario elija uno o varios grupos
  grupos = df_mb2_f['grupo'].unique().tolist()
  grupo_sel = st.selectbox("Selecciona un grupo de evento", grupos)
  df_mb2_f = df_mb2_f[df_mb2["grupo"] == grupo_sel]
  
with col2:
  #  2. Botones por año
  anios=sorted(df_mb3['anio'].unique()) 
  anio_sel = st.pills("Año", anios, selection_mode="single",default=max(anios))
    # 3. Crear un selector para el evento
  eventos = df_mb2_f['Enfermedad_Evento'].unique().tolist()
  eventos.insert(0, "Todos")
  evento_sel = st.selectbox("Seleccione el evento de interes", eventos)

#-------------------------------------------------------------------------------
# Contenido Morbilidad
#-------------------------------------------------------------------------------

Total_casos=df_mb3[(df_mb3['grupo']==grupo_sel) & (df_mb3['anio']==anio_sel)]['Total'].sum()
Total_Pob=df_pob3[df_pob3['anio']==anio_sel]['Total'].sum()
Tasa_grupo_ORQ=(Total_casos/Total_Pob).round(1)


# 2. Filtrar el DataFrame según la selección del usuario

if evento_sel != "Todos":
  df_mb2_f = df_mb2_f[df_mb2_f["Enfermedad_Evento"] == evento_sel]

df_pob2_f = df_pob2.copy()
df_pob2_f=df_pob2_f[df_pob2_f['departamento']==depto_sel]
total_pob=df_pob2_f['Total'].sum()

df_mb2_ft=df_mb2_f.groupby(['anio','sexo'])['Total'].sum().reset_index()

Total_casos_depto=df_mb2_f[df_mb2_f['anio']==anio_sel]['Total'].sum()
Tasa_grupo_depto=(Total_casos_depto/total_pob).round(1)
# Tarjetas con indiadores relevantes
#-------------------------------------------------------------------------------

#col1, col2, col3, col4,col5,col6 = st.columns(6)
#col2.metric(f"Tasa Morbilidad Región {anio_sel}", Tasa_grupo_ORQ)
#col3.metric(f"Total Casos Región {anio_sel}", Total_casos)
#col4.metric(f"Tasa Morbilidad Departamento {anio_sel}", "6.87")
#col5.metric(f"Total Casos Departamento {anio_sel}", Total_casos_depto)

#style_metric_cards(
#    background_color="#ffffff",
#    border_left_color=P_Colores[0],
#    border_color=P_Colores[0],
#    box_shadow="#ccc")


col1, col2 = st.columns(2)
with col1:
  G_bar=osm.diag_barras_apil(df_mb2_f[df_mb2_f['anio']==anio_sel],'nombre_cat_edad','Total',
                                'sexo','Casos por edad',P_Colores[4:],xlab='Edad',ylab='No. de casos')
  st.plotly_chart(G_bar, use_container_width=True)
with col2:
  G_Lineas=osm.diag_lineas(df_mb2_ft,'anio','Total','sexo','Tendencia por años','N. Casos',P_Colores[4:])
  st.plotly_chart(G_Lineas, use_container_width=True)
  
  
#-------------------------------------------------------------------------------
# Diagrama de radar usando tasa por municipio por sexo y filtro por año
#-------------------------------------------------------------------------------

#  filtro por años
#anios=sorted(df_mb3['anio'].unique()) 
#anio_sel = st.pills("Año", anios, selection_mode="single",default=max(anios))

# Filtrado de la base y calculo de las tasas por municipio

df_mb3_f=df_mb3[(df_mb3['departamento']==depto_sel) & (df_mb3['grupo']==grupo_sel) & (df_mb3['anio']==anio_sel)]
df_pob3_f=df_pob3[(df_pob3['departamento']==depto_sel) & (df_pob3['anio']==anio_sel)]

df_mb3_f2=df_mb3_f.groupby(['municipio','sexo'])['Total'].sum().reset_index()
df_pob3_f.rename(columns={'Total':'pob10'},inplace=True)
df_mb3_f2=df_mb3_f2[['municipio','sexo','Total']].merge(df_pob3_f[['municipio','sexo','pob10']], on=['municipio','sexo'])
df_mb3_f2['Tasa_mb'] = (df_mb3_f2['Total'] / df_mb3_f2['pob10']).round(1)

#col1, col2 = st.columns(2)
Tabla_Tasas= df_mb3_f2.pivot(index='municipio',columns='sexo',values='Tasa_mb').reset_index()
Tabla_Tasas = Tabla_Tasas.rename(columns={'municipio': 'Municipio'})
#with col1:
G_bar2=osm.diag_barras_apil(df_mb3_f2,'municipio','Tasa_mb','sexo',
                              'Tasas de morbilidad por municipio',
                              P_Colores[4:],bmode='group',xlab='Municipios',ylab='Tasa x 10.000 hab.')
st.plotly_chart(G_bar2, use_container_width=True)
#with col2:
#  col1,col2,col3=st.columns([1,3,1])
#  with col2:
#    st.subheader('Tasas de morbilidad por municipio')
#    st.dataframe(Tabla_Tasas,width=420,hide_index=True)

