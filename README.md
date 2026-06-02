# 🍽 Generador de Recetas con IA

Aplicación web que permite registrar ingredientes disponibles y generar
recetas personalizadas usando inteligencia artificial.

## Stack
- **Backend:** Python + FastAPI
- **Base de datos:** PostgreSQL + SQLAlchemy + Alembic
- **IA:** OpenRouter (Mistral 7B)
- **Despliegue:** Docker + Docker Compose + VPS + SSL

## Levantar en desarrollo

```bash
cp .env.example .env
# Editar .env con tus valores reales
docker compose up --build
```

La API queda disponible en http://localhost:8000
Documentación automática en http://localhost:8000/docs

## Correr pruebas

```bash
pip install -r requirements.txt
pytest -v
```

## Equipo
- Daniel Morales
- Michael Borrego
- Daniel De La Hoz
- Lucas Lara
- Frank Llerena
- Alberto Castro
