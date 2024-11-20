import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial de página
st.set_page_config(
    page_title="SPOT-IDA Spain Prices",
    page_icon="⚡",
    layout="wide"
)

# Estilo CSS
st.markdown("""
<style>
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}
[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}
[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}
[data-testid="stMetricLabel"] {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

# Caching de la carga de datos
@st.cache_data
def load_data(file_path_parquet):
    return pd.read_parquet(file_path_parquet, engine='pyarrow')

# Carga de datos
path_parquet = './prcs_spot_ida_spain.parquet'
data = load_data(file_path_parquet=path_parquet)

# Convertir a formato de fecha si es necesario
data['FECHA'] = pd.to_datetime(data['FECHA'])

# Crear una nueva columna 'FECHA_HORA' combinando 'FECHA' y 'PERIODO'
data['FECHA_HORA'] = data['FECHA'] + pd.to_timedelta(data['PERIODO'], unit='h')

# Interfaz de usuario
st.title("Precios del Mercado Eléctrico")
# st.sidebar.header("Filtros")

# Rango de fechas con slider
min_date = data['FECHA'].min().date()
max_date = data['FECHA'].max().date()
date_range = st.date_input('Seleccione un rango de fechas:', [min_date, max_date])

# Validación del rango de fechas
if len(date_range) != 2:
    st.error("Seleccione un rango de fechas válido.")
else:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])

    # Filtrar datos
    filtered_data = data[(data['FECHA'] >= start_date) & 
                        (data['FECHA'] <= end_date)]

    # Mostrar resultados
    if filtered_data.empty:
        st.warning("No hay datos disponibles para el rango seleccionado.")
    else:
        # Gráfica interactiva
        # st.subheader("Gráfica de precios")
        fig = px.line(
            filtered_data.reset_index(),  # Resetear índice para Plotly
            x="FECHA_HORA",  # Utilizar la columna generada al resetear índice
            y="PRECIO_EUR", 
            color="SESION",  # Colorear por sesión
            title="SPOT-IDA Spain Prices", 
            labels={
                "PRECIO_EUR": "Precio (€)", 
                "FECHA_HORA": "Fecha y hora",
                "SESION": "Sesión"
            }
        )
        fig.update_traces(mode='lines+markers')
        fig.update_layout(
            autosize=True,  # Activar ajuste automático del tamaño
            margin=dict(l=0, r=0, t=40, b=40),  # Eliminar márgenes para ocupar todo el espacio
            height=800  # Ajustar el alto de la gráfica para que ocupe más espacio
        ) 
        st.plotly_chart(fig, use_container_width=True)