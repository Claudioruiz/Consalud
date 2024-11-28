import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el archivo Excel
uploaded_file = "Informe_Ejecutivos v.8.xlsx"  # Asegúrate de que el archivo esté en el mismo directorio o ruta
try:
    data = pd.read_excel(uploaded_file)
except FileNotFoundError:
    st.error("El archivo no fue encontrado. Verifica la ruta o nombre del archivo.")
    st.stop()

# Mostrar las columnas disponibles en el DataFrame (para depuración)
st.write("Columnas disponibles en el DataFrame:", data.columns.tolist())

# Definir las dimensiones principales
dimensiones = ["Actitud", "Conocimiento", "Argumentación", "Confiabilidad", "Claridad", "Seguridad"]

# Crear lista dinámica de columnas con sufijos
columnas_dinamicas = {dimension: [f"{dimension}_1"] for dimension in dimensiones}

# Crear un menú en la barra lateral
st.sidebar.title("Menú de opciones")
seleccion = st.sidebar.selectbox("Seleccione una dimensión para analizar:", dimensiones)

# Validar si la columna de la dimensión seleccionada existe
if columnas_dinamicas[seleccion][0] not in data.columns:
    st.error(f"La columna {columnas_dinamicas[seleccion][0]} no existe en los datos. Verifica el archivo.")
    st.stop()

# Datos filtrados para la dimensión seleccionada
datos_dimension = data[columnas_dinamicas[seleccion]]

# Calcular promedio para la dimensión seleccionada
promedio_dimension = datos_dimension.mean()[0]

# Crear gráfico radar
fig = px.line_polar(
    r=[promedio_dimension],
    theta=[seleccion],
    line_close=True,
    title=f"Radar de la dimensión: {seleccion}",
)
st.plotly_chart(fig)

# Mostrar comentarios relacionados con la dimensión
comentarios_columna = f"Comentario_1"  # Ajustado para el archivo proporcionado
if comentarios_columna in data.columns:
    st.write(f"Comentarios para la dimensión '{seleccion}':")
    st.write(data[comentarios_columna].dropna().tolist())
else:
    st.warning(f"No se encontró una columna de comentarios asociada ({comentarios_columna}).")

# Campo abierto para observaciones
observacion = st.text_area("Deje sus observaciones sobre esta dimensión:")
if st.button("Guardar observación"):
    st.success(f"¡Observación guardada!: {observacion}")
