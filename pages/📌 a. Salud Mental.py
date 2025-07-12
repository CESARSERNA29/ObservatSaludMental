# Cargando las Librerías:
# ======================

import streamlit as st
import pandas as pd
# from pandas_profiling import ProfileReport
import streamlit.components.v1 as components
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
    orden_cat_edad = ['Primera infancia', 'Infancia', 'Adolescensia', 
                      'Adultez Temprana', 'Adultez Media', 'Adultez Mayor']
    # Convertir la columna 'nombre_cat_edad' a tipo categórico con orden
    df0['nombre_cat_edad'] = pd.Categorical(df0['nombre_cat_edad'], 
                               categories=orden_cat_edad, ordered=True)
    df0['grupo'] = df0['grupo'].str.strip()  
    df0['departamento']=df0['departamento'].str.strip()
    df0['departamento']=pd.Categorical(df0['departamento'])
    
    df0['anio'] = df0['anio'].astype(str)
    
    #df_agregada = df.groupby(['componente','departamento','municipio',
    #                       'grupo','Enfermedad_Evento', 'sexo',
    #                       'nombre_cat_edad','anio'])['cant'].sum().reset_index()
    return df0  
df0 = load_data()








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
st.sidebar.image("data/logo1.png")
#-------------------------------------------------------------------------------






# ==========================================================
# Creacion de pestañas para cada componente del obsevatorio
# ==========================================================
Tab1, Tab2 = st.tabs(["Morbilidad", "Mortalidad"])

# Contenido de la primera pestaña
with Tab1:
    st.header("MORBILIDAD:  Tratamiento Estadístico, KPI y Tendencias")
    st.write("La morbilidad es la frecuencia o proporción de personas que presentan una enfermedad o condición específica dentro de una población determinada. Desde un enfoque estadístico, el análisis de la morbilidad permite identificar patrones, tendencias y distribuciones geográficas o demográficas de las enfermedades, lo cual es clave para la planificación en salud pública. Mediante indicadores como el número de casos absolutos, la tasa de morbilidad (por cada 10.000 habitantes) o la prevalencia y la incidencia, se pueden evaluar los grupos más afectados, detectar zonas de mayor vulnerabilidad y priorizar recursos. Estas métricas también permiten comparar el comportamiento de enfermedades a lo largo del tiempo o entre regiones, facilitando la toma de decisiones basadas en evidencia.  El análisis estadístico de la morbilidad es, por tanto, una herramienta fundamental para monitorear el estado de salud de una población, y diseñar intervenciones efectivas.") 
    df_sm0=df0[df0['componente']=='SM']
    
    
    st.markdown("##")
    
    
    #--------------------------------------------------------------------------- 
    # Tabla de frecuencia de grupos de enfermedades de Salud Mental 
    #---------------------------------------------------------------------------    
    st.markdown("<h4 style='color:#547FD4; font-weight:bold;'>Resumen Tabular del grupo de Enfermedades:</h4>", unsafe_allow_html=True)  
    
    # Crear tabla de frecuencia por grupo, departamento y grupo de edad:
    #df = pd.read_excel(r"C:\Users\cesar\Downloads\TABLERO_STREAMLIT_DASHBOARD\DASHBOARD_Morbilidad_DESPLIEGUE_2\Tasas_Morbilidad_25MB.xlsx", sheet_name='Hoja1') 
    #df0 = df 
    
    # Convertir año a categórica 
    df0['anio'] = pd.to_numeric(df0['anio'], errors='coerce') 
    
    # Filtro para la region de la orinoquia 
    df0=df0[df0['region']=='Orinoquía'] 
    
    
    # Reemplazar valores en la columna 'sexo' 
    df0['sexo'] = df0['sexo'].replace({'Masculino': 'Hombres','Femenino': 'Mujeres'})
    
    
    # Orden ctegorias de edad 
    orden_cat_edad = ['Primera infancia', 'Infancia', 'Adolescensia', 'Adultez Temprana', 'Adultez Media', 'Adultez Mayor'] 
    
    # Convertir la columna 'nombre_cat_edad' a tipo categórico con orden 
    df0['nombre_cat_edad'] = pd.Categorical(df0['nombre_cat_edad'], categories=orden_cat_edad, ordered=True) 
    df0['grupo'] = df0['grupo'].str.strip() 
    df0['departamento']=df0['departamento'].str.strip() 
    df0['departamento']=pd.Categorical(df0['departamento']) 
    
    df0['anio'] = df0['anio'].astype(str)
    
    # Filtro para Salud Mental 
    df0_sm=df0[df0['componente']=='Salud Mental']
    
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
    
    # 1. Crear un selector para que el usuario elija uno o varios grupos 
    
    grupos_sm = df0_sm['grupo'].unique().tolist() 
    # grupo_sm_sel = st.selectbox("Selecciona un grupo de enfermedad", grupos_sm)
    st.markdown("<h5 style='font-weight:bold;'>Selecciona un grupo de enfermedad</h5>", unsafe_allow_html=True) 
    grupo_sm_sel = st.selectbox("", grupos_sm)
    
    # 2. Filtrar el DataFrame según la selección del usuario 
    df_sm_filtrado = df0_sm[df0_sm['grupo'] == grupo_sm_sel] 
    df_sm_filtrado2 = df0_sm.groupby(['anio','nombre_cat_edad', 'departamento']).count().reset_index()
    df_sm_filtrado2 = df0_sm.groupby(['anio','nombre_cat_edad', 'departamento'])['anio'].count().reset_index(name='cant')
    df_sm_filtrado2_2 = df_sm_filtrado2
    df_sm_filtrado2_2.columns = ['anio','nombre_cat_edad', 'departamento','cant'] 
    
    
    
    # 3. Crear la tabla cruzada sumando la columna 'cant' 
    # Tabla Cruzada: 
    tabla_sm2 = df_sm_filtrado2_2.pivot_table(
        values='cant', 
        index='nombre_cat_edad', 
        columns='departamento', 
        aggfunc='sum', 
        fill_value=0, 
        observed=False)
    
    # tabla_cruzada2 = tabla_cruzada2.style.set_properties(**{'text-align': 'center'}) 
    
    
    # 4. Mostrar la tabla en Streamlit 
    st.write("Tabla cruzada, Total de Casos por Rangode Edad") 
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
    Dptos_sm_sel = st.selectbox("", deptos_sm)
    
    
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
    # GRÁFICO DE BARRAS SEGÚN DISPONIBILIDAD DE 'sexo' y 'Enfermedad_Evento' 
    
    
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
                df_agg = df_filtrado.groupby(['Periodo', 'sexo']).size().reset_index(name='Casos')
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

    
    
    
    
    
    
    
    
    
    
    
    
    

##3

































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
    











