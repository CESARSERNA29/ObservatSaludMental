



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
        La salud mental es un componente fundamental del bienestar individual y colectivo de la humanidad, especialmente en contextos marcados por desigualdad, la violencia o la exclusión social.  Desde el bienestar general de las personas y de la estabilidad social de los territorios, la Salud Mental no se trata únicamente de la presencia de trastornos psicológicos, sino de un estado dinámico en el que el individuo puede desarrollar sus habilidades, enfrentar las tensiones normales de la vida, trabajar de forma productiva y contribuir a su comunidad.
        
        \nAhora bien, el interés por estudiar la salud mental desde enfoques cuantitativos, especialmente ante el incremento de diagnósticos relacionados con trastornos de ansiedad, depresión, consumo de sustancias y conductas suicidas, es una necesidad cada vez más frecuente. Esta condición ha sido resaltada por eventos globales como la pandemia del COVID-19, crisis migratorias (desplazamientos), desigualdades estructurales y violencia comunitaria. 
        
        \nEn regiones como la Orinoquía colombiana, caracterizada por una amplia diversidad étnica, condiciones geográficas particulares y limitaciones estructurales de acceso a servicios de salud, el análisis estadístico riguroso de la salud mental se vuelve una herramienta crítica para orientar políticas públicas, optimizar recursos y diseñar intervenciones focalizadas.
       
       
    """, unsafe_allow_html=True)






# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================

st.markdown("---")  # Otra línea si quieres enfatizarlo aún más
st.markdown(
    "<h3 style='text-align: center; color: #DC143C;'>Adicionar aLgo de Salud Mental (Profes...)</h3>", 
    unsafe_allow_html=True
)
st.markdown("---")

# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================




#  ------------------------------------------------------------







