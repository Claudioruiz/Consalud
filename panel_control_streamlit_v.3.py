
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Cargar los datos desde el archivo Excel
@st.cache
def load_data():
    return pd.read_excel("Informe_Ejecutivosv.10.xlsx")

df = load_data()

# Renombrar columnas para mayor claridad
df.rename(columns={'Nombre': 'Ejecutivo', 'Contacto': 'Nota Contacto', 'Reunión': 'Nota Reunión'}, inplace=True)

# Título y configuración de la página
st.set_page_config(page_title="Panel de Evaluación", layout="wide")
st.title("Panel Interactivo de Evaluación de Ejecutivos")

# Sidebar para filtros
st.sidebar.header("Filtros")
selected_supervisor = st.sidebar.selectbox("Seleccione un Supervisor", df['Supervisor'].unique())
filtered_executives = df[df['Supervisor'] == selected_supervisor]['Ejecutivo'].unique()
selected_executive = st.sidebar.selectbox("Seleccione un Ejecutivo", filtered_executives)

# Filtrar datos
filtered_data = df[(df['Supervisor'] == selected_supervisor) & (df['Ejecutivo'] == selected_executive)]

# Mostrar resultados
if not filtered_data.empty:
    st.subheader(f"Información para {selected_executive}")

    # Mostrar comentarios
    st.markdown("### Observaciones")
    st.markdown(filtered_data['Comentario'].iloc[0])

    # Mostrar notas
    st.markdown("#### Nota Contacto")
    st.write(filtered_data['Nota Contacto'].iloc[0])
    st.markdown("#### Nota Reunión")
    st.write(filtered_data['Nota Reunión'].iloc[0])

    # Crear gráfico de radar
    st.markdown("### Evaluación de Competencias")
    dimensions = ['Actitud', 'Conocimiento', 'Argumentación', 'Confiabilidad', 'Claridad', 'Seguridad']
    values = filtered_data[dimensions].iloc[0].values

    # Preparar ángulos para el gráfico de radar
    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    values = np.concatenate((values, [values[0]]))  # Cerrar el gráfico
    angles += angles[:1]

    # Configurar colores basados en Consalud (ejemplo: azul y verde)
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='#007BFF', alpha=0.25)
    ax.plot(angles, values, color='#007BFF', linewidth=2)
    ax.set_yticks(range(1, 11))
    ax.set_yticklabels([str(i) for i in range(1, 11)])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions)
    ax.set_title("Gráfico de Radar", va='bottom')

    st.pyplot(fig)
else:
    st.warning("No hay datos disponibles para los filtros seleccionados.")
