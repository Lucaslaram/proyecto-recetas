from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models import get_db, Ingredient, User
from app.schemas import IngredientCreate, IngredientResponse
from app.routers.auth_deps import get_current_user

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredientes"]
)

@router.post("", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
def create_ingredient(
    ingredient_in: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Agrega un nuevo ingrediente al inventario personal del usuario autenticado.
    """
    db_ingredient = Ingredient(
        nombre=ingredient_in.nombre,
        cantidad=ingredient_in.cantidad,
        user_id=current_user.id
    )
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


@router.get("", response_model=list[IngredientResponse])
def get_ingredients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene todos los ingredientes que pertenecen exclusivamente al usuario autenticado.
    """
    ingredients = db.query(Ingredient).filter(Ingredient.user_id == current_user.id).all()
    return ingredients