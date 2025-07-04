



# Cargando las Librerías:
# ======================

import streamlit as st
import pandas as pd
# from pandas_profiling import ProfileReport
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
# from numerize.numerize import numerize
from numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
# st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go
# ----------------------------------------------------------



# Descomenta esta línea si usas MySQL:
# from query import *

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
#st.header("MORBILIDAD:  Tratamiento Estadístico, KPI y Tendencias")

st.markdown("""
        <h3 style='text-align: center; color: #333333;'>MORTALIDAD:  Tratamiento Estadístico, KPI y Tendencias </h3>
        <hr style="height:2px;border-width:0;color:gray;background-color:gray">
    """, unsafe_allow_html=True)

st.markdown("""
        <div style="text-align: justify; font-size: 18px; color: #444444;">
        La mortalidad se refiere a la cantidad de muertes ocurridas en una población durante un período específico. Desde una perspectiva estadística, el análisis de la mortalidad permite comprender el impacto de distintas causas de defunción sobre la salud pública, así como identificar grupos poblacionales en mayor riesgo o vulnerabilidad.
        
        Mediante indicadores como el número absoluto de muertes, la tasa bruta de mortalidad (por cada 10.000 habitantes), la tasa de mortalidad específica por edad, sexo o causa, es posible evaluar la carga de mortalidad y su distribución geográfica y temporal. 
        Este análisis facilita la detección de patrones, tendencias y desigualdades en las causas de muerte, contribuyendo a priorizar acciones de prevención, fortalecer los sistemas de salud y diseñar políticas públicas basadas en evidencia. En conjunto, el estudio estadístico de la mortalidad es esencial para monitorear el estado de salud de una población, evaluar intervenciones sanitarias y reducir el impacto de enfermedades prevenibles.
        </div>
    """, unsafe_allow_html=True)








st.markdown("##")
st.markdown("##")
st.markdown("##")















import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
#from streamlit-aggrid import AgGrid, GridOptionsBuilder

#-------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Mortalidad", layout="wide")
st.header("Eventos de mortalidad en salud mental y convivencia ciudadana")
st.markdown("##")
#-------------------------------------------------------------------------------

# Cargar y preparación de las fuentes de datos
#-------------------------------------------------------------------------------
@st.cache_data  # Esta linea permite acceder al df desde la memoria cache
def load_data():
    df = pd.read_excel('data/Mortalidad2.xlsx')
    # Convertir año a categórica
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    
    # Filtro para la region de la orinoquia
    df=df[df['region']=='Orinoquía']
    
    # Reemplazar valores en la columna 'sexo'
    df['sexo'] = df['sexo'].replace({'Masculino': 'Hombres','Femenino': 'Mujeres'})
    
    # Orden ctegorias de edad
    orden_cat_edad = ['Primera infancia', 'Infancia', 'Adolescensia', 
                      'Adultez Temprana', 'Adultez media', 'Adultez mayor']
    # Convertir la columna 'nombre_cat_edad' a tipo categórico con orden
    df['nombre_cat_edad'] = pd.Categorical(df['nombre_cat_edad'], 
                               categories=orden_cat_edad, ordered=True)
    df['grupo'] = df['grupo'].str.strip()  
    df['departamento']=df['departamento'].str.strip()
    df['departamento']=pd.Categorical(df['departamento'])
    
    #df_agregada = df.groupby(['componente','departamento','municipio',
    #                       'grupo','Enfermedad_Evento', 'sexo',
    #                       'nombre_cat_edad','anio'])['cant'].sum().reset_index()
    return df

df = load_data()
#-------------------------------------------------------------------------------

# Barra lateral de opciones
st.sidebar.image("data/logo1.png")
#-------------------------------------------------------------------------------


# Creacion de pestañas para cada componente del obsevatorio

Tab1, Tab2 = st.tabs(["Salud Mental", "Convivencia Ciudadana"])

