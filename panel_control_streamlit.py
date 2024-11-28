import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Archivo Excel en el mismo repositorio
uploaded_file = "Informe_Ejecutivos_v.8"  # Nombre exacto del archivo
data = pd.read_excel(uploaded_file)


# Asegurarnos de que las columnas necesarias existan
required_columns = [
    'Supervisor', 'Ejecutivo', 'Comentario',
    'Actitud', 'Conocimiento', 'Argumentación',
    'Confiabilidad', 'Claridad', 'Seguridad'
]

if not all(col in data.columns for col in required_columns):
    st.error("La base de datos no tiene las columnas necesarias.")
    st.stop()

# Filtrar los datos según el supervisor y ejecutivo seleccionados
st.sidebar.header("Filtros")
selected_supervisor = st.sidebar.selectbox("Seleccione un Supervisor", data['Supervisor'].unique())
filtered_executives = data[data['Supervisor'] == selected_supervisor]['Ejecutivo'].unique()
selected_executive = st.sidebar.selectbox("Seleccione un Ejecutivo", filtered_executives)

# Filtrar los datos del ejecutivo seleccionado
filtered_data = data[(data['Supervisor'] == selected_supervisor) & (data['Ejecutivo'] == selected_executive)]

if not filtered_data.empty:
    st.title(f"Evaluación de {selected_executive}")
    
    # Mostrar comentario del ejecutivo
    comentario = filtered_data['Comentario'].iloc[0]
    st.markdown(f"**Observación:** {comentario}")
    
    # Gráfico de radar
    st.markdown("### Evaluación: Gráfico de Radar")
    dimensions = ['Actitud', 'Conocimiento', 'Argumentación', 'Confiabilidad', 'Claridad', 'Seguridad']
    values = filtered_data[dimensions].iloc[0].values

    # Crear el gráfico de radar
    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    values = np.concatenate((values, [values[0]]))  # Cerrar el gráfico
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=1)

    ax.set_yticks(range(1, 11))
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, fontsize=6)

    st.pyplot(fig)

else:
    st.warning("No hay datos disponibles para los filtros seleccionados.")
