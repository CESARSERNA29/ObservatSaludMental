#===============================================================================
#  LECTURA DE ARCHIVOS
#===============================================================================


# Tablas para Morbilidad
# ------------------------------------------------------------------------------
def bd_morbilidad(Tabla):
    df = pd.read_excel('data/Vistas_DB2.xlsx',sheet_name=Tabla)
    # Convertir año a numerico
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df['grupo'] = df['grupo'].str.strip()  
    df['departamento']=df['departamento'].str.strip()
    df['departamento']=pd.Categorical(df['departamento'])
    #df=df[df['componente']=='Conv. Ciudadana']
    #df=df.drop('componente',axis=1)
    return df

# Tablas para Mortalidad
# ------------------------------------------------------------------------------
def bd_mortalidad(Tabla):
    df = pd.read_excel('data/Vistas_DB2.xlsx',sheet_name=Tabla)
    # Convertir año a categórica
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df['grupo'] = df['grupo'].str.strip()  
    df['departamento']=df['departamento'].str.strip()
    df['departamento']=pd.Categorical(df['departamento'])
    #df=df[df['componente']=='Conv. Ciudadana']
    #df=df.drop('componente',axis=1)
    return df

# Tablas Población
# ------------------------------------------------------------------------------
def bd_poblacion(tabla,año):
    df = pd.read_excel('data/Vistas_DB2.xlsx',sheet_name=tabla)
    # Convertir año a numeric
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df=df[df['anio']<=año]
    df['departamento']=pd.Categorical(df['departamento'])
    
    return df

# Tablas Delitos Policia Nacional
# ------------------------------------------------------------------------------
def bd_ponal():
    df = pd.read_excel('data/Vistas_DB2.xlsx',sheet_name='Delitos')
    # Convertir año a categórica
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df['departamento']=pd.Categorical(df['departamento'])
    
    return df

#===============================================================================
# TABLAS
#===============================================================================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math

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
    if total_pob!=0:
      tabla['Tasa'] = (tabla[values_col] / total_pob).round(2)
    else:
      tabla['Tasa'] = 0

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



#===============================================================================
# GRAFICAS
#===============================================================================
  
def diag_lineas(df,vx,vy,grupos,titulo,ylab,colores):
  
  df[vx]=pd.to_numeric(df[vx], errors='coerce')
  a_min=df[vx].min()-1
  a_max=df[vx].max()+1
  n=df[grupos].nunique()
  
  # Crear gráfico de líneas con Plotly Express
  fig = px.line(df,x=vx,y=vy,color=grupos,markers=True,
                title=titulo,
                color_discrete_sequence=colores)
  
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
  fig.update_yaxes(title_text=ylab)
  
  return(fig)
 
 #------------------------------------------------------------------------------
 
def diag_barras_apil(df,vx,vy,grupos,titulo,colores,bmode='stack',xlab="",ylab=""):
  
  n=df[grupos].nunique()
  colores_sel=colores[:n]
  fig = px.bar(df,x=vx,y=vy,
              color=grupos,
              barmode=bmode,
              color_discrete_sequence=colores_sel,
              title=titulo)
  fig.update_layout(xaxis_title=xlab,yaxis_title=ylab )
  #for trace in fig.data:
  #      trace.text = trace.y if hasattr(trace, 'y') else None  # texto con el valor de la barra
  #      trace.textposition = 'inside'   # texto dentro de la barra (centro)
  #      trace.textfont = dict(color='white')  # texto blanco
  return(fig) 
  
#-------------------------------------------------------------------------------

def diag_barras(df,vx,vy,grupo,titulo,colores):
  
  fig = px.bar(df,x=vx,y=vy,
               color=grupo,
               barmode='stack',
               color_discrete_sequence=colores_sel,
               title=titulo)
  return(fig) 


def diag_radar(cat,r1,r2,perfil1,perfil2,colores):
  
  v_max=math.ceil(max(max(r1),max(r2))/10)*10
  
  fig = go.Figure()
  # Serie 1
  fig.add_trace(go.Scatterpolar(r=r1,theta=cat,fill='toself',
    name=perfil1,line=dict(color=colores[0]),marker=dict(color=colores[0])))
  
  #Serie 2
  fig.add_trace(go.Scatterpolar(r=r2,theta=cat,fill='toself',
    name=perfil2, line=dict(color=colores[1]),marker=dict(color=colores[1])))

  fig.update_layout(
    polar=dict(radialaxis=dict(visible=True,range=[0, v_max])),
    showlegend=True)
  return(fig)
  
