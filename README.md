API de Gestión de Etiquetas

Este proyecto es una API RESTful desarrollada con FastAPI utilizando funciones SÍNCRONAS, para gestionar etiquetas de productos. Permite realizar operaciones CRUD sobre una base de datos PostgreSQL que almacena información sobre las etiquetas.
El código Python cumple con los estándares de estilo establecidos por flake8 (algunos de los exigidos por el PEP8), validado automáticamente mediante pre-commit.

Características:
- Obtener todas las etiquetas: Recupera todas las etiquetas almacenadas en la base de datos.
- Obtener una etiqueta por ID: Recupera los detalles de una etiqueta específica.
- Crear una nueva etiqueta: Permite agregar una nueva etiqueta a la base de datos.
- Actualizar una etiqueta existente: Modifica los detalles de una etiqueta existente.
- Eliminar una etiqueta: Elimina una etiqueta específica de la base de datos.

Tecnologías utilizadas:
- Python: Lenguaje de programación principal.
- FastAPI: Framework para construir la API.
- PostgreSQL: Base de datos relacional para almacenar las etiquetas.
- Pydantic: Validación de datos y definición de modelos.
- psycopg2: Conector para interactuar con PostgreSQL.

Requisitos:
- Python 3.9 o superior
- PostgreSQL
- Entorno virtual configurado con las dependencias del archivo requirements.txt

Instalación:

1. Clona este repositorio:
git clone https://github.com/Cmpresiga/API_rotulos.git

2. Crea y activa un entorno virtual:
- python -m venv env
- env/Scripts/activate  # En Windows
- source env/bin/activate      # En Linux/Mac

3. Instala las dependencias:
pip install -r requirements.txt

4. Configura tu base de datos PostgreSQL con las credenciales adecuadas.

5. Ejecuta la aplicación:
uvicorn main:app --reload

Endpoints:
- GET /labels: Obtiene todas las etiquetas.
- GET /label/{id}: Obtiene una etiqueta por su ID.
- POST /label: Crea una nueva etiqueta.
- PUT /label/{id}: Actualiza una etiqueta existente.
- DELETE /label/{id}: Elimina una etiqueta por su ID.

Contribuciones:
¡Las contribuciones son bienvenidas! Si encuentras un problema o tienes una mejora, no dudes en abrir un issue o enviar un pull request.