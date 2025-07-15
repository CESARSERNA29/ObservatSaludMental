



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
        <h3 style='text-align: center; color: #333333;'>SALUD MENTAL:  Tratamiento Estadístico, KPI y Tendencias </h3>
        <hr style="height:2px;border-width:0;color:gray;background-color:gray">
    """, unsafe_allow_html=True)

st.markdown("""
        <div style="text-align: justify; font-size: 18px; color: #444444;">
        La salud mental representa un componente fundamental del bienestar general de las personas y de la estabilidad social de los territorios. No se trata únicamente de la presencia de trastornos psicológicos, sino de un estado dinámico en el que el individuo puede desarrollar sus habilidades, enfrentar las tensiones normales de la vida, trabajar de forma productiva y contribuir a su comunidad. Desde una perspectiva analítica, la salud mental puede ser entendida como un constructo multidimensional influenciado por factores biológicos, psicosociales, económicos, ambientales y culturales.
        
        El interés por estudiar la salud mental desde enfoques cuantitativos, especialmente ante el incremento de diagnósticos relacionados con trastornos de ansiedad, depresión, consumo de sustancias y conductas suicidas, es una necesidad cada vez más frecuente. Esta condición ha sido resaltada por eventos globales como la pandemia del COVID-19, crisis migratorias, desigualdades estructurales y violencia comunitaria. En regiones como la Orinoquía colombiana, caracterizadas por una amplia diversidad étnica, condiciones geográficas particulares y limitaciones estructurales de acceso a servicios de salud, el análisis estadístico riguroso de la salud mental se vuelve una herramienta crítica para orientar políticas públicas, optimizar recursos y diseñar intervenciones focalizadas.
        <br>
        A continuación se presenta un sinnúmero de desarrollos estadísticos que caracteriza las condicones de salud mental, en términos de Morbilidad y mortalidad, de la población que conforma la orinoquía colombiana.
        </div>
    """, unsafe_allow_html=True)






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
st.set_page_config(page_title="Salud Mental", layout="wide")
st.header("Eventos de Morbilidad y Mortalidad, en Salud Mental")
st.markdown("##")
#-------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
# Cargar y preparación de las fuentes de datos
#-------------------------------------------------------------------------------
# -----------------------
# Tablas para Morbilidad:
# -----------------------

@st.cache_data  # Esta linea permite acceder al df desde la memoria cache
def load_data():
    df0 = pd.read_excel('data/Tasas_Morbilidad_25MB.xlsx')
    # Convertir año a categórica
    df0['anio'] = pd.to_numeric(df0['anio'], errors='coerce')
    
    # Filtro para la region de la orinoquia
    # df0=df0[df0['region']=='Orinoquía']
    
    # Reemplazar valores en la columna 'sexo'
    df0['sexo'] = df0['sexo'].replace({'Masculino': 'Hombres','Femenino': 'Mujeres'})
    
    # Orden ctegorias de edad
    #orden_cat_edad = ['Primera infancia', 'Infancia', 'Adolescensia', 
    #                  'Adultez Temprana', 'Adultez Media', 'Adultez Mayor']
    # Convertir la columna 'nombre_cat_edad' a tipo categórico con orden
    #df0['nombre_cat_edad'] = pd.Categorical(df0['nombre_cat_edad'], 
    #                           categories=orden_cat_edad, ordered=True)
    df0['grupo'] = df0['grupo'].str.strip()  
    df0['departamento']=df0['departamento'].str.strip()
    df0['departamento']=pd.Categorical(df0['departamento'])
    
    df0['anio'] = df0['anio'].astype(str)
    
    #df_agregada = df.groupby(['componente','departamento','municipio',
    #                       'grupo','Enfermedad_Evento', 'sexo',
    #                       'nombre_cat_edad','anio'])['cant'].sum().reset_index()
    return df0  
df0 = load_data()



# ******














# -----------------------
# Tablas para Mortalidad:
# -----------------------
    
def load_data():
    df1 = pd.read_excel('data/Mortalidad2.xlsx')
    # Convertir año a categórica
    df1['anio'] = pd.to_numeric(df1['anio'], errors='coerce')
    
    # Filtro para la region de la orinoquia
    df1=df1[df1['region']=='Orinoquía']
    
    # Reemplazar valores en la columna 'sexo'
    df1['sexo'] = df1['sexo'].replace({'Masculino': 'Hombres','Femenino': 'Mujeres'})
    
    # Orden ctegorias de edad
    orden_cat_edad = ['Primera infancia', 'Infancia', 'Adolescensia', 
                      'Adultez Temprana', 'Adultez Media', 'Adultez Mayor']
    # Convertir la columna 'nombre_cat_edad' a tipo categórico con orden
    df1['nombre_cat_edad'] = pd.Categorical(df1['nombre_cat_edad'], 
                               categories=orden_cat_edad, ordered=True)
    df1['grupo'] = df1['grupo'].str.strip()  
    df1['departamento']=df1['departamento'].str.strip()
    df1['departamento']=pd.Categorical(df1['departamento'])
    
    #df1_agregada = df1.groupby(['componente','departamento','municipio',
    #                       'grupo','Enfermedad_Evento', 'sexo',
    #                       'nombre_cat_edad','anio'])['cant'].sum().reset_index()
    return df1

df1 = load_data()

#-------------------------------------------------------------------------------

# Barra lateral de opciones
#st.sidebar.image("data/logo1.png")
#-------------------------------------------------------------------------------






# ==========================================================
# Creacion de pestañas para cada componente del obsevatorio
# ==========================================================
Tab1, Tab2 = st.tabs(["Morbilidad", "Mortalidad"])

# Contenido de la primera pestaña
with Tab1:
    st.header("MORBILIDAD:  Tratamiento Estadístico, KPI y Tendencias")
    st.write("La morbilidad es la frecuencia o proporción de personas que presentan una enfermedad o condición específica dentro de una población determinada. Desde un enfoque estadístico, el análisis de la morbilidad permite identificar patrones, tendencias y distribuciones geográficas o demográficas de las enfermedades, lo cual es clave para la planificación en salud pública. Mediante indicadores como el número de casos absolutos, la tasa de morbilidad (por cada 10.000 habitantes) o la prevalencia y la incidencia, se pueden evaluar los grupos más afectados, detectar zonas de mayor vulnerabilidad y priorizar recursos. Estas métricas también permiten comparar el comportamiento de enfermedades a lo largo del tiempo o entre regiones, facilitando la toma de decisiones basadas en evidencia.  El análisis estadístico de la morbilidad es, por tanto, una herramienta fundamental para monitorear el estado de salud de una población, y diseñar intervenciones efectivas.") 
    
    
    
    # Filtro para Salud Mental 
    df_sm0 = df0[df0['componente']=='Salud Mental']  
    
    
    
    
    st.markdown("##")
    
    
    with st.expander("👉 Mostrar Filtros", expanded=False):
        Departamento = st.multiselect(
            "Selecciona Departamento", 
            options = df_sm0["departamento"].unique(), 
            default = df_sm0["departamento"].unique(),
            )
        Municipio = st.multiselect( 
            "Selecciona Municipio", 
            options = df_sm0["municipio"].unique(), 
            default = df_sm0["municipio"].unique(),
            ) 
        Grupo = st.multiselect(
            "Selecciona el Grupo de Enfermedad", 
            options = df_sm0["grupo"].unique(), 
            default = df_sm0["grupo"].unique(),
            )    
    
    # -----------
    
    df_selection = df_sm0.query(
        "departamento==@Departamento & municipio==@Municipio & grupo ==@Grupo"
    )
    
    # Esta función realiza análisis descriptivos básicos como media, moda, suma, etc.
    def Home(): 
        with st.expander("Ver el Conjunto de Datos en Excel"): 
            showData=st.multiselect('Filter: ',df_selection.columns,default=["anio", "sexo", "nombre_cat_edad", "departamento", "municipio", "componente", "capitulo", "grupo", "Enfermedad_Evento", "pob10", "tasa_morb", "Tot_Eventos"])
        st.dataframe(df_selection[showData],use_container_width=True)
    # calcular los análisis:
    total_investment = float(pd.Series(df_selection['Tot_Eventos']).sum())
    investment_mode1 = float(pd.Series(df_selection['departamento']).nunique())
    investment_mode2 = float(pd.Series(df_selection['municipio']).nunique())
    investment_median= float(pd.Series(df_selection['Enfermedad_Evento']).nunique()) 


    total1,total2,total3,total4,total5=st.columns(5,gap='small')
    with total1:
        st.info('Tot. Eventos',icon="🎯")
        st.metric(label="Tot. Casos", value=f"{total_investment:,.0f}".replace(",", "."))
    with total2:
        st.info('Tot. Dptos.',icon="🎯")
        st.metric(label="Tot. Dptos.",value=f"{investment_mode1:,.0f}")

    with total3:
        st.info('Tot. Municip.',icon="🎯")
        st.metric(label="Tot. Municip.",value=f"{investment_mode2:,.0f}")

    with total4:
        st.info('Tot. Grupo',icon="🎯")
        st.metric(label="Tot. Grupo",value=f"{investment_median:,.0f}")
        
        #variable distribution Histogram
        #with st.expander("Distribución de Frecuencias - Variables Cuantitativas"):
        # df.hist(figsize=(16,8),color='#898784', zorder=2, rwidth=0.9,legend = ['tasa_morb']);
        # st.pyplot()
    
    
    # -----------------------------------------------------
    
    st.markdown("##")
        
