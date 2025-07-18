



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
<h1 style='text-align: center; color: #3A3A3A;'>📈 MORBILIDAD: Tratamiento Estadístico, KPI y Tendencias</h1>
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


#------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA:
#st.set_page_config(page_title="Salud Mental", layout="wide")
#st.header("Eventos de Morbilidad y Mortalidad, en Salud Mental")
#st.markdown("##")

# Base de Referencia:
#-------------------
df0 = pd.read_excel('Tasas_Morbilidad_25MB.xlsx', sheet_name='Hoja1')
df0['anio'] = df0['anio'].astype(str)



st.set_page_config(page_title="📊 Dashboard de Morbilidad", page_icon="🧠", layout="wide")



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
anio = st.sidebar.selectbox("Selecciona Año", options=["Todos"] + sorted(df0['anio'].dropna().unique().tolist()))  
departamento = st.sidebar.selectbox("Departamento", options=["Todos"] + sorted(df0['departamento'].dropna().unique().tolist()))
municipio = st.sidebar.selectbox("Municipio", options=["Todos"] + sorted(df0['municipio'].dropna().unique().tolist()))


# BASE DE DATOS:
# ----------------
# Aplicar filtros:
# ----------------
df_filtrado = df0.copy()
if departamento != "Todos":
    df_filtrado = df_filtrado[df_filtrado['departamento'] == departamento]
if municipio != "Todos":
    df_filtrado = df_filtrado[df_filtrado['municipio'] == municipio]
if anio:
    df_filtrado = df_filtrado[df_filtrado['anio'] == anio]
# -----------------------------



# Secciones del dashboard
if selected == "📊 KPI":
    st.subheader("Indicadores Clave de Morbilidad")
    col1, col2, col3 = st.columns(3)
    col1.metric("Casos Totales", numerize.numerize(df_filtrado["Tot_Eventos"].sum()), "↗︎")
    col2.metric("Tasa Promedio", f"{df_filtrado['tasa_morbilidad'].mean():.2f}")
    col3.metric("Número de Municipios", df_filtrado["municipio"].nunique())

    style_metric_cards(
        background_color="#F0F2F6",
        border_left_color="#0d6efd",
        border_color="#e6e6e6"
    )

elif selected == "📉 Tendencias":
    st.subheader("Tendencia Anual de la Tasa de Morbilidad")
    tendencia = df_filtrado.groupby('anio').mean(numeric_only=True).reset_index()
    fig = px.line(tendencia, x='anio', y='tasa_morbilidad', title='Tasa de Morbilidad Anual')
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
df0 = load_data1()



# ******














# -----------------------
# Tablas para Mortalidad:
# -----------------------
    
def load_data2():
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

