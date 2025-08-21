



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
#st.header("MORTALIDAD:  Tratamiento Estadístico, KPI y Tendencias")



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

st.subheader("Indicadores Clave de Mortalidad")

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

st.subheader("Dataset")
# calcular los Indicadores Clave de Mortalidad:
total_investment = float(pd.Series(df_selection['Tot_Eventos']).sum())
investment_mode1 = float(pd.Series(df_selection['departamento']).nunique())
investment_mode2 = float(pd.Series(df_selection['municipio']).nunique())
investment_median= float(pd.Series(df_selection['Enfermedad_Evento']).nunique()) 


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
df1_sm = df_sm1[df_sm1['componente']=='SM']


# Tabla Pivote: 
df_agregada1 = df1_sm.groupby(['grupo']).count().reset_index() 
df_agregada1_1 = df_agregada1[['grupo', 'anio']] 
df_agregada1_1.columns = ['grupo', 'Tot_Eventos'] 

# Calcular el total de casos 
total_casos = df_agregada1_1['Tot_Eventos'].sum() 

# Agregar columna de porcentaje 
df_agregada1_1['(%)'] = (df_agregada1_1['Tot_Eventos'] / total_casos * 100).round(2) 

st.dataframe(df_agregada1_1) 
# ----------------------------------------------------------------------





st.markdown("##")   # SALTO





#------------------------------------------------------------------------- 

# 1. Crear los selectores para grupo de enfermedades y sexo

grupos_sm = df1_sm['grupo'].dropna().unique().tolist()
sexos = ['Todos'] + df1_sm['sexo'].dropna().unique().tolist()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧬 Grupo de Enfermedades")
    grupo_sm_sel = st.selectbox("Grupo", grupos_sm, key="grupo")

with col2:
    st.markdown("### ⚥ Sexo")
    sexo_sel = st.selectbox("Sexo", sexos, key="sexo")

# -------------------------------------------------------------------------
# 2. Filtrar el DataFrame según las selecciones

df_sm_filtrado = df1_sm[df1_sm['grupo'] == grupo_sm_sel]

if sexo_sel != 'Todos':
    df_sm_filtrado = df_sm_filtrado[df_sm_filtrado['sexo'] == sexo_sel]

# -------------------------------------------------------------------------
# 3. Agrupar los datos ya filtrados

df_sm_filtrado2 = df_sm_filtrado.groupby(
    ['anio', 'nombre_cat_edad', 'departamento']
)['anio'].count().reset_index(name='cant')

# -------------------------------------------------------------------------
# 4. Crear la tabla cruzada sumando la columna 'cant' 

tabla_sm2 = df_sm_filtrado2.pivot_table(
    values='cant', 
    index='nombre_cat_edad', 
    columns='departamento', 
    aggfunc='sum', 
    fill_value=0, 
    observed=False
)

# -------------------------------------------------------------------------
# 5. Mostrar la tabla en Streamlit

st.markdown("### 📊 Tabla cruzada: Total de Decesos por Rango de Edad")
st.dataframe(tabla_sm2)

# -------------------------------------------------------------------------





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




st.markdown("##")   # SALTO






# ----------------------------------------------------------------------------

st.markdown("##")

st.markdown("<h4 style='color:#547FD4; font-weight:bold;'>Tendencia Cronológica de Nro. de Eventos de Mortalidad</h4>", unsafe_allow_html=True) 



# 1. Crear un selector para que el usuario elija uno o varios grupos: 
deptos_sm = df1_sm['departamento'].unique().tolist() 
#depto_sm_sel = st.selectbox("Selecciona un Departamento", deptos_sm, key="sel_dpto_sm_mortalidad")
#st.markdown("<h5 style='font-weight:bold;'>Selecciona un Departamento</h5>", unsafe_allow_html=True) 
Dptos_sm_sel = st.selectbox("Selecciona un Departamento", deptos_sm)


df_sm_filtrado3 = df1_sm.groupby(['anio', 'sexo','nombre_cat_edad', 'departamento']).count().reset_index() 
df_sm_filtrado3_2 = df_sm_filtrado3[['anio','sexo', 'nombre_cat_edad', 'departamento', 'Tot_Eventos']] 
df_sm_filtrado3_2.columns = ['anio', 'sexo','nombre_cat_edad', 'departamento','cant'] 



df_sm_filtrado3_3 = df_sm_filtrado3_2[df_sm_filtrado3_2['departamento'] == Dptos_sm_sel] 
df0_sm3 = df_sm_filtrado3_3.groupby(['sexo','anio'])['cant'].sum().reset_index() 


