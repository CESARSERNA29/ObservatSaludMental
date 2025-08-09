# MODELO CIUDAD:

    



# =======================================
# 📊 DASHBOARD INTERACTIVO STREAMLIT con KPIs VISUALES
# =======================================
import pandas as pd
import streamlit as st
import plotly.express as px

# ============================
# 1. Configuración de la página
# ============================
st.set_page_config(page_title="Dashboard Score", layout="wide")
st.title("📊 Dashboard Interactivo - Score por Filtros")

# ============================
# 2. Cargar Datos
# ============================
#df = pd.read_excel(
#    r"C:\Users\cesar\Downloads\TABLERO_STREAMLIT_DASHBOARD\DASHBOARD_Morbilidad_DESPLIEGUE_2\Tabla_SALIDA_Para_ModeloCiudad.xlsx",
#    sheet_name="ScoreTablero"
#)

df = pd.read_excel("Tabla_SALIDA_Para_ModeloCiudad.xlsx", sheet_name="ScoreTablero")

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
# 5. KPIs y Comparación con año anterior
# ============================
if df_filtered.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados.")
else:
    variacion_pct = None
    flecha_variacion = "➡️"
    color_variacion = "black"

    if len(anio_filter) >= 2:
        anio_actual = max(anio_filter)
        anio_anterior = sorted(anio_filter)[-2]

        df_actual = df_filtered[df_filtered["Anio"] == anio_actual]
        df_anterior = df_filtered[df_filtered["Anio"] == anio_anterior]

        score_actual = df_actual["Score_Unico_Ordinal"].mean()
        score_anterior = df_anterior["Score_Unico_Ordinal"].mean()

        if pd.notna(score_anterior) and score_anterior != 0:
            variacion_pct = ((score_actual - score_anterior) / score_anterior) * 100

            if variacion_pct > 0:
                flecha_variacion = "⬆️"
                color_variacion = "red"  # aumento = rojo
            elif variacion_pct < 0:
                flecha_variacion = "⬇️"
                color_variacion = "lightblue"  # disminución = azul claro
            else:
                flecha_variacion = "➡️"
                color_variacion = "gray"

        # KPI general
        kpi1, kpi2 = st.columns(2)
        kpi1.metric(
            label=f"Score promedio {anio_actual}",
            value=f"{score_actual:.2f}" if pd.notna(score_actual) else "N/A",
            delta=f"{variacion_pct:.2f}%" if variacion_pct is not None else "N/A",
            delta_color="inverse"  # para que azul sea disminución
        )

        # Comparación por departamento
        if not df_actual.empty and not df_anterior.empty:
            df_actual_depto = df_actual.groupby("Departamento")["Score_Unico_Ordinal"].mean().reset_index()
            df_anterior_depto = df_anterior.groupby("Departamento")["Score_Unico_Ordinal"].mean().reset_index()

            df_comp = pd.merge(
                df_actual_depto, df_anterior_depto,
                on="Departamento", how="left",
                suffixes=("_actual", "_anterior")
            )

            df_comp["variacion"] = df_comp["Score_Unico_Ordinal_actual"] - df_comp["Score_Unico_Ordinal_anterior"]
            df_comp["flecha"] = df_comp["variacion"].apply(lambda x: "⬆️" if x > 0 else ("⬇️" if x < 0 else "➡️"))
            df_comp["color"] = df_comp["variacion"].apply(lambda x: "red" if x > 0 else ("lightblue" if x < 0 else "gray"))

            st.subheader("📍 Comparación por Departamento")
            st.dataframe(df_comp)

    else:
        st.warning("Selecciona al menos 2 años para ver la comparación con año anterior.")

# ============================
# 6. Ejemplo de gráfico seguro
# ============================
if not df_filtered.empty:
    columnas_necesarias = ["Departamento", "Score_Unico_Ordinal"]
    if all(col in df_filtered.columns for col in columnas_necesarias):
        fig_box = px.box(
            df_filtered,
            x="Departamento",
            y="Score_Unico_Ordinal",
            color="Departamento",
            template="plotly_white"
        )
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.error(f"Faltan columnas necesarias: {columnas_necesarias}")
else:
    st.info("No se puede mostrar el gráfico porque no hay datos con los filtros seleccionados.")


