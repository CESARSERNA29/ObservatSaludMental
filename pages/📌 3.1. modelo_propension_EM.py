
# ===========================================
# Evaluación de propensión a esquizofrenia
# Niveles: Departamento, Municipio, Persona
# Modelos: Random Forest, XGBoost, NN, Scoring
# Visualización: Mapa de calor
# ===========================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns





import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, classification_report
)
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression



# ----------------------------
# Simulación de datos
# ----------------------------


# Cargar datos
#import pandas as pd
#df = pd.read_excel(
#    r"C:\Users\cesar\Downloads\TABLERO_STREAMLIT_DASHBOARD\DASHBOARD_Morbilidad_DESPLIEGUE_2\TablaParaModelosAnaliticos.xlsx",
#    sheet_name="TabModSM"
#)


df = pd.read_excel('data/TablaParaModelosAnaliticos.xlsx', sheet_name="TabModSM")





# Variable objetivo simulada: presencia de esquizofrenia
#df['Presencia_Esq'] = np.where((df['Enf1'] > 0) & (df['Municipio'] == 'Villavicencio'), 1, 0)

# ----------------------------




#df = pd.read_excel(r"C:\Users\cesar\Downloads\TABLERO_STREAMLIT_DASHBOARD\DASHBOARD_Morbilidad_DESPLIEGUE_2\Tasas_Morbilidad_25MB.xlsx", sheet_name="NombreDeLaHoja")

# -------------------------
# Selección de variables
# -------------------------
# Variables predictoras
X = df[['Hombres', 'Mujeres',
        'a. Primera infancia', 'b. Infancia', 'c. Adolescencia',
        'd. Adultez temprana', 'e. Adultez media', 'f. Adulto mayor',
        'Agresiones', 'ConsSustaPsicoact', 'Esquizofrenia', 'LesionAutoinf',
        'RetrasMental', 'SíndromComportamiento', 'TrastornAfectiv',
        'TrastorPersonAdult', 'TrastornDesarroPsico', 'TrastornHabitNiñezAdoles',
        'TrastornMentales', 'TrastornNeurotic']]

# Escoge el tipo de modelo (clasificación o regresión)
modo = "clasificacion"  # Cambia a "regresion" si deseas usar TotEvent_SM

if modo == "clasificacion":
    y = df['NivEvent_SM']  # Variable objetivo categórica
else:
    y = df['TotEvent_SM']  # Variable objetivo numérica





# Por la variable Y es categórica:
from sklearn.preprocessing import LabelEncoder

# Codificar etiquetas si es clasificación
if modo == "clasificacion":
    le = LabelEncoder()
    y = le.fit_transform(df['NivEvent_SM'])
else:
    y = df['TotEvent_SM']



# División del dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)





# ===========================================

# -------------------------
# Modelos Clasificación
# -------------------------
modelos = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
    "Neural Net": MLPClassifier(hidden_layer_sizes=(10,), max_iter=500, random_state=42),
    "Scoring": LogisticRegression(max_iter=1000)
}

resultados = []
y_preds = {}

for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    y_preds[nombre] = y_pred

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    spec = np.nan  # Especificidad no aplica fácilmente en multiclase
    auc = np.nan   # AUC multiclase requiere tratamiento especial

    resultados.append({
        "Modelo": nombre,
        "Accuracy": acc,
        "Precisión": prec,
        "Sensibilidad (Recall)": recall,
        "Especificidad": spec,
        "F1 Score": f1,
        "AUC": auc
    })









# -------------------------
# Comparación de Modelos
# -------------------------
df_resultados = pd.DataFrame(resultados).sort_values("F1 Score", ascending=False)

st.subheader("📊 Comparativa de Modelos de Clasificación")

# Lista exacta de columnas numéricas que quieres formatear (si están presentes)
columnas_numericas = [
    "Hombres", "Mujeres", "a. Primera infancia", "b. Infancia", "c. Adolescencia",
    "d. Adultez temprana", "e. Adultez media", "f. Adulto mayor",
    "Agresiones", "ConsSustaPsicoact", "Esquizofrenia", "LesionAutoinf", "RetrasMental",
    "SíndromComportamiento", "TrastornAfectiv", "TrastorPersonAdult", "TrastornDesarroPsico",
    "TrastornHabitNiñezAdoles", "TrastornMentales", "TrastornNeurotic", "TotEvent_SM",
    "Accuracy", "Precisión", "Sensibilidad (Recall)", "Especificidad", "F1 Score", "AUC"
]

# Verifica que solo existan las columnas antes de aplicar el formato
columnas_formateables = [col for col in columnas_numericas if col in df_resultados.columns]
formato_columnas = {col: "{:.3f}" for col in columnas_formateables}

# Mostrar con formato seguro
try:
    st.dataframe(df_resultados.style.format(formato_columnas))
except Exception as e:
    st.error(f"❌ Error mostrando la tabla formateada: {e}")
    st.dataframe(df_resultados)

# -------------------------
# Matrices de Confusión
# -------------------------
st.subheader("📌 Matrices de Confusión")

# Construcción dinámica de etiquetas (en caso de multiclase)
etiquetas = le.classes_ if 'le' in locals() else sorted(set(y_test))

for nombre, y_pred in y_preds.items():
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, 
                xticklabels=etiquetas, yticklabels=etiquetas, ax=ax)
    ax.set_title(f"Matriz de Confusión - {nombre}")
    ax.set_xlabel("Predicción")
    ax.set_ylabel("Real")
    st.pyplot(fig)

# -------------------------
# Mejor modelo
# -------------------------
mejor_modelo = df_resultados.iloc[0]["Modelo"]
st.success(f"✅ Mejor modelo según F1 Score: {mejor_modelo}")







# 2. Código para visualizar el árbol del Random Forest
from sklearn.tree import export_graphviz
import pydotplus
from io import StringIO
from PIL import Image
import streamlit as st

# Extraer uno de los árboles del bosque
arbol = modelos["Random Forest"].estimators_[0]

# Exportar a formato DOT
dot_data = StringIO()
export_graphviz(
    arbol,
    out_file=dot_data,
    feature_names=X.columns,
    class_names=[str(c) for c in le.classes_] if modo == "clasificacion" else None,
    filled=True,
    rounded=True,
    special_characters=True
)

# Crear imagen con pydotplus
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
img = Image.open(graph.create_png())

# Mostrar en Streamlit
st.subheader("🌳 Visualización de un árbol del modelo Random Forest (Graphviz)")
st.image(img, caption="Árbol de decisión (árbol 0 del Random Forest)", use_column_width=True)




















