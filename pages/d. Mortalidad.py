# Cargando las Librerías:
# ======================

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import numpy as np

import modulo_osm as osm
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Convivencia Ciudadana", layout="wide")
st.header("CONVIVENCIA CIUDADANA")
st.markdown("##")
#-------------------------------------------------------------------------------

st.markdown("""
        <h3 style='text-align: center; color: #333333;'>Introducción </h3>
        <hr style="height:2px;border-width:0;color:gray;background-color:gray">
    """, unsafe_allow_html=True)

st.markdown("""
        <div style="text-align: justify; font-size: 18px; color: #444444;">
        La convivencia ciudadana es la capacidad de los ciudadanos para vivir juntos en armonía, respetando normas comunes y resolviendo conflictos de manera pacífica, lo cual es esencial para garantizar entornos seguros y el bienestar social. Esta sección examina indicadores clave que reflejan la realidad social y de salud en la región de Orinoquía, permitiendo entender mejor los factores que afectan la calidad de vida y el tejido social. Al analizar diferentes dimensiones —morbilidad, mortalidad y delitos reportados— se facilita la toma de decisiones informadas para promover una convivencia más segura, inclusiva y saludable.
        </div>
    """, unsafe_allow_html=True)

st.markdown("##")


#-------------------------------------------------------------------------------
# RECUPERACION DE DATOS DESDE EL SESION_STATE
#-------------------------------------------------------------------------------
# Se definen los datos desde el estado de la sesion
df_pob=st.session_state.get('df_pob')
df_mt=st.session_state.get('df_mt')
P_Colores=st.session_state.get('P_Colores')
#-------------------------------------------------------------------------------
# Barra lateral de opciones
st.sidebar.header('Filtros')
#-------------------------------------------------------------------------------


# Contenido Mortalidad

st.header("MORTALIDAD")
st.write("Esta sección presenta datos de morbilidad, para enfermedades y problemas\
de salud que afectan a la población relacionada con factores que influyen en la convivencia\
social, incluyendo problemáticas de salud mental y condiciones asociadas. La información permite\
identificar las principales afectaciones en salud que pueden incidir en dinámicas sociales y\
el bienestar colectivo.")
    
    
   
