import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Cargar el archivo
uploaded_file = "Informe_Ejecutivos v.8.xlsx"

# Cargar los datos del archivo Excel
data = pd.read_excel(uploaded_file)

# Reemplazar columnas con sufijos dinámicos
# Asumimos que hay tres conjuntos de evaluaciones (_1, _2, _3)
sufijos = ["_1", "_2", "_3"]
columnas_base = ["Actitud", "Conocimiento", "Argumentación", "Confiabilidad"]
columnas_mapeadas = {f"{col}{suf}": col for col in columnas_base for suf in sufijos}

# Renombrar las columnas para simplificar
data.rename(columns=columnas_mapeadas, inplace=True)

# Crear un selector para elegir la dimensión
dimensiones = list(columnas_base)
seleccion = st.selectbox("Seleccione una dimensión para analizar:", dimensiones)

# Filtrar los datos de la dimensión seleccionada
datos_dimension = data[[f"{seleccion}_1", f"{seleccion}_2", f"{seleccion}_3"]]

# Calcular promedios
promedios = datos_dimension.mean(axis=0)

# Mostrar un gráfico de radar
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
valores = list(promedios.values) + [promedios.values[0]]  # Cerrar el gráfico
etiquetas = list(datos_dimension.columns) + [datos_dimension.columns[0]]  # Etiquetas del gráfico
angulos = [n / float(len(valores)) * 2 * 3.14159 for n in range(len(valores))]
ax.plot(angulos, valores, linewidth=2, linestyle='solid')
ax.fill(angulos, valores, alpha=0.4)
ax.set_yticks([])
ax.set_xticks(angulos[:-1])
ax.set_xticklabels(etiquetas)
st.pyplot(fig)

# Campo de observaciones
observaciones = st.text_area("Observaciones:")
st.write("Sus observaciones son:")
st.write(observaciones)