# Contenido de la primera pestaña
with Tab1:
    st.header("SALUD MENTAL")
    st.write("Aquí va el contenido de la primera pestaña.")
    
    df_sm=df[df['componente']=='Salud Mental']
    
    #---------------------------------------------------------------------------
    # Tabla de frecuencia de muertes asocciadas a grupos de enfermedades de 
    # Salud mental
    #---------------------------------------------------------------------------    
    tabla_sm1 = pd.pivot_table(
    df_sm,
    values='cant',
    index='grupo',
    aggfunc='sum',
    fill_value=0
    )
    # Calcular el total de casos
    total_casos = tabla_sm1['cant'].sum()
    
    # Agregar columna de porcentaje
    tabla_sm1['(%)'] = (tabla_sm1['cant'] / total_casos * 100).round(2)
    
    st.dataframe(tabla_sm1)
    
    #---------------------------------------------------------------------------
    
    # 1. Crear un selector para que el usuario elija uno o varios grupos
    grupos_sm = df_sm['grupo'].unique().tolist()
    grupo_sm_sel = st.selectbox("Selecciona un grupo de enfermedad", grupos_sm)
    
        # 2. Filtrar el DataFrame según la selección del usuario
    df_sm_filtrado = df_sm[df_sm['grupo'] == grupo_sm_sel]
    
    # 3. Crear la tabla cruzada sumando la columna 'cant'
    tabla_sm2 = pd.pivot_table(
    df_sm_filtrado,
    values='cant',
    index='nombre_cat_edad',
    columns='departamento',
    aggfunc='sum',
    fill_value=0,
    observed=False
    )
    
    #tabla_cruzada2 = tabla_cruzada2.style.set_properties(**{'text-align': 'center'})
    
    # 4. Mostrar la tabla en Streamlit
    st.write("Tabla cruzada de suma de 'cant' por rango_edad y sexo")
    st.dataframe(tabla_sm2)
    
    
    
    
    #---------------------------------------------------------------------------
    # Diagrama de lineas año y sexo
    P_Colores = {
    "Azul_cl": "#39A8E0",
    "Gris": "#9D9D9C",
    "Verde": "#009640",
    "Naranja": "#F28F1C",
    "Azul_os": "#2A3180",
    "Rojo": "#E5352B",
    "Morado":"#662681"}
    
    a_min_sm=df_sm['anio'].min()-1
    a_max_sm=df_sm['anio'].max()+1
    
    # 1. Crear un selector para que el usuario elija uno o varios grupos
    deptos_sm = df_sm['departamento'].unique().tolist()
    depto_sm_sel = st.selectbox("Selecciona un departamento", deptos_sm, key="sel_dpto_sm")
    
    df_sm_filtrado2=df_sm_filtrado[df_sm_filtrado['departamento']==depto_sm_sel]
    
    df_sm3 = df_sm_filtrado2.groupby(['sexo','anio'])['cant'].sum().reset_index()
    
    # Crear gráfico de líneas con Plotly Express
    fig_sm = px.line(df_sm3,x='anio',y='cant',
          color='sexo',markers=True,
          title="TENDENCIA DE EVENTOS DE MORTALIDAD",
          color_discrete_sequence=["#2A3180","#E5352B"])
    
    # Personalizar marcadores para que tengan borde del color de la línea y fondo blanco
    fig_sm.update_traces(
        marker=dict(size=10,
            color='white',          # fondo blanco
            line=dict(width=2)      # borde que tomará el color de la línea
       )
    )
    
    # Ajustar eje x para mostrar todos los años y con rango fijo
    fig_sm.update_xaxes(
        dtick=1,
        range=[a_min_sm,a_max_sm],
        tickmode='linear'
    )
    
    fig_sm.update_xaxes(title_text="")
    fig_sm.update_yaxes(title_text="Número de casos")
    
    st.plotly_chart(fig_sm, use_container_width=True)
    #----------------------------------------------------------------------------- 
    
# Contenido de la segunda pestaña
with Tab2:
    st.header("CONVIVENCIA CIUDADANA")
    st.write("Aquí va el contenido de la segunda pestaña.")
    
    df_cc=df[df['componente']=='Conv. Ciudadana']


    tabla_cc1 = pd.pivot_table(
    df_cc,
    values='cant',
    index='grupo',
    aggfunc='sum',
    fill_value=0
    )
    # Calcular el total de casos
    total_casos_cc = tabla_cc1['cant'].sum()
    
    # Agregar columna de porcentaje
    tabla_cc1['(%)'] = (tabla_cc1['cant'] / total_casos_cc * 100).round(2)
    
    st.dataframe(tabla_cc1)
    
    #---------------------------------------------------------------------------
    
    # 1. Crear un selector para que el usuario elija uno o varios grupos
    grupos_cc = df_cc['grupo'].unique().tolist()
    grupo_cc_sel = st.selectbox("Selecciona un grupo de enfermedad", grupos_cc)
    
        # 2. Filtrar el DataFrame según la selección del usuario
    df_cc_filtrado = df_cc[df_cc['grupo'] == grupo_cc_sel]
    
    # 3. Crear la tabla cruzada sumando la columna 'cant'
    tabla_cc2 = pd.pivot_table(
    df_cc_filtrado,
    values='cant',
    index='nombre_cat_edad',
    columns='departamento',
    aggfunc='sum',
    fill_value=0,
    observed=False
    )
    
    #tabla_cruzada2 = tabla_cruzada2.style.set_properties(**{'text-align': 'center'})
    
    # 4. Mostrar la tabla en Streamlit
    st.write("Tabla cruzada de suma de 'cant' por rango_edad y sexo")
    st.dataframe(tabla_cc2)
    
    #---------------------------------------------------------------------------
    # Diagrama de lineas año y sexo
    
    a_min_cc=df_cc['anio'].min()-1
    a_max_cc=df_cc['anio'].max()+1
    
    # 1. Crear un selector para que el usuario elija uno o varios grupos
    deptos_cc = df_cc['departamento'].unique().tolist()
    depto_cc_sel = st.selectbox("Selecciona un departamento", deptos_cc,key="sel_dpto_cc")
    
    df_cc_filtrado_2=df_cc_filtrado[df_cc_filtrado['departamento']==depto_cc_sel]
    
    df_cc_3 = df_cc_filtrado_2.groupby(['sexo','anio'])['cant'].sum().reset_index()
    
    # Crear gráfico de líneas con Plotly Express
    fig_cc = px.line(df_cc_3,x='anio',y='cant',
          color='sexo',markers=True,
          title="TENDENCIA DE EVENTOS DE MORTALIDAD",
          color_discrete_sequence=["#2A3180","#E5352B"])
    
    # Personalizar marcadores para que tengan borde del color de la línea y fondo blanco
    fig_cc.update_traces(
        marker=dict(size=10,
            color='white',          # fondo blanco
            line=dict(width=2)      # borde que tomará el color de la línea
       )
    )
    
    # Ajustar eje x para mostrar todos los años y con rango fijo
    fig_cc.update_xaxes(
        dtick=1,
        range=[a_min_cc,a_max_cc],
        tickmode='linear'
    )
    
    fig_cc.update_xaxes(title_text="")
    fig_cc.update_yaxes(title_text="Número de casos")
    
    st.plotly_chart(fig_cc, use_container_width=True)
    
    




















