



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
# Tabla de Datos para Morbilidad:
# -------------------------------

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

# Base de Referencia:
#-------------------



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






# SECCIÓN 1.1. : 
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

# ---------------------------------------------------------------------------
# Sección de Filtros – Ocultos pero definidos por defecto
# ---------------------------------------------------------------------------

# 🧩 Valores por defecto para los filtros (sin mostrarlos)
Departamento = df_sm0['departamento'].dropna().unique().tolist()
Municipio = df_sm0['municipio'].dropna().unique().tolist()
Grupo = df_sm0['grupo'].dropna().unique().tolist()

# ✅ DataFrame filtrado (en este caso sin aplicar restricciones)
df_selection = df_sm0[
    (df_sm0['departamento'].isin(Departamento)) &
    (df_sm0['municipio'].isin(Municipio)) &
    (df_sm0['grupo'].isin(Grupo))
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

df_selection = df_sm0.copy()  # No se filtra todavía


# ----------------------------------------------------------------------------
# Asignación directa sin filtros interactivos
df_selection = df_sm0.copy()



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
        st.info('Años', icon="📆") 
        st.metric(label="Periodo", value="2018 - 2023")
    with total2:
        st.info('Tot. Eventos',icon="🎯")
        st.metric(label="Tot. Casos", value=f"{total_investment:,.0f}".replace(",", "."))
    with total3:
        st.info('Tot. Dptos.',icon="🎯")
        st.metric(label="Tot. Dptos.",value=f"{investment_mode1:,.0f}")

    with total4:
        st.info('Tot. Municip.',icon="🎯")
        st.metric(label="Tot. Municip.",value=f"{investment_mode2:,.0f}")

    with total5:
        st.info('Tot. Grupo Enferm.',icon="🎯")
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




    
# ----------------------------------------------------------------------

# Llamar la función antes del resumen tabular
Home1()

st.markdown("##")

st.markdown("<h4 style='color:#547FD4; font-weight:bold;'>Resumen Tabular del grupo de Enfermedades</h4>", unsafe_allow_html=True) 

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
# ----------------------------------------------------------------------





st.markdown("##")   # SALTO





#------------------------------------------------------------------------- 

# Crear las listas de opciones
grupos_sm = df0_sm['grupo'].unique().tolist()
sexos = ['Todos'] + df0_sm['sexo'].dropna().unique().tolist()

# Crear dos columnas para los filtros en una misma línea
col1, col2 = st.columns([2, 1])  # Ajusta proporción si quieres que Grupo sea más ancho

with col1:
    st.markdown("<h5 style='font-weight:bold;'>Grupo de Enfermedades</h5>", unsafe_allow_html=True)
    grupo_sm_sel = st.selectbox("Grupo", grupos_sm, label_visibility="collapsed")

with col2:
    st.markdown("<h5 style='font-weight:bold;'>Sexo</h5>", unsafe_allow_html=True)
    sexo_sel = st.selectbox("Sexo", sexos, label_visibility="collapsed")

# Filtrar según selección
df_sm_filtrado = df0_sm[df0_sm['grupo'] == grupo_sm_sel]

if sexo_sel != 'Todos':
    df_sm_filtrado = df_sm_filtrado[df_sm_filtrado['sexo'] == sexo_sel]

# Agrupar los datos filtrados
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

df0_sm['anio'] = pd.to_numeric(df0_sm['anio'], errors='coerce')  # convierte strings a números, NaNs si no puede 
a_min_sm = df0_sm['anio'].min() - 1 
a_max_sm = df0_sm['anio'].max()+1 
# -----------------------------------------------------------------------------




st.markdown("##")   # SALTO






# ----------------------------------------------------------------------------

st.markdown("##")

st.markdown("<h4 style='color:#547FD4; font-weight:bold;'>Tendencia Cronológica de Nro. de Eventos de Morbilidad</h4>", unsafe_allow_html=True) 



# 1. Crear un selector para que el usuario elija uno o varios grupos: 
deptos_sm = df0_sm['departamento'].unique().tolist() 
#depto_sm_sel = st.selectbox("Selecciona un Departamento", deptos_sm, key="sel_dpto_sm_morbilidad")
#st.markdown("<h5 style='font-weight:bold;'>Selecciona un Departamento</h5>", unsafe_allow_html=True) 
Dptos_sm_sel = st.selectbox("Selecciona un Departamento", deptos_sm)


df_sm_filtrado3 = df0_sm.groupby(['anio', 'sexo','nombre_cat_edad', 'departamento']).count().reset_index() 
df_sm_filtrado3_2 = df_sm_filtrado3[['anio','sexo', 'nombre_cat_edad', 'departamento', 'Tot_Eventos']] 
df_sm_filtrado3_2.columns = ['anio', 'sexo','nombre_cat_edad', 'departamento','cant'] 



df_sm_filtrado3_3 = df_sm_filtrado3_2[df_sm_filtrado3_2['departamento'] == Dptos_sm_sel] 
df0_sm3 = df_sm_filtrado3_3.groupby(['sexo','anio'])['cant'].sum().reset_index() 


# Crear gráfico de líneas con Plotly Express 
fig_sm = px.line(df0_sm3, x='anio', y='cant', color='sexo', markers=True, 
                 title="TENDENCIA DE EVENTOS DE MORBILIDAD",
                 color_discrete_sequence=["#2A3180","#E5352B"]) 


# Personalizar marcadores para que tengan borde del color de la línea y fondo blanco 
fig_sm.update_traces( 
    marker=dict(size=10, 
                color='white',          # fondo blanco 
                line=dict(width=2)      # borde que tomará el color de la línea
                ))

# Ajustar eje x para mostrar todos los años y con rango fijo 
fig_sm.update_xaxes(dtick=1, range=[a_min_sm,a_max_sm], tickmode='linear') 

fig_sm.update_xaxes(title_text="") 
fig_sm.update_yaxes(title_text="Número de casos") 

st.plotly_chart(fig_sm, use_container_width=True)
# ---------------------------------------------------------------------





st.markdown("##")





    
# ----------------------------------------------------------------------
# TRES GRÁFICOS DE ANÁLISIS DE LA TASA DE MORBILIDAD:
# ---------------------------------------------------
st.markdown("##")

st.markdown("<h4 style='color:#547FD4; font-weight:bold;'>Tasas de Morbilidad</h4>", unsafe_allow_html=True) 


# Todos los gráficos se personalizan usando CSS , no Streamlit. 
theme_plotly = None 


# Cargar los estilo css:
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Descomenta estas dos líneas si obtienes datos de MySQL:
# result = view_all_data()
# df=pd.DataFrame(result,columns=["Policy","Expiry","Location","State","Investment","Construction","BusinessType","Earthquake","Flood","Rating","id"])

# cargar archivo Excel | comente esta línea cuando obtenga datos de MySQL:

# df = pd.read_excel("C:/Users/cesar/Downloads/TABLERO_STREAMLIT_DASHBOARD/DASHBOARD_Morbilidad_DESPLIEGUE/Tasas_Morbilidad.xlsx", sheet_name='Hoja1')    
# df = pd.read_excel('Tasas_Morbilidad_25MB.xlsx', sheet_name='Hoja1')
# COMO ESTA BASE YA ESTÁ DEFINIDA DESDE EL INICIO COMO df0, NO LA DEBO LLAMAR DE NUEVO, SOLO LA ASIGNO.
df = df0_sm

# Convirtiendo la columna Anio a Categórica:
    # Opción 2: Convertir a categórica (más eficiente)
df['anio'] = df['anio'].astype(str)
    
# ======================================================================



def safe_numerize(value):
    """Convierte un valor a formato numerize de forma segura"""
    try:
        # Manejar valores None o vacíos
        if value is None:
            return "0"
        
        # Convertir a string y limpiar
        str_value = str(value).strip().lower()
        if str_value in ['', 'nan', 'none', 'null']:
            return "0"
        
        # Convertir a número
        num_value = float(value)
        
        # Verificar si es NaN
        if num_value != num_value:  # NaN check sin pandas
            return "0"
        
        # Aplicar numerize
        return numerize(int(num_value))
        
    except (ValueError, TypeError, AttributeError):
        return "0"




#graphs
def graphs():
    investment_by_business_type=(
        df_selection.groupby(by=["anio"]).count()[["tasa_morb"]].sort_values(by="tasa_morb")
    )
    
    # Convertir el índice en una columna
    investment_by_business_type = investment_by_business_type.reset_index()
    
    # CORRECCIÓN: Usar 'tasa_morb' como y, no 'index'
    fig_investment = px.bar(
        investment_by_business_type,
        x="anio", 
        y="tasa_morb",  # ← Esta es la columna correcta
        title="Análisis de Morbilidad por Año", 
        color_discrete_sequence=["#0083B8"] * len(investment_by_business_type),
        template="plotly_white"
    )
    
    fig_investment.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),
     yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Mostrar la cuadrícula del eje y y establecer su color  
     paper_bgcolor='rgba(0, 0, 0, 0)',  # Establecer el color del fondo  en transparente
     xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Mostrar la cuadrícula del eje x y establecer su color
     )
    
    # gráfico de regresión lineal simple de inversión por nombre_cat_edad
    investment_state = df_selection.groupby(by=["nombre_cat_edad"]).count()[["tasa_morb"]]
    
    investment_state_reset = investment_state.reset_index()    
    
    fig_state = px.line(investment_state_reset, 
                   x="nombre_cat_edad",  # Categorías de edad en el eje X
                   y="tasa_morb",        # Conteo/tasa en el eje Y
                   orientation="v", 
                   title="<b> TASA DE MORBILIDAD POR CATEGORÍA DE EDADES </b>",
                   color_discrete_sequence=["#0083b8"]*len(investment_state_reset), 
                   template="plotly_white",
                   
    )
    
    fig_state.update_layout(
        xaxis=dict(tickmode="linear"), 
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False))
        )
    
    left,right,center=st.columns(3)
    left.plotly_chart(fig_state,use_container_width=True)
    right.plotly_chart(fig_investment,use_container_width=True)
    
    with center:
      #pie chart
      fig = px.pie(df_selection, values='tasa_morb', names='departamento', title="<b> TASA  MORBILIDAD POR DEPARTAMENTO </b>")
      fig.update_layout(legend_title="Dptos.", legend_y=0.9)
      fig.update_traces(textinfo='percent+label', textposition='inside')
      st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


