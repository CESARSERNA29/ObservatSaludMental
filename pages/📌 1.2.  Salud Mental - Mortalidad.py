



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


#  ------------------------------------------------------------



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
# -------------------------------
# Tabla de Datos para Mortalidad:
# -------------------------------




# --------------------------------
# Tabla de Datos para Mortalidad:
# --------------------------------
@st.cache_data  # Esta linea permite acceder al df desde la memoria cache
def load_data2():
    df1 = pd.read_excel('data/Mortalidad2.xlsx')
    # Convertir año a categórica
    df1['anio'] = pd.to_numeric(df1['anio'], errors='coerce')
    
    # Filtro para la region de la orinoquia
    df1=df1[df1['region']=='Orinoquía']
    
    # Reemplazar valores en la columna 'sexo'
    df1['sexo'] = df1['sexo'].replace({'Masculino': 'Hombres','Femenino': 'Mujeres'})
    
    # Orden ctegorias de edad
    #orden_cat_edad = ['Primera infancia', 'Infancia', 'Adolescensia', 
    #                  'Adultez Temprana', 'Adultez Media', 'Adultez Mayor']
    # Convertir la columna 'nombre_cat_edad' a tipo categórico con orden
    #df1['nombre_cat_edad'] = pd.Categorical(df1['nombre_cat_edad'], 
    #                           categories=orden_cat_edad, ordered=True)
    df1['grupo'] = df1['grupo'].str.strip()  
    df1['departamento']=df1['departamento'].str.strip()
    df1['departamento']=pd.Categorical(df1['departamento'])
    
    #df1_agregada = df1.groupby(['componente','departamento','municipio',
    #                       'grupo','Enfermedad_Evento', 'sexo',
    #                       'nombre_cat_edad','anio'])['cant'].sum().reset_index()
    return df1

df1 = load_data2()

df_sm1=df1[df1['componente']=='SM']



#-------------------------------------------------------------------------------




st.markdown("##")







#------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA:
# Base de Referencia:
#-------------------


#st.set_page_config(page_title="📊 Dashboard de Mortalidad", layout="wide")



# Estilo Tablero Personalizado:

#with open("style.css") as f:
#    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Menú de navegación elegante
#with st.sidebar:
#    selected = option_menu(
#        menu_title="Navegación",
#        options=["📊 KPI", "📉 Tendencias", "📍 Mapa", "📥 Datos"],
#        icons=["speedometer", "bar-chart-line", "geo-alt", "table"],
#        default_index=0,
#        orientation="vertical",
#        styles={
#            "container": {"padding": "5px", "background-color": "#f8f9fa"},
#            "icon": {"color": "#0d6efd", "font-size": "18px"},
#            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px"},
#            "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
#        }
#    )

# Filtros elegantes
#st.sidebar.markdown("### Filtros")
#anio = st.sidebar.selectbox("Selecciona Año", options=["Todos"] + sorted(df_sm0['anio'].dropna().unique().tolist()))  
#departamento = st.sidebar.selectbox("Departamento", options=["Todos"] + sorted(df_sm0['departamento'].dropna().unique().tolist()))
#municipio = st.sidebar.selectbox("Municipio", options=["Todos"] + sorted(df_sm0['municipio'].dropna().unique().tolist()))


# BASE DE DATOS:
# ----------------
# Aplicar filtros:
# ----------------
df_filtrado = df_sm1.copy()

#if departamento != "Todos":
#    df_filtrado = df_filtrado[df_filtrado['departamento'] == departamento]
#if municipio != "Todos":
#    df_filtrado = df_filtrado[df_filtrado['municipio'] == municipio]
#if anio:
#    df_filtrado = df_filtrado[df_filtrado['anio'] == anio]
# -----------------------------






# SECCIÓN 1.2. : 
# INTRODUCCIONA A MORTALIDAD:
# --------------------------
st.markdown("##")




st.header("MORTALIDAD")
st.write(" La mortalidad se refiere a la cantidad de muertes ocurridas en una población durante un período específico. Desde una perspectiva estadística, el análisis de la mortalidad permite comprender el impacto de distintas causas de defunción sobre la salud pública, así como identificar grupos poblacionales en mayor riesgo o vulnerabilidad.  Mediante indicadores como el número absoluto de muertes, la tasa bruta de mortalidad (por cada 10.000 habitantes), la tasa de mortalidad específica por edad, sexo o causa, es posible evaluar la carga de mortalidad y su distribución geográfica y temporal. Este análisis facilita la detección de patrones, tendencias y desigualdades en las causas de muerte, contribuyendo a priorizar acciones de prevención, fortalecer los sistemas de salud y diseñar políticas públicas basadas en evidencia. En conjunto, el estudio estadístico de la mortalidad es esencial para monitorear el estado de salud de una población, evaluar intervenciones sanitarias y reducir el impacto de enfermedades prevenibles.") 












