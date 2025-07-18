



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
        Home1()
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
    





    
    
   
    
    
    
    
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")
    
    
    
    
    
    
    
    
    
    
    
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")
    
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")
    
    
    
    

    
   
    
##3






















# ****************************************************************************
# ****************************************************************************
# ****************************************************************************
# ****************************************************************************
# ****************************************************************************
# ****************************************************************************
# ****************************************************************************
# ****************************************************************************




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
    





