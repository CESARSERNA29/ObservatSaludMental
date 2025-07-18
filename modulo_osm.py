# TABLAS
#===============================================================================
import pandas as pd
import plotly.express as px

def tabla_grupo(df, total_pob, index_col, values_col):
    # Validar que index_col y values_col existen en df
    if index_col not in df.columns:
        raise KeyError(f"Columna '{index_col}' no existe en el DataFrame.")
    if values_col not in df.columns:
        raise KeyError(f"Columna '{values_col}' no existe en el DataFrame.")

    # Crear pivot_table
    tabla = pd.pivot_table(
        df,
        values=values_col,
        index=index_col,
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    # Validar que values_col está en tabla
    if values_col not in tabla.columns:
        raise KeyError(f"Columna '{values_col}' no está presente tras pivot_table. Columnas: {tabla.columns.tolist()}")

    # Calcular total de casos
    total_casos = tabla[values_col].sum()
    if total_casos == 0:
        # Evitar división por cero
        raise ValueError("El total de casos es cero. No se puede calcular porcentajes ni tasas.")

    # Agregar columnas %(porcentaje) y Tasa
    tabla['(%)'] = (tabla[values_col] / total_casos * 100).round(2)
    tabla['Tasa'] = (tabla[values_col] / total_pob).round(2)

    # Renombrar para presentación
    col_rename = {
        index_col: 'Grupo',
        values_col: 'Número de Casos',
        'Tasa': 'Tasa x 10000 Hab.'
    }
    tabla = tabla.rename(columns=col_rename)

    # Aplicar estilo pandas
    tabla = tabla.style \
        .set_properties(
            subset=['Número de Casos', '(%)', 'Tasa x 10000 Hab.'],
            **{'text-align': 'center'}
        ) \
        .set_table_styles([
            {'selector': 'th', 'props': [('text-align', 'center')]}
        ]) \
        .format({
            '(%)': '{:.2f}',
            'Tasa x 10000 Hab.': '{:.2f}',
            'Número de Casos': '{:,.0f}'
        })

    return tabla
#-------------------------------------------------------------------------------  
def tabla_dlt(df,total_pob):
  
  df=df[df['region']=='Orinoquía']
  tabla = pd.pivot_table(df,values='cant',index='desc_delito',aggfunc='sum',
    fill_value=0).reset_index()
  tabla.reset_index(drop=True)
  # Calcular el total de casos
  total_casos = tabla['cant'].sum()
  
  # Agregar columna de porcentaje
  tabla['(%)'] = (tabla['cant'] / total_casos * 100).round(2)
  tabla['Tasa'] = (tabla['cant'] / total_pob).round(2)
  
  tabla = tabla.rename(columns={'desc_delito':'Delito','cant':'Número de Casos',
    'Tasa':'Tasa x 10000 Hab.'})
  
  # Aplicar estilo para centrar solo las columnas 'Número de Casos' y '(%)'
  tabla = tabla.style\
  .set_properties(
    subset=['Número de Casos', '(%)', 'Tasa x 10000 Hab.'],
    **{'text-align': 'center'}
  )\
  .set_table_styles(
    [{'selector': 'th', 'props': [('text-align', 'center')]}]
  )\
  .format({
    '(%)': '{:.2f}',
    'Tasa x 10000 Hab.': '{:.2f}',
    'Número de Casos': '{:,.0f}'
  })
  
  return(tabla)
  
  # GRAFICAS
  #===============================================================================
  
def diag_lineas(df,titulo):
  
  df['anio']=pd.to_numeric(df['anio'], errors='coerce')
  a_min=df['anio'].min()-1
  a_max=df['anio'].max()+1
  
  # Crear gráfico de líneas con Plotly Express
  fig = px.line(df,x='anio',y='cant',color='sexo',markers=True,
                title=titulo,
                color_discrete_sequence=["#2A3180","#E5352B"])
  
  # Personalizar marcadores para que tengan borde del color de la línea y fondo blanco
  fig.update_traces(
      marker=dict(size=10,
                color='white',          # fondo blanco
                line=dict(width=2)      # borde que tomará el color de la línea
      )
  )
  
    # Ajustar eje x para mostrar todos los años y con rango fijo
  fig.update_xaxes(
      dtick=1,
      range=[a_min,a_max],
      tickmode='linear'
  )
  
  fig.update_xaxes(title_text="")
  fig.update_yaxes(title_text="Número de casos")
  
  return(fig)
 
 #------------------------------------------------------------------------------
 
def diag_barras_apil(df,titulo):
  
  fig = px.bar(df,x='Categoría',y='Valor',color='Subgrupo',barmode='stack',
                title=titulo)
  return(fig) 
  
