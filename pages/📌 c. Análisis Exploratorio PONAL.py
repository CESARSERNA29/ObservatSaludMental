

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
        <h3 style='text-align: center; color: #333333;'>DELITOS POLICÍA NACIONAL:  Tratamiento Estadístico, KPI y Tendencias </h3>
        <hr style="height:2px;border-width:0;color:gray;background-color:gray">
    """, unsafe_allow_html=True)

st.markdown("""
        <div style="text-align: justify; font-size: 18px; color: #444444;">
        Los casos de delitos registrados por la Policía Nacional constituyen una fuente clave para comprender los fenómenos de violencia, criminalidad y conflictividad social en el territorio. Desde una perspectiva epidemiológica y estadística, el análisis de estos eventos permite establecer vínculos entre la seguridad ciudadana y los determinantes sociales de la salud, particularmente en su relación con la morbilidad y la mortalidad asociadas a causas externas, como homicidios, lesiones personales, violencia intrafamiliar o violencia de género.
        
        Mediante la identificación de patrones geográficos, grupos poblacionales más afectados y tendencias temporales, es posible detectar zonas de alta incidencia delictiva, muchas veces coincidentes con áreas de mayor vulnerabilidad social y sanitaria. Este cruce de información entre los datos de criminalidad y los indicadores de salud pública permite abordar de forma integral problemáticas como la violencia estructural, la salud mental y los traumas físicos, y facilita el diseño de estrategias preventivas intersectoriales. 
        El análisis regional de la criminalidad, junto con los indicadores de morbilidad y mortalidad, aporta evidencia crucial para orientar políticas públicas en salud, seguridad y cohesión social, permitiendo priorizar recursos y actuar sobre factores estructurales que afectan tanto el bienestar como la vida de las personas.
        </div>
    """, unsafe_allow_html=True)

st.markdown("##")