# función para mostrar las ganancias actuales frente al objetivo esperado
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
    target=3000000000
    current=df_selection["Investment"].sum()
    percent=round((current/target*100))
    mybar=st.progress(0)

    if percent>100:
        st.subheader("Objetivo cumplido !")
    else:
     st.write("tienes ",percent, "% " ,"of ", (format(target, 'd')), "TZS")
     for percent_complete in range(percent):
        time.sleep(0.1)
        mybar.progress(percent_complete+1,text=" Objetivo Porcentual")

#menu bar
def sideBar():
 with st.sidebar:
    selected=option_menu(
        menu_title="Menú Principal",
        options=["Home","Progress"],
        icons=["house","eye"],
        menu_icon="cast",
        default_index=0
    )
 if selected=="Home":
    #st.subheader(f"Page: {selected}")
    graphs()
 if selected=="Progress":
    #st.subheader(f"Page: {selected}")
    Progressbar()
    graphs()


sideBar()

# ---------------------------------------------------------------------





st.markdown("##")
st.markdown("##")






    
# ------------------------------------------------------------------------
# CONSTRUCCIÓN DE UNA TABLA DE FRECUENCIA DE EVENTOS POR GRUPOS DE EDADES:
# -----------------------------------------------------------------------

st.markdown("##")

