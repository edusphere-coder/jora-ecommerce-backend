from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
from app.schemas import ProductResponse, ProductCreate, ProductUpdate
from app.models.product import Product
from app.models.product_variant import ProductVariant
from app.dependencies import get_admin_user
from app.models.user import User

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 20,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Get all products with optional filters"""
    query = db.query(Product).filter(Product.is_active == True)
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if search:
        query = query.filter(
            or_(
                Product.name.contains(search),
                Product.description.contains(search)
            )
        )
    
    if min_price:
        query = query.filter(Product.base_price >= min_price)
    
    if max_price:
        query = query.filter(Product.base_price <= max_price)
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{slug}", response_model=ProductResponse)
async def get_product(slug: str, db: Session = Depends(get_db)):
    """Get product by slug"""
    product = db.query(Product).filter(Product.slug == slug).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Create a new product (Admin only)"""
    # Check if slug already exists
    existing = db.query(Product).filter(Product.slug == product_data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product slug already exists")
    
    # Create product
    product = Product(
        name=product_data.name,
        slug=product_data.slug,
        description=product_data.description,
        fabric_details=product_data.fabric_details,
        care_instructions=product_data.care_instructions,
        base_price=product_data.base_price,
        discount_percentage=product_data.discount_percentage,
        category_id=product_data.category_id
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # Create variants
    for variant_data in product_data.variants:
        variant = ProductVariant(
            product_id=product.id,
            sku=variant_data.sku,
            size=variant_data.size,
            color=variant_data.color,
            stock_quantity=variant_data.stock_quantity,
            price_override=variant_data.price_override,
            images=variant_data.images
        )
        db.add(variant)
    
    db.commit()
    db.refresh(product)
    
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Update product (Admin only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update fields
    for field, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Delete product (Admin only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return None
