Secure API Lab
Laboratorio práctico de backend e infraestructura construido con FastAPI, PostgreSQL, 
Docker Compose y Nginx. El proyecto está orientado a aprendizaje técnico progresivo 
en contenedores, observabilidad básica, variables de entorno, troubleshooting y buenas prácticas 
de seguridad como ejecución con usuario no root.

Arquitectura
FastAPI como servicio API.

PostgreSQL 16 como base de datos relacional con volumen persistente.

Nginx como reverse proxy expuesto al host por el puerto 80.

Docker Compose para orquestar servicios, red interna y healthchecks.

text
Cliente
  |
  v
Nginx (:80)
  |
  v
FastAPI (:8000, red interna)
  |
  v
PostgreSQL (:5432, red interna)
Objetivos del proyecto
Practicar dockerización de una API Python.

Conectar servicios por nombre interno usando Compose.

Gestionar configuración con .env.

Implementar un endpoint de salud para API y base de datos.

Añadir logging de requests y trazas de error.

Ejecutar el contenedor API con usuario no root.

Estructura sugerida

secure-api-lab/
├── api/
│   ├── app/
│   │   ├── main.py
│   │   └── db.py
│   ├── Dockerfile
│   └── requirements.txt
├── nginx/
│   └── default.conf
├── docker-compose.yml
├── .env
└── .gitignore
Requisitos
macOS o Linux.

Docker Desktop o Docker Engine con Compose.
Python 3 y entorno virtual local para desarrollo.
Git y VS Code opcionalmente para edición y control de versiones.

Variables de entorno
Crear un archivo .env en la raíz del proyecto:


POSTGRES_USER=secureapi
POSTGRES_PASSWORD=changeme123
POSTGRES_DB=secureapidb
DATABASE_URL=postgresql://secureapi:changeme123@db:5432/secureapidb

Docker Compose puede cargar automáticamente variables desde un archivo .env ubicado 
junto al docker-compose.yml, y esas variables pueden reutilizarse dentro de la definición 
de servicios.

Levantar el proyecto

cd ~/Projects/secure-api-lab
source .venv/bin/activate
docker compose up -d --build
Verificar estado:


docker compose ps
docker compose logs api
docker compose logs db
docker compose logs nginx
El uso de healthchecks y dependencias entre servicios ayuda a evitar que la API arranque 
antes de que PostgreSQL esté listo para aceptar conexiones.

Endpoints disponibles
Endpoint	Método	Descripción
/	GET	Respuesta base del servicio API.
/health	GET	Estado básico de la API.
/health/db	GET	Verifica conexión a PostgreSQL.
/docs	GET	Documentación Swagger UI generada por FastAPI.
/boom	GET	Endpoint de error controlado para practicar logs y manejo de excepciones.
FastAPI genera documentación interactiva automáticamente en /docs, lo que facilita validar endpoints durante desarrollo y pruebas locales.

Seguridad básica aplicada
API ejecutándose como usuario no root dentro del contenedor.

Nginx como único servicio expuesto al host.

PostgreSQL y FastAPI comunicándose por red interna de Docker.

Uso de .gitignore para evitar subir .env y .venv/ al repositorio.

Observabilidad
El proyecto incluye logging básico por request con duración en milisegundos y un endpoint
 de error (/boom) para practicar lectura de trazas. FastAPI permite además definir handlers 
 personalizados para devolver respuestas JSON consistentes cuando ocurren excepciones de 
 aplicación.

Ejemplo de flujo útil de diagnóstico:


docker compose logs -f api
curl http://127.0.0.1/health
curl http://127.0.0.1/health/db
curl http://127.0.0.1/boom

Errores aprendidos
Durante el desarrollo se documentaron errores relacionados con versiones inválidas de pip, 
contexto incorrecto del Dockerfile, typos en variables de entorno, nombres de base de datos, 
indentación YAML, orden de definición de app en FastAPI y configuración del intérprete en VS Code.
Todos esos casos quedaron registrados en una bitácora separada para reutilizarlos como 
aprendizaje técnico y evidencia de troubleshooting.