st.markdown("##")

# ---------------------------------------------------------------------------
# Sección de Filtrado:
# -------------------

st.subheader("Indicadores Clave de Morbilidad")

# ---------------------------------------------------------------------------
# Sección de Filtros – Ocultos pero definidos por defecto
# ---------------------------------------------------------------------------

# 🧩 Valores por defecto para los filtros (sin mostrarlos)
Departamento = df_sm1['departamento'].dropna().unique().tolist()
Municipio = df_sm1['municipio'].dropna().unique().tolist()
Grupo = df_sm1['grupo'].dropna().unique().tolist()

# ✅ DataFrame filtrado (en este caso sin aplicar restricciones)
df_selection = df_sm1[
    (df_sm1['departamento'].isin(Departamento)) &
    (df_sm1['municipio'].isin(Municipio)) &
    (df_sm1['grupo'].isin(Grupo))
]

# ---------------------------------------------------------------------------

# -----------------------------------------------------------------
# st.expander("👉 Mostrar Filtros", expanded=False)
#with st.expander("👉 Mostrar Filtros", expanded=False):
#    Departamento = st.multiselect(
#        "Selecciona Departamento", 
#        options=df_sm0["departamento"].unique(), 
#        default=df_sm0["departamento"].unique()
#    )
#    
#    Municipio = st.multiselect( 
#        "Selecciona Municipio", 
#        options=df_sm0["municipio"].unique(), 
#        default=df_sm0["municipio"].unique()
#    ) 
#    
#    Grupo = st.multiselect(
#        "Selecciona el Grupo de Enfermedad", 
#        options=df_sm0["grupo"].unique(), 
#        default=df_sm0["grupo"].unique()
#    )    


# ✅ Filtrar el dataframe según los valores seleccionados
#df_selection = df_sm0.query("departamento in @Departamento and municipio in @Municipio and grupo in @Grupo")

    

# ✅ Mostrar resultados
#st.write("Datos filtrados:", df_selection)
# ---------------------------------------------------------------------------
# Filtros visibles para el usuario, pero aún no se aplican
#Departamento = st.multiselect("Selecciona Departamento", df_sm0['departamento'].dropna().unique())
#Municipio = st.multiselect("Selecciona Municipio", df_sm0['municipio'].dropna().unique())
#Grupo = st.multiselect("Selecciona Grupo", df_sm0['grupo'].dropna().unique())

df_selection = df_sm1.copy()  # No se filtra todavía


# ----------------------------------------------------------------------------
# Asignación directa sin filtros interactivos
df_selection = df_sm1.copy()



# Secciones del dashboard
#if selected == "📊 KPI":

#st.subheader("KPI")
# calcular los Indicadores Clave de Morbilidad:
#total_investment = float(pd.Series(df_selection['Tot_Eventos']).sum())
#investment_mode1 = float(pd.Series(df_selection['departamento']).nunique())
#investment_mode2 = float(pd.Series(df_selection['municipio']).nunique())
#investment_median= float(pd.Series(df_selection['Enfermedad_Evento']).nunique()) 


#total1,total2,total3,total4,total5=st.columns(5,gap='small')
#with total1: 
#    st.info('Años', icon="📆") 
#    st.metric(label="Periodo", value="2018 - 2023")
#with total2:
#    st.info('Tot. Eventos',icon="🎯")
#    st.metric(label="Tot. Casos", value=f"{total_investment:,.0f}".replace(",", "."))
#with total3:
#    st.info('Tot. Dptos.',icon="🎯")
#    st.metric(label="Tot. Dptos.",value=f"{investment_mode1:,.0f}")

#with total4:
#    st.info('Tot. Municip.',icon="🎯")
#    st.metric(label="Tot. Municip.",value=f"{investment_mode2:,.0f}")

#with total5:
#    st.info('Tot. Grupo Enferm.',icon="🎯")
#    st.metric(label="Tot. Grupo",value=f"{investment_median:,.0f}")



#------------------------------------------------------------------------------






# ******

# ✅ Filtrar el dataframe según los valores seleccionados
df_selection = df_sm1.query("departamento in @Departamento and municipio in @Municipio and grupo in @Grupo")

    
#--------------------------------------------------------------------------- 
# Tabla de frecuencia de grupos de enfermedades de Salud Mental 
#---------------------------------------------------------------------------
# Mostrar tabla expandible con el conjunto de datos

