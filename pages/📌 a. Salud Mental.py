



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

# Título general
st.markdown("""
<h1 style='text-align: center; color: #3A3A3A;'>📈 SALUD MENTAL: Tratamiento Estadístico, KPI y Tendencias</h1>
""", unsafe_allow_html=True)

st.markdown("##")

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







import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
#from streamlit-aggrid import AgGrid, GridOptionsBuilder



#-------------------------------------------------------------------------------
# Cargar y preparación de las fuentes de datos
#-------------------------------------------------------------------------------
# -----------------------
# Tablas para Morbilidad:
# -----------------------

@st.cache_data  # Esta linea permite acceder al df desde la memoria cache
def load_data1():
    df0 = pd.read_excel('data/Tasas_Morbilidad_25MB.xlsx')
    # Convertir año a categórica
    df0['anio'] = pd.to_numeric(df0['anio'], errors='coerce')
    df0['Tot_Eventos'] = pd.to_numeric(df0['Tot_Eventos'], errors='coerce')
    
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
    
    cols = ['Tot_Eventos', 'tasa_morb']
    df0[cols] = df0[cols].apply(pd.to_numeric, errors='coerce')
    
    #df_agregada = df.groupby(['componente','departamento','municipio',
    #                       'grupo','Enfermedad_Evento', 'sexo',
    #                       'nombre_cat_edad','anio'])['cant'].sum().reset_index()
    return df0  
df0 = load_data1()

# Filtro para Salud Mental 
df_sm0 = df0[df0['componente']=='Salud Mental'] 

# -------------------------------------------------------------------------












#------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA:
#st.set_page_config(page_title="Salud Mental", layout="wide")
#st.header("Eventos de Morbilidad y Mortalidad, en Salud Mental")
#st.markdown("##")

# Base de Referencia:
#-------------------
#df0 = pd.read_excel('Tasas_Morbilidad_25MB.xlsx', sheet_name='Hoja1')
#df0['anio'] = df0['anio'].astype(str)
#df0['Tot_Eventos'] = pd.to_numeric(df0['Tot_Eventos'], errors='coerce')





st.set_page_config(page_title="📊 Dashboard de Morbilidad", layout="wide")



# Estilo Tablero Personalizado:
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


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
anio = st.sidebar.selectbox("Selecciona Año", options=["Todos"] + sorted(df_sm0['anio'].dropna().unique().tolist()))  
departamento = st.sidebar.selectbox("Departamento", options=["Todos"] + sorted(df_sm0['departamento'].dropna().unique().tolist()))
municipio = st.sidebar.selectbox("Municipio", options=["Todos"] + sorted(df_sm0['municipio'].dropna().unique().tolist()))


# BASE DE DATOS:
# ----------------
# Aplicar filtros:
# ----------------
df_filtrado = df_sm0
if departamento != "Todos":
    df_filtrado = df_filtrado[df_filtrado['departamento'] == departamento]
if municipio != "Todos":
    df_filtrado = df_filtrado[df_filtrado['municipio'] == municipio]
if anio:
    df_filtrado = df_filtrado[df_filtrado['anio'] == anio]
# -----------------------------







# INTRODUCCIONA A MORBILIDAD:
# --------------------------
st.markdown("##")


st.header("MORBILIDAD")
st.write("La morbilidad es la frecuencia o proporción de personas que presentan una enfermedad o condición específica dentro de una población determinada. Desde un enfoque estadístico, el análisis de la morbilidad permite identificar patrones, tendencias y distribuciones geográficas o demográficas de las enfermedades, lo cual es clave para la planificación en salud pública.  \n Mediante indicadores como el número de casos absolutos, la tasa de morbilidad (por cada 10.000 habitantes) o la prevalencia y la incidencia, se pueden evaluar los grupos más afectados, detectar zonas de mayor vulnerabilidad y priorizar recursos. Estas métricas también permiten comparar el comportamiento de enfermedades a lo largo del tiempo o entre regiones, facilitando la toma de decisiones basadas en evidencia.  El análisis estadístico de la morbilidad es, por tanto, una herramienta fundamental para monitorear el estado de salud de una población, y diseñar intervenciones efectivas.") 












st.markdown("##")

# ---------------------------------------------------------------------------
# Sección de Filtrado:
# -------------------

st.subheader("Indicadores Clave de Morbilidad")

with st.expander("👉 Mostrar Filtros", expanded=False):
    Departamento = st.multiselect(
        "Selecciona Departamento", 
        options=df_sm0["departamento"].unique(), 
        default=df_sm0["departamento"].unique()
    )
    
    Municipio = st.multiselect( 
        "Selecciona Municipio", 
        options=df_sm0["municipio"].unique(), 
        default=df_sm0["municipio"].unique()
    ) 
    
    Grupo = st.multiselect(
        "Selecciona el Grupo de Enfermedad", 
        options=df_sm0["grupo"].unique(), 
        default=df_sm0["grupo"].unique()
    )    


# ✅ Filtrar el dataframe según los valores seleccionados
df_selection = df_sm0.query("departamento in @Departamento and municipio in @Municipio and grupo in @Grupo")

    

# ✅ Mostrar resultados
st.write("Datos filtrados:", df_selection)

# ----------------------------------------------------------------------------



# Secciones del dashboard
if selected == "📊 KPI":
    st.subheader("KPI")
    # calcular los Indicadores Clave de Morbilidad:
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

