# MODELO CIUDAD:

    



# =======================================
# 📊 DASHBOARD INTERACTIVO STREAMLIT con KPIs VISUALES
# =======================================
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ============================
# 1. Configuración de la página
# ============================
st.set_page_config(page_title="Dashboard Score", layout="wide")
st.title("📊 Dashboard Interactivo - Score por Filtros")

# ============================
# 2. Cargar Datos
# ============================
df = pd.read_excel("Tabla_SALIDA_Para_ModeloCiudad.xlsx", sheet_name="ScoreTablero")
# df = pd.read_excel(r"C:\Users\cesar\Downloads\TABLERO_STREAMLIT_DASHBOARD\DASHBOARD_Morbilidad_DESPLIEGUE_2\Tabla_SALIDA_Para_ModeloCiudad.xlsx", sheet_name="ScoreTablero")

# ============================
# 3. Sidebar - Filtros
# ============================
st.sidebar.header("Filtros")

anio_filter = st.sidebar.multiselect(
    "Selecciona Año:",
    options=sorted(df["Anio"].unique()),
    default=sorted(df["Anio"].unique())
)

edad_filter = st.sidebar.multiselect(
    "Selecciona Edad:",
    options=df["a. Primera infancia"].unique(),
    default=df["a. Primera infancia"].unique()
)

sexo_filter = st.sidebar.multiselect(
    "Selecciona Sexo:",
    options=df["Tot_Hombres"].unique(),
    default=df["Tot_Hombres"].unique()
)

depto_filter = st.sidebar.multiselect(
    "Selecciona Departamento:",
    options=df["Departamento"].unique(),
    default=df["Departamento"].unique()
)

mun_filter = st.sidebar.multiselect(
    "Selecciona Municipio:",
    options=df["Municipio"].unique(),
    default=df["Municipio"].unique()
)

# ============================
# 4. Filtrar DataFrame
# ============================
df_filtered = df[
    (df["Anio"].isin(anio_filter)) &
    (df["a. Primera infancia"].isin(edad_filter)) &
    (df["Tot_Hombres"].isin(sexo_filter)) &
    (df["Departamento"].isin(depto_filter)) &
    (df["Municipio"].isin(mun_filter))
]

# ============================
# 5. Comparación con año anterior
# ============================
variacion_pct = None
flecha_variacion = "➡️"
color_variacion = "black"

# *** (Opcional) revisar filtro sexo: si tienes una columna 'Sexo' úsala en el sidebar
# sexo_filter = st.sidebar.multiselect("Selecciona Sexo:", options=df["Sexo"].unique(), default=df["Sexo"].unique())

if len(anio_filter) >= 2:
    anio_actual = max(anio_filter)
    anio_anterior = sorted(anio_filter)[-2]

    df_actual = df_filtered[df_filtered["Anio"] == anio_actual]
    df_anterior = df_filtered[df_filtered["Anio"] == anio_anterior]

    # KPIs globales (promedios)
    score_actual = df_actual["Score_Unico_Ordinal"].mean()
    score_anterior = df_anterior["Score_Unico_Ordinal"].mean()

    if pd.notna(score_anterior) and score_anterior != 0:
        variacion_pct = ((score_actual - score_anterior) / score_anterior) * 100

        if variacion_pct > 0:
            flecha_variacion = "⬆️"
            color_variacion = "green"
        elif variacion_pct < 0:
            flecha_variacion = "⬇️"
            color_variacion = "red"
        else:
            flecha_variacion = "➡️"
            color_variacion = "gray"

    # Comparación por departamento (promedios por dpto para cada año)
    df_actual_depto = df_actual.groupby("Departamento")["Score_Unico_Ordinal"].mean().reset_index()
    df_anterior_depto = df_anterior.groupby("Departamento")["Score_Unico_Ordinal"].mean().reset_index()

    # Merge — esto generará columnas con sufijos, por ejemplo:
    # Score_Unico_Ordinal_actual y Score_Unico_Ordinal_anterior
    df_comp = pd.merge(df_actual_depto, df_anterior_depto, on="Departamento", how="left", suffixes=("_actual", "_anterior"))

    # Normalizar nombres resultantes a Score_actual / Score_anterior (robusto frente a variaciones)
    # Buscar la columna que termina en '_actual' y la que termina en '_anterior'
    actual_col = [c for c in df_comp.columns if c.endswith('_actual')][0]
    anterior_col = [c for c in df_comp.columns if c.endswith('_anterior')][0]

    df_comp = df_comp.rename(columns={actual_col: 'Score_actual', anterior_col: 'Score_anterior'})

    # Calcular variación (si no hay dato anterior, mantenemos NaN para tratarlo visualmente)
    df_comp['variacion'] = df_comp['Score_actual'] - df_comp['Score_anterior']

    # Flechas y colores: si no hay valor anterior => gris/➡️
    def flecha_color(row):
        if pd.isna(row['Score_anterior']):
            return pd.Series({'flecha': '➡️', 'color': 'gray'})
        if row['variacion'] > 0:
            return pd.Series({'flecha': '⬆️', 'color': 'red'})
        if row['variacion'] < 0:
            return pd.Series({'flecha': '⬇️', 'color': 'lightblue'})
        return pd.Series({'flecha': '➡️', 'color': 'gray'})

    df_comp[['flecha', 'color']] = df_comp.apply(flecha_color, axis=1)

