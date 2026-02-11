from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import CartItemAdd, CartItemUpdate, CartItemResponse
from app.models.cart import Cart
from app.models.product_variant import ProductVariant
from app.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/api/cart", tags=["Cart"])

@router.get("", response_model=List[CartItemResponse])
async def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's cart items"""
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    return cart_items

@router.post("/add", response_model=CartItemResponse, status_code=201)
async def add_to_cart(
    item: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Add item to cart"""
    # Check if variant exists
    variant = db.query(ProductVariant).filter(ProductVariant.id == item.product_variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Product variant not found")
    
    # Check stock
    if variant.stock_quantity < item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Check if item already in cart
    existing_item = db.query(Cart).filter(
        Cart.user_id == current_user.id,
        Cart.product_variant_id == item.product_variant_id
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        # Add new item
        cart_item = Cart(
            user_id=current_user.id,
            product_variant_id=item.product_variant_id,
            quantity=item.quantity
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item

@router.put("/{cart_item_id}", response_model=CartItemResponse)
async def update_cart_item(
    cart_item_id: int,
    item_update: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update cart item quantity"""
    cart_item = db.query(Cart).filter(
        Cart.id == cart_item_id,
        Cart.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Check stock
    if cart_item.variant.stock_quantity < item_update.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    cart_item.quantity = item_update.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/{cart_item_id}", status_code=204)
async def remove_from_cart(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Remove item from cart"""
    cart_item = db.query(Cart).filter(
        Cart.id == cart_item_id,
        Cart.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    return None

@router.delete("", status_code=204)
async def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Clear all items from cart"""
    db.query(Cart).filter(Cart.user_id == current_user.id).delete()
    db.commit()
    return None
