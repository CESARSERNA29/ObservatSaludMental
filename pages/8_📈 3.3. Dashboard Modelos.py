# MODELO CIUDAD:

    



# =======================================
# 📊 DASHBOARD STREAMLIT con FILTROS TIPO BOTÓN
# =======================================
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ============================
# Configuración de página
# ============================
st.set_page_config(page_title="Dashboard Score", layout="wide")
st.title("📊 Dashboard Interactivo - Filtros tipo Botón")

# ============================
# Cargar datos
# ============================
df = pd.read_excel("Tabla_SALIDA_Para_ModeloCiudad.xlsx", sheet_name="ScoreTablero")
if "Anio" in df.columns:
    df.rename(columns={"Anio": "Año"}, inplace=True)

# ============================
# Filtros como botones toggle
# ============================
st.subheader("🎛 Filtros (activar/desactivar)")

def toggle_filter(label, options):
    selected = []
    cols = st.columns(len(options))
    for i, opt in enumerate(options):
        if cols[i].checkbox(str(opt), value=True, key=f"{label}_{opt}"):
            selected.append(opt)
    return selected

col_f1, col_f2 = st.columns(2)
with col_f1:
    anio_filter = toggle_filter("Año", sorted(df["Año"].unique()))
with col_f2:
    edad_filter = toggle_filter("Edad", sorted(df["a. Primera infancia"].unique()))

col_f3, col_f4 = st.columns(2)
with col_f3:
    sexo_filter = toggle_filter("Sexo", sorted(df["Tot_Hombres"].unique()))
with col_f4:
    depto_filter = toggle_filter("Departamento", sorted(df["Departamento"].unique()))

mun_filter = toggle_filter("Municipio", sorted(df["Municipio"].unique()))

# ============================
# Filtrar datos
# ============================
df_filtered = df[
    (df["Año"].isin(anio_filter)) &
    (df["a. Primera infancia"].isin(edad_filter)) &
    (df["Tot_Hombres"].isin(sexo_filter)) &
    (df["Departamento"].isin(depto_filter)) &
    (df["Municipio"].isin(mun_filter))
]

# ============================
# KPIs
# ============================
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
col_kpi1.metric("📊 Score Promedio", f"{df_filtered['Score_Unico_Ordinal'].mean():,.2f}")
col_kpi2.metric("🏆 Score Máximo", f"{df_filtered['Score_Unico_Ordinal'].max():,.2f}")

if len(anio_filter) >= 2:
    anio_actual = max(anio_filter)
    anio_anterior = sorted(anio_filter)[-2]
    score_actual = df_filtered[df_filtered["Año"] == anio_actual]["Score_Unico_Ordinal"].mean()
    score_anterior = df_filtered[df_filtered["Año"] == anio_anterior]["Score_Unico_Ordinal"].mean()
    if score_anterior != 0:
        variacion_pct = ((score_actual - score_anterior) / score_anterior) * 100
        flecha = "⬆️" if variacion_pct > 0 else "⬇️" if variacion_pct < 0 else "➡️"
        col_kpi3.metric("📈 Variación %", f"{variacion_pct:.2f}%", flecha)
else:
    col_kpi3.metric("📈 Variación %", "N/A")

# ============================
# Gráficos
# ============================
col1, col2 = st.columns(2)
fig_bar = px.bar(df_filtered.groupby("Departamento")["Score_Unico_Ordinal"].mean().reset_index(),
                 x="Departamento", y="Score_Unico_Ordinal", title="📊 Score Promedio por Departamento",
                 color="Departamento", template="plotly_white")
col1.plotly_chart(fig_bar, use_container_width=True)

fig_box = px.box(df_filtered, x="Departamento", y="Score_Unico_Ordinal", color="Departamento",
                 title="📦 Distribución del Score", template="plotly_white")
col2.plotly_chart(fig_box, use_container_width=True)

fig_line = px.line(df_filtered.groupby(["Año", "Departamento"])["Score_Unico_Ordinal"].mean().reset_index(),
                   x="Año", y="Score_Unico_Ordinal", color="Departamento", markers=True,
                   title="📆 Evolución del Score", template="plotly_white")
st.plotly_chart(fig_line, use_container_width=True)
