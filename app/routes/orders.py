from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.schemas import OrderCreate, OrderResponse
from app.models.order import Order, OrderItem, OrderStatus, PaymentStatus
from app.models.product_variant import ProductVariant
from app.models.coupon import Coupon
from app.dependencies import get_current_active_user, get_admin_user
from app.models.user import User
import random
import string

router = APIRouter(prefix="/api/orders", tags=["Orders"])

def generate_order_number() -> str:
    """Generate unique order number"""
    timestamp = datetime.now().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.digits, k=6))
    return f"JORA{timestamp}{random_str}"

@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new order"""
    # Calculate totals
    subtotal = 0
    order_items_data = []
    
    for item in order_data.items:
        variant = db.query(ProductVariant).filter(ProductVariant.id == item.product_variant_id).first()
        if not variant:
            raise HTTPException(status_code=404, detail=f"Variant {item.product_variant_id} not found")
        
        if variant.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {variant.sku}")
        
        price = variant.price_override or variant.product.base_price
        total_price = price * item.quantity
        subtotal += total_price
        
        order_items_data.append({
            "variant": variant,
            "quantity": item.quantity,
            "unit_price": price,
            "total_price": total_price
        })
    
    # Apply coupon if provided
    discount_amount = 0
    if order_data.coupon_code:
        coupon = db.query(Coupon).filter(Coupon.code == order_data.coupon_code).first()
        if coupon and coupon.is_active and coupon.valid_from <= datetime.utcnow() <= coupon.valid_until:
            if subtotal >= coupon.min_order_value:
                if coupon.discount_type == "percentage":
                    discount_amount = subtotal * (coupon.discount_value / 100)
                    if coupon.max_discount:
                        discount_amount = min(discount_amount, coupon.max_discount)
                else:
                    discount_amount = coupon.discount_value
    
    # Calculate tax and shipping
    tax_amount = (subtotal - discount_amount) * 0.18  # 18% GST
    shipping_cost = 0 if subtotal > 1000 else 100  # Free shipping above 1000
    total_amount = subtotal + tax_amount + shipping_cost - discount_amount
    
    # Create order
    order = Order(
        order_number=generate_order_number(),
        user_id=current_user.id,
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        tax_amount=tax_amount,
        discount_amount=discount_amount,
        total_amount=total_amount,
        shipping_address_id=order_data.shipping_address_id,
        billing_address_id=order_data.billing_address_id
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Create order items and update stock
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_variant_id=item_data["variant"].id,
            product_name=item_data["variant"].product.name,
            variant_details=f"{item_data['variant'].size} / {item_data['variant'].color}",
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"],
            total_price=item_data["total_price"]
        )
        db.add(order_item)
        
        # Update stock
        item_data["variant"].stock_quantity -= item_data["quantity"]
    
    db.commit()
    db.refresh(order)
    
    return order

@router.get("", response_model=List[OrderResponse])
async def get_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all orders for current user"""
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get order details"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cancel an order"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
        raise HTTPException(status_code=400, detail="Order cannot be cancelled")
    
    order.status = OrderStatus.CANCELLED
    
    # Restore stock
    for item in order.items:
        if item.variant:
            item.variant.stock_quantity += item.quantity
    
    db.commit()
    db.refresh(order)
    
    return order

@router.put("/{order_id}/status")
async def update_order_status(
    order_id: str,
    status: OrderStatus,
    tracking_number: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Update order status (Admin only)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    if tracking_number:
        order.tracking_number = tracking_number
    
    db.commit()
    db.refresh(order)
    
    return order