def Home1(): 
    with st.expander("Ver el Conjunto de Datos en Excel"): 
        showData = st.multiselect(
            'Filter:', 
            df_selection.columns,
            default=["anio", "sexo", "nombre_cat_edad", "region","departamento", "municipio", 
                     "componente", "capitulo", "grupo", "Enfermedad_Evento", 
                     "pob10", "tasa_morb", "Tot_Eventos"], 
            key='SelectorMultiple'
            ) 
        st.dataframe(df_selection[showData], use_container_width=True)

# Hasta aqui se muestra el excel con la base original
# ---------------------------------------------------------------------









# Llamar la función antes del resumen tabular
Home1()

st.markdown("##")

st.markdown("<h4 style='color:#547FD4; font-weight:bold;'>Resumen Tabular del Número de Decesos Por Grupo de Enfermedades</h4>", unsafe_allow_html=True) 




# Convertir año a categórica 
df_sm1['anio'] = pd.to_numeric(df_sm1['anio'], errors='coerce') 

# Filtro para la region de la orinoquia 
df_sm1=df_sm1[df_sm1['region']=='Orinoquía'] 


# Reemplazar valores en la columna 'sexo' 
df_sm1['sexo'] = df_sm1['sexo'].replace({'Masculino': 'Hombres','Femenino': 'Mujeres'})


# Orden ctegorias de edad 
#orden_cat_edad = ['Primera infancia', 'Infancia', 'Adolescensia', 'Adultez Temprana', 'Adultez Media', 'Adultez Mayor'] 

# Convertir la columna 'nombre_cat_edad' a tipo categórico con orden 
#df0['nombre_cat_edad'] = pd.Categorical(df0['nombre_cat_edad'], categories=orden_cat_edad, ordered=True)
df_sm1['nombre_cat_edad'] = pd.Categorical(df_sm1['nombre_cat_edad'])
df_sm1['grupo'] = df_sm1['grupo'].str.strip() 
df_sm1['departamento']= df_sm1['departamento'].str.strip() 
df_sm1['departamento']=pd.Categorical(df_sm1['departamento']) 

df_sm1['anio'] = df_sm1['anio'].astype(str)   # esto va en contra de la septima línea de código hacia arriba

# Filtro para Salud Mental 
df1_sm = df_sm1[df_sm1['componente']=='Salud Mental']

# Tabla Pivote: 
df_agregada1 = df1_sm.groupby(['grupo']).count().reset_index() 
df_agregada1_1 = df_agregada1[['grupo', 'anio']] 
df_agregada1_1.columns = ['grupo', 'cant'] 

# Calcular el total de casos 
total_casos = df_agregada1_1['cant'].sum() 

# Agregar columna de porcentaje 
df_agregada1_1['(%)'] = (df_agregada1_1['cant'] / total_casos * 100).round(2) 

st.dataframe(df_agregada1_1) 
# ----------------------------------------------------------------------





st.markdown("##")   # SALTO





#------------------------------------------------------------------------- 

# 1. Crear los selectores para grupo de enfermedades y sexo

grupos_sm = df1_sm['grupo'].unique().tolist()
sexos = ['Todos'] + df1_sm['sexo'].dropna().unique().tolist()

st.markdown("<h5 style='font-weight:bold;'>Selecciona un grupo de enfermedades</h5>", unsafe_allow_html=True)
grupo_sm_sel = st.selectbox("Grupo", grupos_sm)

st.markdown("<h5 style='font-weight:bold;'>Selecciona el sexo</h5>", unsafe_allow_html=True)
sexo_sel = st.selectbox("Sexo", sexos)

# 2. Filtrar el DataFrame según las selecciones

df_sm_filtrado = df1_sm[df1_sm['grupo'] == grupo_sm_sel]

if sexo_sel != 'Todos':
    df_sm_filtrado = df_sm_filtrado[df_sm_filtrado['sexo'] == sexo_sel]

# 3. Agrupar los datos ya filtrados

df_sm_filtrado2 = df_sm_filtrado.groupby(
    ['anio', 'nombre_cat_edad', 'departamento']
)['anio'].count().reset_index(name='cant')




# ----------------------------------------------------------------------

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

# ---------------------------------------------------------------------





st.markdown("##")





    
# ----------------------------------------------------------------------
# Diagrama de lineas año y sexo: 
# ----------------------------- 
P_Colores = {"Azul_cl": "#39A8E0", 
             "Gris": "#9D9D9C", 
             "Verde": "#009640", 
             "Naranja": "#F28F1C", 
             "Azul_os": "#2A3180", 
             "Rojo": "#E5352B",
             "Morado":"#662681"} 

df1_sm['anio'] = pd.to_numeric(df1_sm['anio'], errors='coerce')  # convierte strings a números, NaNs si no puede 
a_min_sm = df1_sm['anio'].min() - 1 
a_max_sm = df1_sm['anio'].max()+1 
# -----------------------------------------------------------------------------