elif selected == "📉 Tendencias":
    st.subheader("Tendencia Anual de la Tasa de Morbilidad")
    tendencia = df_filtrado.groupby('anio').mean(numeric_only=True).reset_index()
    fig = px.line(tendencia, x='anio', y='tasa_morb', title='Tasa de Morbilidad Anual')
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
#------------------------------------------------------------------------------





# ******

# ✅ Filtrar el dataframe según los valores seleccionados
df_selection = df_sm0.query("departamento in @Departamento and municipio in @Municipio and grupo in @Grupo")

    
#--------------------------------------------------------------------------- 
# Tabla de frecuencia de grupos de enfermedades de Salud Mental 
#---------------------------------------------------------------------------
# Mostrar tabla expandible con el conjunto de datos

def Home1(): 
    with st.expander("Ver el Conjunto de Datos en Excel"): 
        showData = st.multiselect(
            'Filter:', 
            df_selection.columns,
            default=["anio", "sexo", "nombre_cat_edad", "departamento", "municipio", 
                     "componente", "capitulo", "grupo", "Enfermedad_Evento", 
                     "pob10", "tasa_morb", "Tot_Eventos"], 
            key='SelectorMultiple'
            ) 
        st.dataframe(df_selection[showData], use_container_width=True)

# Hasta aqui se muestra el excel con la base original
# ---------------------------------------------------------------------



st.markdown("##")
st.markdown("##")
    

# Llamar la función antes del resumen tabular
Home1()

st.markdown("<h4 style='color:#547FD4; font-weight:bold;'>Resumen Tabular del grupo de Enfermedades:</h4>", unsafe_allow_html=True) 

# Convertir año a categórica 
df_sm0['anio'] = pd.to_numeric(df_sm0['anio'], errors='coerce') 

# Filtro para la region de la orinoquia 
df_sm0=df_sm0[df_sm0['region']=='Orinoquía'] 


# Reemplazar valores en la columna 'sexo' 
df_sm0['sexo'] = df_sm0['sexo'].replace({'Masculino': 'Hombres','Femenino': 'Mujeres'})


# Orden ctegorias de edad 
#orden_cat_edad = ['Primera infancia', 'Infancia', 'Adolescensia', 'Adultez Temprana', 'Adultez Media', 'Adultez Mayor'] 

# Convertir la columna 'nombre_cat_edad' a tipo categórico con orden 
#df0['nombre_cat_edad'] = pd.Categorical(df0['nombre_cat_edad'], categories=orden_cat_edad, ordered=True)
df_sm0['nombre_cat_edad'] = pd.Categorical(df_sm0['nombre_cat_edad'])
df_sm0['grupo'] = df_sm0['grupo'].str.strip() 
df_sm0['departamento']= df_sm0['departamento'].str.strip() 
df_sm0['departamento']=pd.Categorical(df_sm0['departamento']) 

df_sm0['anio'] = df_sm0['anio'].astype(str)   # esto va en contra de la septima línea de código hacia arriba

# Filtro para Salud Mental 
df0_sm = df_sm0[df_sm0['componente']=='Salud Mental']

# Tabla Pivote: 
df_agregada1 = df0_sm.groupby(['grupo']).count().reset_index() 
df_agregada1_1 = df_agregada1[['grupo', 'anio']] 
df_agregada1_1.columns = ['grupo', 'cant'] 

# Calcular el total de casos 
total_casos = df_agregada1_1['cant'].sum() 

# Agregar columna de porcentaje 
df_agregada1_1['(%)'] = (df_agregada1_1['cant'] / total_casos * 100).round(2) 

st.dataframe(df_agregada1_1) 




st.markdown("##")   # SALTO

#------------------------------------------------------------------------- 

# 1. Crear los selectores para grupo de enfermedades y sexo

grupos_sm = df0_sm['grupo'].unique().tolist()
sexos = ['Todos'] + df0_sm['sexo'].dropna().unique().tolist()

st.markdown("<h5 style='font-weight:bold;'>Selecciona un grupo de enfermedades</h5>", unsafe_allow_html=True)
grupo_sm_sel = st.selectbox("Grupo", grupos_sm)

st.markdown("<h5 style='font-weight:bold;'>Selecciona el sexo</h5>", unsafe_allow_html=True)
sexo_sel = st.selectbox("Sexo", sexos)

# 2. Filtrar el DataFrame según las selecciones

df_sm_filtrado = df0_sm[df0_sm['grupo'] == grupo_sm_sel]

if sexo_sel != 'Todos':
    df_sm_filtrado = df_sm_filtrado[df_sm_filtrado['sexo'] == sexo_sel]

# 3. Agrupar los datos ya filtrados

df_sm_filtrado2 = df_sm_filtrado.groupby(
    ['anio', 'nombre_cat_edad', 'departamento']
)['anio'].count().reset_index(name='cant')






# 4. Crear la tabla cruzada sumando la columna 'cant' 
# Tabla Cruzada: 
tabla_sm2 = df_sm_filtrado2.pivot_table(
    values='cant', 
    index='nombre_cat_edad', 
    columns='departamento', 
    aggfunc='sum', 
    fill_value=0, 
    observed=False)


# 5. Mostrar la tabla en Streamlit 
st.write("Tabla cruzada, Total de Casos por Rango de Edad") 
st.dataframe(tabla_sm2) 













