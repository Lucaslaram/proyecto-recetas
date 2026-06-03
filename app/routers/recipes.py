import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import get_db, Recipe, User
from app.schemas import RecipeResponse, RecipeRate
from app.routers.auth_deps import get_current_user

router = APIRouter(
    prefix="/recipes",
    tags=["Recetas"]
)

def format_recipe_response(recipe: Recipe) -> RecipeResponse:
    """
    Función utilitaria para convertir los campos de texto (JSON string) 
    de la base de datos en listas reales antes de enviarlos al cliente.
    """
    try:
        ingredientes_list = json.loads(recipe.ingredientes)
    except Exception:
        ingredientes_list = [i.strip() for i in recipe.ingredientes.split("\n") if i.strip()]

    try:
        pasos_list = json.loads(recipe.pasos)
    except Exception:
        pasos_list = [p.strip() for p in recipe.pasos.split("\n") if p.strip()]

    return RecipeResponse(
        id=recipe.id,
        nombre_plato=recipe.nombre_plato,
        ingredientes=ingredientes_list,
        pasos=pasos_list,
        tiempo_estimado=recipe.tiempo_estimado,
        nivel_dificultad=recipe.nivel_dificultad,
        rating=recipe.rating,
        user_id=recipe.user_id,
        created_at=recipe.created_at
    )


@router.get("", response_model=list[RecipeResponse])
def get_recipes_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ver el historial completo de recetas generadas por el usuario autenticado.
    """
    recipes = db.query(Recipe).filter(Recipe.user_id == current_user.id).order_by(Recipe.created_at.desc()).all()
    return [format_recipe_response(recipe) for recipe in recipes]


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Elimina una receta específica del historial del usuario, validando su propiedad.
    """
    db_recipe = db.query(Recipe).filter(Recipe.id == id, Recipe.user_id == current_user.id).first()
    
    if not db_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La receta no existe en tu historial."
        )
        
    db.delete(db_recipe)
    db.commit()
    return None


@router.post("/{id}/rate", response_model=RecipeResponse)
def rate_recipe(
    id: int,
    rate_in: RecipeRate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Califica una receta existente de 1 a 5 estrellas. 
    Valida la existencia y la pertenencia al usuario actual.
    """
    db_recipe = db.query(Recipe).filter(Recipe.id == id, Recipe.user_id == current_user.id).first()
    
    if not db_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La receta no existe en tu historial."
        )
    
    # Asignar la nueva calificación (Pydantic ya validó que esté entre 1 y 5)
    db_recipe.rating = rate_in.rating
    
    db.commit()
    db.refresh(db_recipe)
    return format_recipe_response(db_recipe)