else:
    st.warning("Selecciona al menos 2 años para ver la comparación con año anterior.")
    df_comp = df_filtered.groupby("Departamento")["Score_Unico_Ordinal"].mean().reset_index()
    df_comp.rename(columns={"Score_Unico_Ordinal": "Score_actual"}, inplace=True)
    df_comp["flecha"] = "➡️"
    df_comp["color"] = "gray"






# ============================
# 6. KPIs con estilo
# ============================
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

with col_kpi1:
    st.markdown(
        f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center;">
            <h3>📊 Score Promedio</h3>
            <h1 style="color:#1f77b4;">{df_filtered['Score_Unico_Ordinal'].mean():,.2f}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_kpi2:
    st.markdown(
        f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center;">
            <h3>🏆 Score Máximo</h3>
            <h1 style="color:#ff7f0e;">{df_filtered['Score_Unico_Ordinal'].max():,.2f}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_kpi3:
    if variacion_pct is not None:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center;">
                <h3>📈 Variación vs Año Anterior</h3>
                <h1 style="color:{color_variacion};">{flecha_variacion} {variacion_pct:.2f}%</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center;">
                <h3>📈 Variación vs Año Anterior</h3>
                <h1 style="color:gray;">N/A</h1>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================
# 7. Layout en dos filas
# ============================
col1, col2 = st.columns(2)

# ----- Gráfico 1: Comparación por Departamento -----
fig_comp = go.Figure()
fig_comp.add_trace(go.Bar(
    x=df_comp["Departamento"],
    y=df_comp["Score_actual"],
    marker_color=df_comp["color"],
    text=df_comp["flecha"],
    textposition="outside",
    textfont=dict(size=18)
))
fig_comp.update_layout(
    title="📈 Score Promedio por Departamento (con variación)",
    yaxis_title="Score",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#cecdcd")
)
col1.plotly_chart(fig_comp, use_container_width=True)

# ----- Gráfico 2: Distribución de Score -----
fig_box = px.box(
    df_filtered,
    x="Departamento",
    y="Score",
    color="Departamento",
    title="📦 Distribución del Score por Departamento",
    template="plotly_white"
)
col2.plotly_chart(fig_box, use_container_width=True)

# ============================
# 8. Fila 2: Línea temporal
# ============================
fig_line = px.line(
    df_filtered.groupby(["Año", "Departamento"])["Score_Unico_Ordinal"].mean().reset_index(),
    x="Año",
    y="Score",
    color="Departamento",
    markers=True,
    title="📆 Evolución del Score por Año y Departamento",
    labels={"Score_Unico_Ordinal": "Score promedio", "Anio": "Año"},
    template="plotly_white"
)
st.plotly_chart(fig_line, use_container_width=True)

