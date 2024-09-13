import streamlit as st
import numpy as np
import joblib
import pandas as pd
from datetime import date


def neg_log(x):
    return -np.log1p(x)


def inverse_neg_log(x):
    return np.expm1(-x)


region_mapping = {
    1: "Tarapacá",
    2: "Antofagasta",
    3: "Atacama",
    4: "Coquimbo",
    5: "Valparaíso",
    6: "O’Higgins",
    7: "Maule",
    8: "Biobío",
    9: "La Araucanía",
    10: "Los Lagos",
    11: "Aysén",
    12: "Magallanes",
    13: "Metropolitana",
    14: "Los Ríos",
    15: "Arica y Parinacota",
    16: "Ñuble",
}

df = pd.read_csv("notebooks/car_data_clean.csv")

# Cargar el modelo serializado
model = joblib.load("notebooks/model.pkl")

# Título de la app
st.title("Predicción de Precio de Autos")

# Sección para ingresar los datos del auto
st.header("Ingrese los detalles del auto")


# Entrada de datos categóricos
marca = st.selectbox("Marca del Auto", df.marca.unique())
modelo = st.selectbox("Modelo del Auto", df[df.marca == marca].modelo.unique())
combustible = st.selectbox("Tipo de Combustible", df.combustible.dropna().unique())
transmision = st.selectbox("Tipo de Transmisión", df.transmision.dropna().unique())
region = st.selectbox("Región", region_mapping.values())

motor = st.select_slider("Cilindrada del Motor (lt)", [i / 10.0 for i in range(10, 61)])
kilometraje = st.number_input(
    "Kilometraje (km)", min_value=0, max_value=500000, value=50000
)
anio = st.number_input(
    "Año del Auto", min_value=2000, max_value=date.today().year, value=2015
)

# Procesamiento de los datos
user_inputs = {
    "motor": motor,
    "kilometraje": kilometraje,
    "año": anio,
    "marca": marca,
    "modelo": modelo,
    "combustible": combustible,
    "transmision": transmision,
    "region": region,
}

# Botón para predecir
if st.button("Predecir Precio"):
    # Organizar los datos en el formato adecuado para el modelo
    input_array = np.array(
        [[motor, kilometraje, anio, marca, modelo, combustible, transmision, region]]
    )

    input_data = pd.DataFrame(data=user_inputs, index=[0])

    # Realizar la predicción
    predicted_price = model.predict(input_data)[0]

    # Mostrar el resultado
    st.success(
        f"El precio estimado del auto es: ${predicted_price:,.2f} millones de pesos"
    )