st.markdown("<h4 style='color:#547FD4; font-weight:bold;'>Casos de Morbilidad por Categoría de Edades y Regiones </h4>", unsafe_allow_html=True) 



import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Morbilidad",
    page_icon="📊",
    layout="wide"
)

# Cargar dataframe
@st.cache_data
def load_data3():
    df = pd.read_excel('Tasas_Morbilidad.xlsx', sheet_name='Hoja1')
    # Convertir año a categórica
    df['anio'] = df['anio'].astype(str)
    # Crear columna Periodo
    df['Periodo'] = df['anio']
    return df

df = load_data3()

# Sidebar con logo
#st.sidebar.image("data/logo1.png")

# Título principal
#st.title("📊 Análisis Comparativo de Morbilidad")

# === SECCIÓN 1: TABLA DE FRECUENCIAS ===
#st.header("📈 Tabla de Frecuencias por Categoría de Edad")
st.markdown("<h5 style='font-weight:bold;'>📈 Tabla de Frecuencias por Categoría de Edad</h5>", unsafe_allow_html=True)

# Calcular frecuencias
frequency = df.nombre_cat_edad.value_counts().sort_index()
percentage_frequency = frequency / len(df.nombre_cat_edad) * 100
cumulative_frequency = frequency.cumsum()
relative_frequency = frequency / len(df.nombre_cat_edad)
cumulative_relative_frequency = relative_frequency.cumsum()

