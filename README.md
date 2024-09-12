# Predicción de Precios de Vehículos Usados en Chile
Este proyecto busca desarrollar un modelo de machine learning para predecir los precios de vehículos usados en el mercado chileno. El enfoque principal es crear una herramienta que permita a compradores y vendedores estimar un precio justo basándose en datos históricos y características clave de los vehículos.

Tabla de Contenidos
- Descripción del Proyecto
- Tecnologías Utilizadas
- Instalación
- Estructura del Proyecto
- Uso
- Licencia
- Contacto


# Descripción del Proyecto
El mercado de autos usados en Chile presenta desafíos para estimar precios debido a múltiples variables como el modelo, kilometraje, año de fabricación, entre otros. Este proyecto utiliza técnicas de machine learning y data science para predecir los precios de vehículos usados basándose en datos recolectados de distintas plataformas como ChileAutos, Yapo.cl, y OLX.

Objetivos
- Recopilar datos a través de web scraping y APIs públicas.
- Procesar y limpiar los datos para eliminar inconsistencias y valores nulos.
- Entrenar modelos predictivos como Random Forest y XGBoost para estimar precios.
- Entregar los resultados de los modelos predictivos.

Tecnologías Utilizadas
- Python 3.8+
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Selenium/Scrapy

# Instalación
# Requisitos previos
Asegúrate de tener instaladas las siguientes herramientas en tu sistema:
- Python 3.8+
- Git

# Predicción de Precios de Vehículos Usados en Chile

Este proyecto busca desarrollar un modelo de machine learning para predecir los precios de vehículos usados en el mercado chileno. 

## Instalación

1. Clona el repositorio en tu máquina local:

   ```bash
   git clone https://github.com/tu-usuario/prediccion-precios-autos-usados.git
   cd prediccion-precios-autos-usados

2. Instala las dependencias de Python:

     ```bash
   pip install -r requirements.txt

# Estructura del Proyecto
     ```bash
     prediccion-precios-autos-usados/
    │
    ├── data/                     # Contiene los datasets recolectados
    ├── models/                   # Almacena los modelos entrenados
    ├── scraping/                 # Scripts para recolección de datos con Scrapy
    ├── notebooks/                # Jupyter Notebooks para análisis exploratorio
    ├── requirements.txt          # Dependencias de Python
    └── README.md                 # Este archivo

# Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.

# Contacto
- Nombre: Rodrigo Aguilera Vasconcellos
- Correo: raguilerav@udec.cl
- Proyecto desarrollado para: Universidad de Concepción, Magíster en Ciencia de Datos para la Innovación
