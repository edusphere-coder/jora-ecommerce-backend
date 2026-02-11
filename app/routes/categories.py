from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import CategoryCreate, CategoryResponse
from app.models.category import Category
from app.dependencies import get_admin_user
from app.models.user import User

router = APIRouter(prefix="/api/categories", tags=["Categories"])

@router.get("", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    """Get all categories"""
    categories = db.query(Category).order_by(Category.display_order).all()
    return categories

@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Create a new category (Admin only)"""
    category = Category(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
