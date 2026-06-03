from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.models import Base, engine

# Crear de forma automática todas las tablas registradas en el __init__
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Generador de Recetas",
    description="API para generar recetas con IA a partir de tu inventario",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}