# Crear gráfico de líneas con Plotly Express 
fig_sm = px.line(df0_sm3, x='anio', y='cant', color='sexo', markers=True, 
                 title="TENDENCIA DE EVENTOS DE MORTALIDAD",
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





    
# ---------------------------------------------------
#  GRÁFICOS DE CASCADA:
# ---------------------------------------------------


    
# Cargando las Librerías:
#import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go
import plotly.graph_objects as go

# Cargando las Librerías:
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# =====================================
# TITULO Y ESTILO DEL ENCABEZADO:
st.set_page_config(page_title="Dashboard ", page_icon="📈", layout="wide")  
st.header("Histórico del Total de Casos de Mortalidad por Grupo de Eventos")
st.markdown("##")

# Cargar estilos si existe
try:
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Archivo style.css no encontrado. Continuando sin estilos personalizados.")

# LLAMANDO EL DATAFRAME:
df_GrupoEnfer = pd.read_excel('Tabla_Grafico_Cascada_MORTALIDAD.xlsx', sheet_name='Hoja1')

# Cambiar round por parte entera
df_GrupoEnfer["Tot_Eventos"] = df_GrupoEnfer["Tot_Eventos"].astype(int)
df_GrupoEnfer["Tot_pob10"] = df_GrupoEnfer["Tot_pob10"].astype(int)

# =====================================
# FILTROS: Departamento y Año
if 'departamento' in df_GrupoEnfer.columns and 'anio' in df_GrupoEnfer.columns:

    # Filtro de departamento
    departamentos_disponibles = ['Todos los Dptos'] + sorted(df_GrupoEnfer['departamento'].unique().tolist())
    departamento_seleccionado = st.selectbox(
        "Selecciona el Departamento:",
        options=departamentos_disponibles,
        index=0
    )

    # Filtro de año
    anios_disponibles = sorted(df_GrupoEnfer['anio'].unique().tolist())
    anio_seleccionado = st.selectbox(
        "Selecciona el Año:",
        options=anios_disponibles,
        index=0
    )

    # Filtrar datos según selección
    if departamento_seleccionado == 'Todos los Dptos':
        df_filtrado = df_GrupoEnfer[df_GrupoEnfer['anio'] == anio_seleccionado] \
            .groupby('grupo').agg({
                'Tot_Eventos': 'sum',
                'Tot_pob10': 'sum'
            }).reset_index()
        titulo_grafico = f"Todos los Departamentos - {anio_seleccionado}"
    else:
        df_filtrado = df_GrupoEnfer[
            (df_GrupoEnfer['departamento'] == departamento_seleccionado) &
            (df_GrupoEnfer['anio'] == anio_seleccionado)
        ].copy()
        titulo_grafico = f"{departamento_seleccionado} - {anio_seleccionado}"

else:
    st.error("Faltan columnas 'departamento' o 'anio' en el DataFrame. Verifica el archivo.")
    st.write("Columnas disponibles:", df_GrupoEnfer.columns.tolist())
    df_filtrado = df_GrupoEnfer.copy()
    titulo_grafico = "Datos Generales"

# =====================================
# PREPARAR DATOS PARA EL GRÁFICO:
GrupoEnf = df_filtrado['grupo'].tolist()
y_list = df_filtrado['Tot_Eventos'].tolist()
x_list = GrupoEnf
Total = 'Total'
x_list = GrupoEnf + ['Total']
total = int(sum(y_list))
y_list.append(total)

# Formato miles
def formato_miles(valor):
    return f"{valor:,.0f}".replace(",", ".")

# Etiquetas con formato
text_list = []
for index, item in enumerate(y_list):
    texto = formato_miles(item)
    if index != 0 and index != len(y_list) - 1:
        texto = f'+{texto}'
    text_list.append(texto)

# Colores para texto
for index, item in enumerate(text_list):
    if item.startswith('+') and index != 0 and index != len(text_list) - 1:
        text_list[index] = f'<span style="color:#ff7f0e">{item}</span>'  # naranja
    elif item.startswith('-') and index != 0 and index != len(text_list) - 1:
        text_list[index] = f'<span style="color:#d62728">{item}</span>'
    if index == 0 or index == len(text_list) - 1:
        text_list[index] = f'<b>{item}</b>'

# =====================================
# CREAR EL GRÁFICO WATERFALL:
y_list_modified = y_list.copy()
measures = ["absolute"] + ["relative"] * (len(y_list) - 2) + ["absolute"]
y_list_modified[-1] = sum(y_list[:-1])  

fig = go.Figure(go.Waterfall(
    name="prevalencia", orientation="v",
    measure=measures,
    x=x_list,
    y=y_list_modified,
    text=text_list,
    textposition="outside",
    connector={"line":{"color":'rgba(0,0,0,0)'}},  # sin líneas punteadas
    increasing={"marker":{"color":"#ff7f0e"}},  # naranja
    decreasing={"marker":{"color":"#d62728"}},
    totals={'marker':{"color":"#9467bd"}},
    textfont={"family":"Open Sans", "color":"black"}
))

# Layout del gráfico
fig.update_layout(
    title={
        'text': f'<b>Waterfall Chart - {titulo_grafico}</b><br><span style="color:#666666">Prevalencia de Decesos por Enfermedades Mentales</span>',
        'x': 0.5,
        'xanchor': 'center'
    },
    showlegend=False,
    height=450,   # más pequeño
    font={'family':'Open Sans', 'color':'black', 'size':14},
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_title="Casos",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)

fig.update_xaxes(tickangle=-45, tickfont=dict(family='Open Sans', color='black', size=12))
fig.update_yaxes(tickangle=0, tickfont=dict(family='Open Sans', color='black', size=12))

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)

# =====================================
# INFORMACIÓN ADICIONAL:
if 'departamento' in df_GrupoEnfer.columns:
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Casos", value=f"{total:,}".replace(",", "."))
    
    with col2:
        if departamento_seleccionado != 'Todos los Dptos':
            st.metric("Departamento Seleccionado", value=departamento_seleccionado)
        else:
            st.metric("Departamentos Incluidos", value=len(df_GrupoEnfer['departamento'].unique()))
    
    with col3:
        st.metric("Grupos de Enfermedades", value=len(GrupoEnf))

















