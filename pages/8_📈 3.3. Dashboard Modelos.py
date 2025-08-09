# MODELO CIUDAD:

    



# =======================================
# 📊 DASHBOARD INTERACTIVO STREAMLIT con KPIs VISUALES y FILTROS SUPERIORES
# =======================================
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ============================
# 1. Configuración de página
# ============================
st.set_page_config(page_title="Dashboard Score", layout="wide")
st.title("📊 Dashboard Interactivo - Score por Filtros")

# ============================
# 2. Estilos CSS
# ============================
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ============================
# 3. Cargar Datos
# ============================
df = pd.read_excel("Tabla_SALIDA_Para_ModeloCiudad.xlsx", sheet_name="ScoreTablero")

# Asegurar consistencia de nombres de columnas
if "Anio" in df.columns:
    df.rename(columns={"Anio": "Año"}, inplace=True)

# ============================
# 4. Filtros superiores
# ============================
col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)

anio_filter = col_f1.multiselect(
    "Año:",
    options=sorted(df["Año"].unique()),
    default=sorted(df["Año"].unique())
)
edad_filter = col_f2.multiselect(
    "Edad:",
    options=df["a. Primera infancia"].unique(),
    default=df["a. Primera infancia"].unique()
)
sexo_filter = col_f3.multiselect(
    "Sexo:",
    options=df["Tot_Hombres"].unique(),
    default=df["Tot_Hombres"].unique()
)
depto_filter = col_f4.multiselect(
    "Departamento:",
    options=df["Departamento"].unique(),
    default=df["Departamento"].unique()
)
mun_filter = col_f5.multiselect(
    "Municipio:",
    options=df["Municipio"].unique(),
    default=df["Municipio"].unique()
)

# ============================
# 5. Filtrar datos
# ============================
df_filtered = df[
    (df["Año"].isin(anio_filter)) &
    (df["a. Primera infancia"].isin(edad_filter)) &
    (df["Tot_Hombres"].isin(sexo_filter)) &
    (df["Departamento"].isin(depto_filter)) &
    (df["Municipio"].isin(mun_filter))
]

# ============================
# 6. Comparación con año anterior
# ============================
variacion_pct = None
flecha_variacion = "➡️"
color_variacion = "gray"

if len(anio_filter) >= 2:
    anio_actual = max(anio_filter)
    anio_anterior = sorted(anio_filter)[-2]

    df_actual = df_filtered[df_filtered["Año"] == anio_actual]
    df_anterior = df_filtered[df_filtered["Año"] == anio_anterior]

    score_actual = df_actual["Score_Unico_Ordinal"].mean()
    score_anterior = df_anterior["Score_Unico_Ordinal"].mean()

    if pd.notna(score_anterior) and score_anterior != 0:
        variacion_pct = ((score_actual - score_anterior) / score_anterior) * 100
        if variacion_pct > 0:
            flecha_variacion = "⬆️"
            color_variacion = "red"
        elif variacion_pct < 0:
            flecha_variacion = "⬇️"
            color_variacion = "lightblue"

    df_actual_depto = df_actual.groupby("Departamento")["Score_Unico_Ordinal"].mean().reset_index()
    df_anterior_depto = df_anterior.groupby("Departamento")["Score_Unico_Ordinal"].mean().reset_index()
    df_comp = pd.merge(df_actual_depto, df_anterior_depto, on="Departamento", how="left",
                       suffixes=("_actual", "_anterior"))
    df_comp.rename(columns={"Score_Unico_Ordinal_actual": "Score_actual",
                            "Score_Unico_Ordinal_anterior": "Score_anterior"}, inplace=True)
    df_comp["variacion"] = df_comp["Score_actual"] - df_comp["Score_anterior"]

    def flecha_color(row):
        if pd.isna(row["Score_anterior"]):
            return pd.Series({"flecha": "➡️", "color": "gray"})
        if row["variacion"] > 0:
            return pd.Series({"flecha": "⬆️", "color": "red"})
        if row["variacion"] < 0:
            return pd.Series({"flecha": "⬇️", "color": "lightblue"})
        return pd.Series({"flecha": "➡️", "color": "gray"})

    df_comp[["flecha", "color"]] = df_comp.apply(flecha_color, axis=1)

else:
    st.warning("Selecciona al menos 2 años para la comparación.")
    df_comp = df_filtered.groupby("Departamento")["Score_Unico_Ordinal"].mean().reset_index()
    df_comp.rename(columns={"Score_Unico_Ordinal": "Score_actual"}, inplace=True)
    df_comp["flecha"] = "➡️"
    df_comp["color"] = "gray"

# ============================
# 7. KPIs
# ============================
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

col_kpi1.markdown(f"""
<div class="kpi-card">
    <h3>📊 Score Promedio</h3>
    <h1 style="color:#1f77b4;">{df_filtered['Score_Unico_Ordinal'].mean():,.2f}</h1>
</div>
""", unsafe_allow_html=True)

col_kpi2.markdown(f"""
<div class="kpi-card">
    <h3>🏆 Score Máximo</h3>
    <h1 style="color:#ff7f0e;">{df_filtered['Score_Unico_Ordinal'].max():,.2f}</h1>
</div>
""", unsafe_allow_html=True)

if variacion_pct is not None:
    col_kpi3.markdown(f"""
    <div class="kpi-card">
        <h3>📈 Variación vs Año Anterior</h3>
        <h1 style="color:{color_variacion};">{flecha_variacion} {variacion_pct:.2f}%</h1>
    </div>
    """, unsafe_allow_html=True)
else:
    col_kpi3.markdown(f"""
    <div class="kpi-card">
        <h3>📈 Variación vs Año Anterior</h3>
        <h1 style="color:gray;">N/A</h1>
    </div>
    """, unsafe_allow_html=True)

# ============================
# 8. Gráficos
# ============================
col1, col2 = st.columns(2)

fig_comp = go.Figure()
fig_comp.add_trace(go.Bar(
    x=df_comp["Departamento"],
    y=df_comp["Score_actual"],
    marker_color=df_comp["color"],
    text=df_comp["flecha"],
    textposition="outside",
    textfont=dict(size=18)
))
fig_comp.update_layout(title="📈 Score Promedio por Departamento",
                       yaxis_title="Score", plot_bgcolor="rgba(0,0,0,0)")
col1.plotly_chart(fig_comp, use_container_width=True)

fig_box = px.box(df_filtered, x="Departamento", y="Score_Unico_Ordinal", color="Departamento",
                 title="📦 Distribución del Score por Departamento", template="plotly_white")
col2.plotly_chart(fig_box, use_container_width=True)

fig_line = px.line(df_filtered.groupby(["Año", "Departamento"])["Score_Unico_Ordinal"].mean().reset_index(),
                   x="Año", y="Score_Unico_Ordinal", color="Departamento", markers=True,
                   title="📆 Evolución del Score por Año y Departamento",
                   labels={"Score_Unico_Ordinal": "Score promedio", "Año": "Año"},
                   template="plotly_white")
st.plotly_chart(fig_line, use_container_width=True)