df1 = load_data2()

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
    
    
    
    
    
    
    
    
    
    #------------------------------------------------------------------------- 
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
    
    
    st.markdown("##")   # SALTO
    
    
    # 1. Crear un selector para que el usuario elija uno o varios grupos: 
    deptos_sm = df0_sm['departamento'].unique().tolist() 
    #depto_sm_sel = st.selectbox("Selecciona un Departamento", deptos_sm, key="sel_dpto_sm_morbilidad")
    st.markdown("<h5 style='font-weight:bold;'>Selecciona un Departamento</h5>", unsafe_allow_html=True) 
    Dptos_sm_sel = st.selectbox("Selecciona Un Departamento", deptos_sm)
    
    
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
    #-----------------------------------------------------------------------------
    
    # **********************************************************************************
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
    #st.sidebar.image("data/Logo_UNILLANOS.png",caption="")      # LOGO
    #st.sidebar.image("Logo_UNILLANOS.png",caption="")            # LOGO
    
    
    
    #st.subheader('Seleccione Atributos para Observar Tendencias de Distrib. Por Cuartiles',)
    #feature_x = st.selectbox('Select feature for x Qualitative data', df_selection.select_dtypes("object").columns)
    #feature_y = st.selectbox('Seleccionar función para (Y) Datos cuantitativos', df_selection.select_dtypes("number").columns)
    #fig2 = go.Figure(
    #    data=[go.Box(x=df['grupo'], y=df[feature_y])],
    #    layout=go.Layout(
    #        title=go.layout.Title(text="Distribución Numérica, por Grupo de Enfermedades"),
    #        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
    #        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
    #        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
    #        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
    #        font=dict(color='#cecdcd'),  # Set text color to black
    #    )
    #)
    # Display the Plotly figure using Streamlit
    #st.plotly_chart(fig2,use_container_width=True)
    
    
    
    #theme
    hide_st_style=""" 
    
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    </style>
    """
    
    
    
    
    
    
    
    
    
    
    
    
    
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")
    





    
    
    
    
    
    
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
    st.title("📊 Análisis Comparativo de Morbilidad")
    
    # === SECCIÓN 1: TABLA DE FRECUENCIAS ===
    st.header("📈 Tabla de Frecuencias por Categoría de Edad")
    
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
    
    # === SECCIÓN 2: GRÁFICO INTERACTIVO ===
    st.header("📊 Frecuencia de Morbilidad por Departamento y Categoría de Edad")
    
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
    
    # === SECCIÓN 3: INFORMACIÓN ADICIONAL ===
    st.header("ℹ️ Información del Dataset")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Registros", f"{len(df):,}")
    
    with col2:
        st.metric("Departamentos", f"{df['departamento'].nunique()}")
    
    with col3:
        st.metric("Categorías de Edad", f"{df['nombre_cat_edad'].nunique()}")
    
    # Mostrar vista previa del dataset
    with st.expander("🔎 Ver Vista Previa del Dataset"):
        st.dataframe(df.head(), use_container_width=True)
    
    # Información sobre las columnas
    with st.expander("📋 Información de Columnas"):
        st.write("**Columnas disponibles en el dataset:**")
        for i, col in enumerate(df.columns, 1):
            st.write(f"{i}. **{col}** - Tipo: {df[col].dtype}")
    
    ##3
    
    
    
    
    
    
    
    
    
    
    
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")
    
    
    
    
    
    
    
    
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
    st.header("Resumen Gráfico Exploratorio Multidimensional")
    st.markdown("##")
     
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
                "font": dict(size=34, family="Agency FB", color="black")
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
        
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")
    
    
    
    
    
    
    
    # Diagrama TREE:
    # =============
    import streamlit as st
    import plotly.express as px
    import pandas as pd
    
    
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
    st.header("Diagrama Tree por Departamento, Grupo de Enfermedad y Año")
    st.markdown("##")
    
    # Carga de datos
    # Importando la tabla agregada con los resúmenes de las variables:
    population_df = pd.read_excel("Tabla_Morbilidad_TREE.xlsx", sheet_name='Hoja1')
    
    # Filtrar años disponibles
    anios = sorted(population_df['anio'].unique())
    anio_seleccionado = st.selectbox("Selecciona el Año", anios)
    
    # Filtrar por año
    df_filtrado = population_df[population_df['anio'] == anio_seleccionado]
    
    # Crear Treemap
    fig = px.treemap(
        df_filtrado,
        path=['Dptos', 'GrupEnfer'],
        values='MorbTot',
        color='MorbTot',
        color_continuous_scale=["red", "orange", "green"],
        title=f'Morbilidad Total por Departamento y Grupo de Enfermedad - {anio_seleccionado}'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")
    
    
    
    
    
    
    
    import streamlit as st
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    
    # =====================================
    # CONFIGURACIÓN DE PÁGINA
    st.set_page_config(page_title="Pirámide Poblacional", page_icon="👥", layout="wide")
    st.header("Pirámide Poblacional por Departamento y Año")
    st.markdown("##")
    
    # Definición de la paleta de colores
    P_Colores = {
        "Azul_cl": "#39A8E0",
        "Gris": "#9D9D9C",
        "Verde": "#009640",
        "Naranja": "#F28F1C",
        "Azul_os": "#2A3180",
        "Rojo": "#E5352B",
        "Morado": "#662681"
    }
    
    # =====================================
    # FUNCIONES
    
    def lectura_frec_dataframe(df0):
        """
        Procesa un DataFrame que ya está cargado en memoria
        """
        orden_rangos_edad = ['0 - 4','5 - 9','10 - 14','15 - 19','20 - 24','25 - 29' ,'30 - 34', '35 - 39',
                            '40 - 44', '45 - 49','50 - 54', '55 - 59', '60 - 64', '65 - 69', '70 - 74' ,'75 - 79', '80 - 84', '85 - 89']
        
        # Convert 'rango_edad' column to a categorical type with the specified order
        df0['rango_edad'] = pd.Categorical(df0['rango_edad'], categories=orden_rangos_edad, ordered=True)
        
        # Sort the DataFrame by the ordered 'rango_edad'
        df0 = df0.sort_values('rango_edad')
        
        # Se reestructura la base para disponer valores de H y M en columnas
        df = df0.pivot_table(index=['anio','region', 'departamento', 'rango_edad'],
                            columns='sexo', values='pob', observed=False).reset_index()
        df = df.rename_axis(None, axis=1)
        df['Total'] = df['Femenino'] + df['Masculino']
        df.rename(columns={'Femenino':'Mujeres','Masculino':'Hombres'}, inplace=True)
        
        return df
    
    def graficar_piramide(df, dpto, año):
        """
        Genera una pirámide poblacional usando matplotlib
        """
        df_filtered = df.copy()
    
        if dpto != "Todos":
            df_filtered = df_filtered[df_filtered["departamento"] == dpto]
    
        if año != "Todos":
            df_filtered = df_filtered[df_filtered["anio"] == año]
    
        # Agrupar datos
        df_plot = df_filtered.groupby("rango_edad", observed=False)[["Hombres", "Mujeres"]].sum().reset_index()
    
        # Calculate percentages
        df_plot['Total_age_group'] = df_plot['Hombres'] + df_plot['Mujeres']
        total = df_plot['Total_age_group'].sum()
        df_plot['Hombres_pct'] = (df_plot['Hombres'] / total) * 100
        df_plot['Mujeres_pct'] = (df_plot['Mujeres'] / total) * 100
    
        # Calcular límites
        Lim_h = df_plot['Hombres_pct'].max()
        Lim_m = df_plot['Mujeres_pct'].max()
        Lim = max(Lim_h, Lim_m)
        Lim = np.floor(Lim) + 3
    
        # Recalcular columnas necesarias para la pirámide
        df_plot["Female_Left"] = 0
        df_plot["Female_Width"] = df_plot["Mujeres_pct"]
        df_plot["Male_Left"] = -df_plot["Hombres_pct"]
        df_plot["Male_Width"] = df_plot["Hombres_pct"]
    
        # Colores
        Col_M = P_Colores.get('Rojo')
        Col_H = P_Colores.get('Azul_os')
        
        # Create the figure
        plt.style.use("fivethirtyeight")
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Crear las barras
        ax.barh(df_plot["rango_edad"], df_plot["Female_Width"], color=Col_M, label="Mujeres")
        ax.barh(df_plot["rango_edad"], df_plot["Male_Width"], left=df_plot["Male_Left"], color=Col_H, label="Hombres")
    
        # Agregar etiquetas de porcentaje
        for idx in range(len(df_plot)):
            ax.text(df_plot["Male_Left"].iloc[idx] - 0.1, idx, f"{df_plot['Hombres_pct'].iloc[idx]:.1f}%", 
                    ha="right", va="center", fontsize=10, color=Col_H, fontweight="bold")
            ax.text(df_plot["Female_Width"].iloc[idx] + 0.1, idx, f"{df_plot['Mujeres_pct'].iloc[idx]:.1f}%", 
                    ha="left", va="center", fontsize=10, color=Col_M, fontweight="bold")
    
        # Configuración del gráfico
        Lim_int = int(Lim)
        ax.set_xlim(-Lim, Lim)
        ax.set_xticks([])  # Omitir las etiquetas del eje x
        ax.set_ylabel("Rango de Edad", fontsize=14)
    
        # Título dinámico
        title = f"Pirámide Poblacional - {dpto}"
        if año != "Todos":
            title += f" ({año})"
        ax.set_title(title, fontsize=16, fontweight="bold", pad=20)
    
        ax.grid(False)
        ax.legend(loc='upper right', fontsize=12)
        
        plt.tight_layout()
        return fig
    
    # =====================================
    # CARGA DE DATOS
    
    try:
        # Lectura de la base desde la carpeta
        df0 = pd.read_csv('Poblacion_prm.csv', sep=';')
        
        # Procesar datos
        orden_rangos_edad = ['0 - 4','5 - 9','10 - 14','15 - 19','20 - 24','25 - 29' ,'30 - 34', '35 - 39',
                            '40 - 44', '45 - 49','50 - 54', '55 - 59', '60 - 64', '65 - 69', '70 - 74' ,'75 - 79', '80 - 84', '85 - 89']
        
        df0['rango_edad'] = pd.Categorical(df0['rango_edad'], categories=orden_rangos_edad, ordered=True)
        df0 = df0.sort_values('rango_edad')
        
        # Usar la función para procesar los datos
        df = lectura_frec_dataframe(df0)
        
        # =====================================
        # CONTROLES DE STREAMLIT
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Dropdown de departamentos
            departamento = sorted(df["departamento"].unique().tolist())
            departamento.insert(0, "Todos")
            dpto_seleccionado = st.selectbox("Seleccione Departamento:", departamento)
        
        with col2:
            # Dropdown de año
            año = sorted(df["anio"].unique().tolist())
            año.insert(0, "Todos")
            año_seleccionado = st.selectbox("Seleccione Año:", año)
        
        # =====================================
        # GENERAR Y MOSTRAR GRÁFICO
        
        if st.button("Generar Pirámide") or True:  # Se actualiza automáticamente
            with st.spinner("Generando pirámide poblacional..."):
                fig = graficar_piramide(df, dpto_seleccionado, año_seleccionado)
                st.pyplot(fig)
        
        # =====================================
        # INFORMACIÓN ADICIONAL
        
        # Mostrar estadísticas
        df_filtered = df.copy()
        if dpto_seleccionado != "Todos":
            df_filtered = df_filtered[df_filtered["departamento"] == dpto_seleccionado]
        if año_seleccionado != "Todos":
            df_filtered = df_filtered[df_filtered["anio"] == año_seleccionado]
        
        total_poblacion = df_filtered[["Hombres", "Mujeres"]].sum().sum()
        total_hombres = df_filtered["Hombres"].sum()
        total_mujeres = df_filtered["Mujeres"].sum()
        
        st.markdown("---")
        st.subheader("Estadísticas Resumidas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Población Total", f"{total_poblacion:,.0f}".replace(',', '.'))
        
        with col2:
            st.metric("Hombres", f"{total_hombres:,.0f}".replace(',', '.'), 
                     f"{(total_hombres/total_poblacion*100):.1f}%")
        
        with col3:
            st.metric("Mujeres", f"{total_mujeres:,.0f}".replace(',', '.'), 
                     f"{(total_mujeres/total_poblacion*100):.1f}%")
    
    except FileNotFoundError:
        st.error("❌ Archivo 'Poblacion_prm.csv' no encontrado. Verifica que el archivo esté en el directorio correcto.")
        
        # Mostrar datos de ejemplo
        st.info("📊 Mostrando pirámide de ejemplo:")
        
        # Crear datos de ejemplo
        np.random.seed(42)
        rangos_edad = ['0 - 4','5 - 9','10 - 14','15 - 19','20 - 24','25 - 29' ,'30 - 34', '35 - 39',
                       '40 - 44', '45 - 49','50 - 54', '55 - 59', '60 - 64', '65 - 69', '70 - 74' ,'75 - 79', '80 - 84', '85 - 89']
        
        ejemplo_data = []
        for rango in rangos_edad:
            hombres = np.random.randint(50000, 150000)
            mujeres = np.random.randint(50000, 150000)
            ejemplo_data.append({
                'anio': 2023,
                'region': 'Ejemplo',
                'departamento': 'Ejemplo',
                'rango_edad': rango,
                'Hombres': hombres,
                'Mujeres': mujeres,
                'Total': hombres + mujeres
            })
        
        df_ejemplo = pd.DataFrame(ejemplo_data)
        fig_ejemplo = graficar_piramide(df_ejemplo, "Ejemplo", 2023)
        st.pyplot(fig_ejemplo)
    
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {str(e)}")
        st.info("Verifica que el archivo CSV tenga las columnas correctas: anio, region, departamento, rango_edad, sexo, pob")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")
    
    
    
    
    
    
    
    
    
    
    
    
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
    st.header("Resumen del Total de Casos por cada Grupo de Eventos")
    st.markdown("##")
    
    # Cargar La base:  Tabla_Grafico_Cascada
    try:
        with open('style.css') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Archivo style.css no encontrado. Continuando sin estilos personalizados.")
    
    # LLAMANDO EL DATAFRAME:
    # Importando la tabla agregada con los resúmenes de las variables:
    df_GrupoEnfer = pd.read_excel('Tabla_Grafico_Cascada.xlsx', sheet_name='Hoja1')
    
    # Cambiar round por parte entera
    df_GrupoEnfer["TotCasos"] = df_GrupoEnfer["TotCasos"].astype(int)
    df_GrupoEnfer["Tot_pob10"] = df_GrupoEnfer["Tot_pob10"].astype(int)
    
    # =====================================
    # FILTRO POR DEPARTAMENTO:
    # Asumiendo que existe una columna 'departamento' en el DataFrame
    # Si la columna tiene otro nombre, cambia 'departamento' por el nombre correcto
    
    # Verificar si existe la columna departamento
    if 'departamento' in df_GrupoEnfer.columns:
        departamentos_disponibles = ['Todos los Dptos'] + sorted(df_GrupoEnfer['departamento'].unique().tolist())
        
        # Crear el selectbox para filtrar por departamento
        departamento_seleccionado = st.selectbox(
            "Selecciona el Departamento:",
            options=departamentos_disponibles,
            index=0
        )
        
        # Filtrar los datos según la selección
        if departamento_seleccionado == 'Todos los Dptos':
            # Agregar datos por grupo para todos los departamentos
            df_filtrado = df_GrupoEnfer.groupby('grupo').agg({
                'TotCasos': 'sum',
                'Tot_pob10': 'sum'
            }).reset_index()
            titulo_grafico = "Todos los Departamentos"
        else:
            # Filtrar por departamento específico
            df_filtrado = df_GrupoEnfer[df_GrupoEnfer['departamento'] == departamento_seleccionado].copy()
            titulo_grafico = departamento_seleccionado
    else:
        st.error("La columna 'departamento' no existe en el DataFrame. Por favor verifica el nombre correcto de la columna.")
        st.write("Columnas disponibles:", df_GrupoEnfer.columns.tolist())
        # Usar todos los datos si no existe la columna departamento
        df_filtrado = df_GrupoEnfer.copy()
        titulo_grafico = "Datos Generales"
    
    # =====================================
    # PREPARAR DATOS PARA EL GRÁFICO:
        
    GrupoEnf = df_filtrado['grupo'].tolist()
    y_list = df_filtrado['TotCasos'].tolist()
    x_list = GrupoEnf
    Total = 'Total'
    x_list = GrupoEnf + ['Total']  # Esta línea agrega el valor de la variable total al final de la lista x_list.
    total = int(sum(y_list))  # Cambiar round por int
    y_list.append(total)  # Esta línea agrega el valor de la variable total al final de la lista y_list.
    
    # Función para formato con punto de miles
    def formato_miles(valor):
        return f"{valor:,.0f}".replace(",", ".")
    
    # Preparar texto con formato miles y color HTML
    text_list = []
    for index, item in enumerate(y_list):
        texto = formato_miles(item)
        if index != 0 and index != len(y_list) - 1:
            texto = f'+{texto}'
        text_list.append(texto)
    
    
    # Aplicar formato de color a las etiquetas
    for index, item in enumerate(text_list):
        if item.startswith('+') and index != 0 and index != len(text_list) - 1:
            text_list[index] = f'<span style="color:#2ca02c">{item}</span>'
        elif item.startswith('-') and index != 0 and index != len(text_list) - 1:
            text_list[index] = f'<span style="color:#d62728">{item}</span>'
        if index == 0 or index == len(text_list) - 1:
            text_list[index] = f'<b>{item}</b>'
    
    
    
    # Crear líneas de cuadrícula
    dict_list = []
    max_value = max(y_list) if y_list else 1200
    step = max(200, int(max_value / 6))  # Ajustar el paso según el valor máximo
    for i in range(0, int(max_value * 1.2), step):
        dict_list.append(dict(
                type="line",
                line=dict(
                     color="#666666",
                     dash="dot"
                ),
                x0=-0.5,
                y0=i,
                x1=len(x_list),
                y1=i,
                line_width=1,
                layer="below"))
    
    # =====================================
    # CREAR EL GRÁFICO WATERFALL:
    
    # Método alternativo: Crear el gráfico con absolute para el total
    # Modificar la lista de medidas para que el Total sea absolute
    y_list_modified = y_list.copy()
    measures = ["absolute"] + ["relative"] * (len(y_list) - 2) + ["absolute"]
    
    # Para el total, usar el valor real en lugar del acumulado
    y_list_modified[-1] = sum(y_list[:-1])  # El total real sin duplicar
    
    fig = go.Figure(go.Waterfall(
        name = "prevalencia", orientation = "v",
        measure = measures,
        x = x_list,
        y = y_list_modified,
        text = text_list,
        textposition = "outside",
        connector = {"line":{"color":'rgba(0,0,0,0)'}},
        increasing = {"marker":{"color":"#2ca02c"}},
        decreasing = {"marker":{"color":"#d62728"}},
        totals={'marker':{"color":"#9467bd"}},
        textfont={"family":"Open Sans, light",
                  "color":"black"
                 }
    ))
    
    # Actualizar el layout del gráfico
    fig.update_layout(
        title = {
            'text': f'<b>Waterfall Chart - {titulo_grafico}</b><br><span style="color:#666666">Prevalencia de Enfermedades Mentales de 2013 a 2014</span>',
            'x': 0.5,
            'xanchor': 'center'
        },
        showlegend = False,
        height=650,
        font={
            'family':'Open Sans, light',
            'color':'black',
            'size':14
        },
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Casos",
        shapes=dict_list,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    
    
    # Fuente de las etiquetas:
    fig.update_xaxes(tickangle=-45, tickfont=dict(family='Open Sans, light', color='black', size=14))
    fig.update_yaxes(tickangle=0, tickfont=dict(family='Open Sans, light', color='black', size=14))
    
    # =====================================
    # MOSTRAR EL GRÁFICO:
    st.plotly_chart(fig, use_container_width=True)
    
    # =====================================
    # INFORMACIÓN ADICIONAL (OPCIONAL):
    if 'departamento' in df_GrupoEnfer.columns:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Total de Casos",
                value=f"{total:,}".replace(",", ".")
            )
        
        with col2:
            if departamento_seleccionado != 'Todos los Dptos':
                st.metric(
                    label="Departamento Seleccionado",
                    value=departamento_seleccionado
                )
            else:
                st.metric(
                    label="Departamentos Incluidos",
                    value=len(df_GrupoEnfer['departamento'].unique())
                )
        
        with col3:
            st.metric(
                label="Grupos de Enfermedades",
                value=len(GrupoEnf)
            )
    
    
    

   
    
   
    
##3






















# *************************************************************************
# *************************************************************************
# *************************************************************************
# *************************************************************************
# *************************************************************************
# *************************************************************************
# *************************************************************************




# ***********************
# SECCIÓN DE MORTALIDAD:
# ----------------------

# Contenido de la primera pestaña
with Tab2:
    st.header("MORTALIDAD:  Tratamiento Estadístico, KPI y Tendencias")
    st.write(" La mortalidad se refiere a la cantidad de muertes ocurridas en una población durante un período específico. Desde una perspectiva estadística, el análisis de la mortalidad permite comprender el impacto de distintas causas de defunción sobre la salud pública, así como identificar grupos poblacionales en mayor riesgo o vulnerabilidad.  Mediante indicadores como el número absoluto de muertes, la tasa bruta de mortalidad (por cada 10.000 habitantes), la tasa de mortalidad específica por edad, sexo o causa, es posible evaluar la carga de mortalidad y su distribución geográfica y temporal. Este análisis facilita la detección de patrones, tendencias y desigualdades en las causas de muerte, contribuyendo a priorizar acciones de prevención, fortalecer los sistemas de salud y diseñar políticas públicas basadas en evidencia. En conjunto, el estudio estadístico de la mortalidad es esencial para monitorear el estado de salud de una población, evaluar intervenciones sanitarias y reducir el impacto de enfermedades prevenibles.") 
    df_sm=df1[df1['componente']=='Salud Mental']
    
    
    st.markdown("##")
    


    st.markdown("<h4 style='color:#547FD4; font-weight:bold;'>Resumen Tabular del grupo de Enfermedades, en Reporte de Mortalidad:</h4>", unsafe_allow_html=True)
    
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
    
    
    
    st.markdown("##")   # SALTO
    
    
    
    #---------------------------------------------------------------------------
    
    # 1. Crear un selector para que el usuario elija uno o varios grupos
    grupos_sm = df_sm['grupo'].unique().tolist()
    #grupo_sm_sel = st.selectbox("Selecciona un grupo de enfermedad", grupos_sm)
    st.markdown("<h5 style='font-weight:bold;'>Selecciona un grupo de enfermedad</h5>", unsafe_allow_html=True) 
    grupo_sm_sel = st.selectbox("", grupos_sm)
    
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
    
    
    
    st.markdown("##")   #SALTO
    
    
    
    
    # 1. Crear un selector para que el usuario elija uno o varios grupos
    deptos_sm = df_sm['departamento'].unique().tolist()
    #depto_sm_sel = st.selectbox("Selecciona un departamento", deptos_sm, key = "sel_dpto_sm_mortalidad")
    st.markdown("<h5 style='font-weight:bold;'>Selecciona un departamento</h5>", unsafe_allow_html=True) 
    depto_sm_sel = st.selectbox("", deptos_sm)
    
    df_sm_filtrado2=df_sm_filtrado[df_sm_filtrado['departamento']==Dptos_sm_sel]
    
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
    