# Crear tabla resumen
summary_table = pd.DataFrame({
    'Freq.': frequency,
    '% Freq.': percentage_frequency,
    'Freq. Acum.': cumulative_frequency,
    'Freq. Relat.': relative_frequency,
    'Freq. Relat. Acum.': cumulative_relative_frequency
})

# Selector de columnas para mostrar
showData = st.multiselect(
    "### FILTRO - Selecciona las columnas a mostrar:",
    summary_table.columns.tolist(),
    default=summary_table.columns.tolist(), 
    key='SeclMul2'
)

if showData:
    st.dataframe(summary_table[showData], use_container_width=True)
else:
    st.warning("Selecciona al menos una columna para mostrar")




st.markdown("##")




# === SECCIÓN 2: GRÁFICO INTERACTIVO ===
#st.header("📊 Frecuencia de Morbilidad por Departamento y Categoría de Edad")
st.markdown("<h5 style='font-weight:bold;'>📊 Frecuencia de Morbilidad por Departamento y Categoría de Edad </h5>", unsafe_allow_html=True)

# Crear columnas para los filtros
col1, col2 = st.columns(2)

with col1:
    # Dropdown para departamento (agregando opción "Todos")
    departamentos_options = ['Todos'] + list(df['departamento'].unique())
    departamento_selected = st.selectbox(
        "Selecciona departamento:",
        options=departamentos_options,
        index=0
    )

with col2:
    # Dropdown para categoría de edad (agregando opción "Todas")
    categorias_options = ['Todas'] + list(df['nombre_cat_edad'].unique())
    categoria_edad_selected = st.selectbox(
        "Selecciona categoría de edad:",
        options=categorias_options,
        index=0
    )

# Función para actualizar gráfico
def crear_grafico(departamento, nombre_cat_edad):
    # Filtrar datos según las selecciones
    df_filtrado = df.copy()
    
    # Aplicar filtro de departamento
    if departamento != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['departamento'] == departamento]
    
    # Aplicar filtro de categoría de edad
    if nombre_cat_edad != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['nombre_cat_edad'] == nombre_cat_edad]
    
    if df_filtrado.empty:
        st.warning(f"No hay datos para {departamento} - {nombre_cat_edad}")
        return None
    st.markdown("##")
    # Determinar título del gráfico
    if departamento == 'Todos' and nombre_cat_edad == 'Todas':
        titulo = 'Casos de Morbilidad - Todos los Departamentos y Categorías de Edad'
    elif departamento == 'Todos':
        titulo = f'Casos de Morbilidad - Todos los Departamentos - {nombre_cat_edad}'
    elif nombre_cat_edad == 'Todas':
        titulo = f'Casos de Morbilidad en {departamento} - Todas las Categorías de Edad'
    else:
        titulo = f'Casos de Morbilidad en {departamento} - {nombre_cat_edad}'
    
    # Agrupar datos
    if 'sexo' in df_filtrado.columns:
        # Si tienes columna de casos específica, úsala; si no, cuenta las filas
        if 'Enfermedad_Evento' in df_filtrado.columns:
            df_agg = df_filtrado.groupby(['Periodo', 'sexo'])['Enfermedad_Evento'].count().reset_index()
            y_column = 'Enfermedad_Evento'
        else:
            # Contar filas por grupo
            df_agg = df_filtrado.groupby(['Periodo', 'sexo']).size().reset_index(name='Tot_Eventos')
            y_column = 'Casos'
        df_agg = df_agg.sort_values(by='Periodo')
        
        # Crear gráfico con sexo
        fig = px.bar(
            df_agg, 
            x='Periodo', 
            y=y_column, 
            color='sexo',
            barmode='group',
            labels={y_column: 'Número de Casos', 'Periodo': 'Año'},
            color_discrete_map={'Masculino': '#2A3180', 'Femenino': '#39A8E0'},
            title=titulo
        )
        
    else:
        # Si no hay columna sexo, hacer gráfico simple
        if 'Enfermedad_Evento' in df_filtrado.columns:
            df_agg = df_filtrado.groupby('Periodo')['Enfermedad_Evento'].count().reset_index()
            y_column = 'Enfermedad_Evento'
        else:
            df_agg = df_filtrado.groupby('Periodo').size().reset_index(name='Casos')
            y_column = 'Casos'
        
        fig = px.bar(
            df_agg,
            x='Periodo',
            y=y_column,
            title=titulo,
            color_discrete_sequence=['#2A3180'],
            labels={y_column: 'Número de Casos', 'Periodo': 'Año'}
        )
    
    fig.update_layout(
        title_x=0.5,
        xaxis_tickangle=-45,
        height=500,
        margin=dict(l=60, r=30, t=60, b=80)
    )
    
    return fig

