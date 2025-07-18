import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize import numerize
from streamlit_extras.metric_cards import style_metric_cards

# Configuración inicial
st.set_page_config(page_title="📊 Dashboard de Morbilidad", page_icon="🧠", layout="wide")

# Estilo personalizado
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Título general
st.markdown("<h1 style='text-align: center; color: #3A3A3A;'>📈 MORBILIDAD: Tratamiento Estadístico, KPI y Tendencias</h1>", unsafe_allow_html=True)

# Cargar datos
df = pd.read_excel('Tasas_Morbilidad_25MB.xlsx', sheet_name='Hoja1')
df['anio'] = df['anio'].astype(str)

# Menú de navegación elegante
'''
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
'''



# Filtros elegantes
st.sidebar.markdown("### Filtros")
anio = st.sidebar.selectbox("Selecciona Año", options=sorted(df['anio'].unique(), reverse=True))
departamento = st.sidebar.selectbox("Departamento", options=["Todos"] + sorted(df['departamento'].dropna().unique().tolist()))
municipio = st.sidebar.selectbox("Municipio", options=["Todos"] + sorted(df['municipio'].dropna().unique().tolist()))

# Filtro lógico aplicado a la base
df_filtrado = df.copy()
if departamento != "Todos":
    df_filtrado = df_filtrado[df_filtrado['departamento'] == departamento]
if municipio != "Todos":
    df_filtrado = df_filtrado[df_filtrado['municipio'] == municipio]
if anio:
    df_filtrado = df_filtrado[df_filtrado['anio'] == anio]

# Vista según sección seleccionada
if selected == "📊 KPI":
    st.subheader("Indicadores Clave de Morbilidad")
    col1, col2, col3 = st.columns(3)
    col1.metric("Casos Totales", numerize.numerize(df_filtrado["casos"].sum()), "↗︎")
    col2.metric("Tasa Promedio", f"{df_filtrado['tasa_morbilidad'].mean():.2f}")
    col3.metric("Número de Municipios", df_filtrado["municipio"].nunique())

    style_metric_cards(background_color="#F0F2F6", border_left_color="#0d6efd", border_color="#e6e6e6")

elif selected == "📉 Tendencias":
    st.subheader("Tendencia Anual de la Tasa de Morbilidad")
    fig = px.line(df_filtrado.groupby('anio').mean(numeric_only=True).reset_index(), 
                  x='anio', y='tasa_morbilidad', title='Tasa de Morbilidad Anual')
    st.plotly_chart(fig, use_container_width=True)

elif selected == "📍 Mapa":
    st.subheader("Mapa Interactivo de Morbilidad")
    st.map(df_filtrado[['latitud', 'longitud']].dropna())

elif selected == "📥 Datos":
    st.subheader("Datos Detallados")
    st.dataframe(df_filtrado)

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


# =============================================

# 📍 📎 🗺️ 🎯 🔗 ⚓ 🏠 🏢 🏭 🏬
# 🏷️ 🔖 📋 📝 📄 📊 📈 📉 🗂️ 📁
# 🔧 🔨 ⚙️ 🛠️ ⚡ 🔧 🗝️ 🔑 🎛️ ⚖️
#  ⚠️ ❗ ❓ ✅ ❌ 🟢 🔴 🟡 🟠 🔵
# 👆 👇 👈 👉 ↗️ ↘️ ↙️ ↖️ ⬆️ ⬇️ ⬅️ ➡️
# 💡 🔍 🎲 🎯 🎪 🎨 🎭 🎪 🎊 🎉
# 📊 📈 📉 💹 📋 🗃️ 🗄️ 💾 💿 📀
# 🏥 ⚕️ 💊 🩺 🧬 🦠 💉 🧪 🔬 📱

# =============================================



with st.expander("👉 Mostrar Filtros", expanded=False):
    Departamento = st.multiselect(
        "Selecciona Departamento",
        options=df["departamento"].unique(),
        default=df["departamento"].unique(),
    )

    Municipio = st.multiselect(
        "Selecciona Municipio",
        options=df["municipio"].unique(),
        default=df["municipio"].unique(),
    )

    Grupo = st.multiselect(
        "Selecciona el Grupo de Enfermedad",
        options=df["grupo"].unique(),
        default=df["grupo"].unique(),
    )








df_selection=df.query(
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
    with st.expander("Distribución de Frecuencias - Variables Cuantitativas"):
     df.hist(figsize=(16,8),color='#898784', zorder=2, rwidth=0.9,legend = ['tasa_morb']);
     st.pyplot()

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
    Home()
    graphs()
 if selected=="Progress":
    #st.subheader(f"Page: {selected}")
    Progressbar()
    graphs()


sideBar()
#st.sidebar.image("data/Logo_UNILLANOS.png",caption="")      # LOGO
st.sidebar.image("Logo_UNILLANOS.png",caption="")            # LOGO



st.subheader('Seleccione Atributos para Observar Tendencias de Distrib. Por Cuartiles',)
#feature_x = st.selectbox('Select feature for x Qualitative data', df_selection.select_dtypes("object").columns)
feature_y = st.selectbox('Seleccionar función para (Y) Datos cuantitativos', df_selection.select_dtypes("number").columns)
fig2 = go.Figure(
    data=[go.Box(x=df['grupo'], y=df[feature_y])],
    layout=go.Layout(
        title=go.layout.Title(text="Distribución Numérica, por Grupo de Enfermedades"),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
        font=dict(color='#cecdcd'),  # Set text color to black
    )
)
# Display the Plotly figure using Streamlit
st.plotly_chart(fig2,use_container_width=True)



#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""





# PARA EJECUTAR EL DASHBOARD, CORRER LAS SIGUIENTES LÍNEAS EN C:
# Invoca la carpeta donde está ubicado el archivo:  --->

# cd C:\Users\cesar\Downloads\TABLERO_STREAMLIT_DASHBOARD\DASHBOARD_STREAMLIT_COMPLETO




# Invocando el archivo: ---->
# python streamlit_app.py (este comando no corrió... entonces ejecutar el siguiente: ----> )

# streamlit run Home_Tablero.py



























