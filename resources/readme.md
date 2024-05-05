# Energy Consumption API

Este proyecto implementa una API para gestionar datos de consumo de energía utilizando FastAPI y MongoDB.

## Instalación

1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener Python instalado.
3. Instala las dependencias del proyecto ejecutando `pip install -r requirements.txt`.

## Uso

1. Asegúrate de tener una instancia de MongoDB en ejecución.
2. Configura la conexión a MongoDB en el archivo `api_manager.py`.
3. Ejecuta el archivo `main.py` para iniciar el servidor de la API, esto automáticamente volcará los datos existentes en el CSV a la base de datos MongoDB, y se añadirán datos nuevos tanto al CSV como a la MongoDB en caso de que estos sean introducidos exitosamente.
4. Ejecuta el archivo `main.py` .
5. Accede a la API a través de `http://localhost:8000`.

## Decisiones Técnicas

- **FastAPI**: Se utiliza FastAPI como framework web debido a su velocidad y facilidad de uso.
- **MongoDB**: Se elige MongoDB como base de datos debido a su flexibilidad y escalabilidad para datos no estructurados.
- **Pandas**: Se utiliza la librería Pandas para el manejo de datos en formato CSV.

## Siguientes Pasos

A continuación se presentan algunas mejoras que podrían realizarse en la aplicación:

1. **Diferentes tipos de gráficos**: Implementación del tipo de gráfico más adecuado al dato que se está observando.
2. **Optimización de Consultas**: Optimizar las consultas a la base de datos para mejorar el rendimiento de la aplicación.
3. **Manejo de Errores**: Mejorar el manejo de errores para proporcionar mensajes de error más descriptivos.

¡Gracias por utilizar nuestra aplicación!