# Crear y mostrar gráfico
fig = crear_grafico(departamento_selected, categoria_edad_selected)

if fig:
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------





st.markdown("##")





    
# ------------------------------------------------------------------------
# GRÁFICO CIRCULAR DE SUBSECTORES:
# ---------------------------------

st.markdown("##")

st.markdown("<h4 style='color:#547FD4; font-weight:bold;'>Tasa de Morbilidad por Departamento </h4>", unsafe_allow_html=True) 
st.write("Da click en uno de los departamentos (en el centro del gráfico) para desplegar estadísticas") 



# Cargando las Librerías:
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go
import plotly.graph_objects as go

# =====================================
# TITULO Y ESTILO DEL ENCABEZADO:
st.set_page_config(page_title="Dashboard ", page_icon="📈", layout="wide")  
#st.header("Resumen Gráfico Exploratorio Multidimensional")
 
# Cargar CSS si existe el archivo
try:
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Archivo style.css no encontrado. Continuando sin estilos personalizados.")

# LLAMANDO EL DATAFRAME:
try:
    # Importando la tabla agregada con los resúmenes de las variables:
    df_subsectores = pd.read_excel('TablaMorbilidad_Subsectores.xlsx', sheet_name='Hoja1')
    df_subsectores["conteos"] = round(df_subsectores["conteos"], 0)
    df_subsectores["tasas"] = round(df_subsectores["tasas"], 1) 

    
    # Estructura jerárquica: País > Departamento > Enfermedad
    labels = df_subsectores['labels'].tolist()
    parents = df_subsectores['parents'].tolist()
    conteos = df_subsectores['conteos'].tolist()
    tasas = df_subsectores['tasas'].tolist()
    
    # Etiquetas personalizadas con conteo y tasa
    custom_labels = [f"{l}<br>Casos: {v:,.0f}<br>Tasa: {t:.1f}/10k".replace(',', '.') if v != 0 else l 
                 for l, v, t in zip(labels, conteos, tasas)]
    
    # Sunburst plot
    #colors = ['#2A3180', '#39A8E0', '#F28F1C', '#E5352B', '#662681', '#009640', '#9D9D9C']
    fig = go.Figure(go.Sunburst(
        labels=custom_labels,
        parents=parents,
        values=conteos,
        branchvalues="remainder" #,  # ahora los padres no necesitan tener suma directa
        #marker=dict(colors=colors * (len(labels) // len(colors) + 1))  # Repetir colores si son necesarios
    ))
    
    # Agregando el Titulo (Elegante)
    fig.update_layout(
        title={
            "text": "Enfermedades más Frecuentes por Departamento",
            "y": 0.95, 
            "x": 0.5, 
            "xanchor": "center", 
            "yanchor": "top", 
            "font": dict(size=24, color="black")
        }, 
        margin=dict(t=80, l=10, r=10, b=10)
    )
    
    
    
    # ¡AQUÍ ESTÁ LA LÍNEA QUE FALTABA!
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
except FileNotFoundError:
    st.error("Archivo 'TablaMorbilidad_Subsectores.xlsx' no encontrado. Verifica que el archivo esté en el directorio correcto.")
except Exception as e:
    st.error(f"Error al cargar los datos: {str(e)}")
    
 

# ---------------------------------------------------------------------





st.markdown("##")
st.markdown("##")




    
# ------------------------------------------------------------------------
# Diagrama TREE:
# ---------------------------------




# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar página
st.set_page_config(page_title="Dashboard ", page_icon="📈", layout="wide")
st.header("Diagrama Tree por Departamento, Grupo de Enfermedad, Sexo y Año")
st.markdown("###")

# 📥 Cargar los datos
population_df = pd.read_excel("Tabla_Morbilidad_TREE.xlsx", sheet_name='Hoja2')

