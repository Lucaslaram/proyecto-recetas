from fastapi import FastAPI
from app.models import Base, engine
from app.routers import ingredients_router, recipes_router

# Crear las tablas automáticamente al iniciar la app
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Generador de Recetas",
    description="API para generar recetas con IA a partir de tu inventario",
    version="1.0.0"
)

# Incluir los endpoints del sistema
app.include_router(ingredients_router)
app.include_router(recipes_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}