# 📅 Filtro por Año
anios = sorted(population_df['anio'].unique())
#st.markdown("<h5 style='font-weight:bold;'>Selecciona el Año</h5>", unsafe_allow_html=True) 
anio_seleccionado = st.selectbox("Selecciona el Año", anios)

# 📊 Filtros horizontales
col1, col2 = st.columns(2)

# 📍 Filtro Departamento
departamentos = ["Total"] + sorted(population_df["Dptos"].dropna().unique())
with col1:
    #st.markdown("<h5 style='font-weight:bold;'>Selecciona el Departamento</h5>", unsafe_allow_html=True) 
    dpto_seleccionado = st.selectbox("Selecciona el Departamento", departamentos)

# 🚻 Filtro Sexo
sexos = ["Ambos sexos"] + sorted(population_df["sexo"].dropna().unique())
with col2:
    #st.markdown("<h5 style='font-weight:bold;'>Selecciona el Sexo</h5>", unsafe_allow_html=True)
    sexo_seleccionado = st.selectbox("Selecciona el Sexo", sexos)

# 🎯 Aplicar filtros
df_filtrado = population_df[population_df['anio'] == anio_seleccionado]

if dpto_seleccionado != "Total":
    df_filtrado = df_filtrado[df_filtrado["Dptos"] == dpto_seleccionado]

if sexo_seleccionado != "Ambos sexos":
    df_filtrado = df_filtrado[df_filtrado["sexo"] == sexo_seleccionado]

# 🌳 Crear el Treemap
fig = px.treemap(
    df_filtrado,
    path=['Dptos', 'GrupEnfer'],
    values='MorbTot',
    color='MorbTot',
    color_continuous_scale=["#c6dbef", "#6baed6", "#2171b5"],
)

# 🧾 Título dinámico
titulo = f"Morbilidad por Departamento y Grupo de Enfermedad - {anio_seleccionado}"
if dpto_seleccionado != "Total":
    titulo += f" | {dpto_seleccionado}"
if sexo_seleccionado != "Ambos sexos":
    titulo += f" | Sexo: {sexo_seleccionado}"

fig.update_layout(title=titulo)

# 📊 Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)
# ---------------------------------------------------------------------





st.markdown("##")
st.markdown("##")




    
# ------------------------------------------------------------------------








# ===========================
# Mapa Leaflet de Morbilidad:
# ---------------------------
#pip install streamlit-folium

import geopandas as gpd
import folium
import numpy as np



if selected == "📍 Mapa":

    st.markdown("## 🗺️ Mapa de Tasa de Morbilidad por Municipio")
    st.markdown("Este mapa muestra la tasa de morbilidad por cada municipio de la Orinoquía, de acuerdo con la tabla consolidada.")

    # 1. Cargar la tabla con tasas y el geopandas:
    # Leer shapefile
    gdf_municipios = gpd.read_file("/ciudades_shp/MGN_ADM_MPIO_GRAFICO.shp")

    df_tasas = pd.read_excel("/ciudades_shp/Tabla_Muni_Orinoquia_Mapas_Tasas.xlsx")
    
    # 2. Unir con geometrías por municipio
    gdf_merged = gdf_municipios.merge(df_tasas, on=["mpio_cdpmp"], how="left")

    # 3. Rellenar valores faltantes con 0 o NaN si se quiere ignorar
    gdf_merged['Tasa_Morbi'] = gdf_merged['Tasa_Morbi'].fillna(0)

    # 4. Crear el mapa base
    m = folium.Map(location=[4.5, -72.5], zoom_start=6.3, tiles="cartodb positron", control_scale=True)

    # 5. Agregar capa coroplética
    folium.Choropleth(
        geo_data=gdf_merged,
        name="Tasa de Morbilidad",
        data=gdf_merged,
        columns=["municipio", "Tasa_Morbi"],
        key_on="feature.properties.municipio",
        fill_color="Blues",  # Puedes cambiar a "YlGnBu", "BuPu", etc.
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Tasa de Morbilidad"
    ).add_to(m)

    # 6. Etiquetas emergentes con el valor de tasa
    for _, row in gdf_merged.iterrows():
        if row['geometry'] is not None and not pd.isna(row['Tasa_Morbi']):
            folium.Marker(
                location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
                popup=f"{row['municipio']}: {row['Tasa_Morbi']:.2f}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

    # 7. Mostrar el mapa en Streamlit
    from streamlit_folium import st_folium
    st_data = st_folium(m, width=1100, height=650)
