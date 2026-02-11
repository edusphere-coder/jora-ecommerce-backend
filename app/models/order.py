from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.database import Base

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(CHAR(36), ForeignKey("users.id", ondelete="SET NULL"))
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    payment_status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    payment_method = Column(String(50))
    payment_id = Column(String(255))  # Gateway payment ID
    
    subtotal = Column(Numeric(10, 2), nullable=False)
    shipping_cost = Column(Numeric(10, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    discount_amount = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), nullable=False)
    
    shipping_address_id = Column(Integer, ForeignKey("addresses.id", ondelete="SET NULL"))
    billing_address_id = Column(Integer, ForeignKey("addresses.id", ondelete="SET NULL"))
    
    tracking_number = Column(String(100))
    notes = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(CHAR(36), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_variant_id = Column(Integer, ForeignKey("product_variants.id", ondelete="SET NULL"))
    product_name = Column(String(255), nullable=False)  # Store name for history
    variant_details = Column(String(255))  # Store size/color for history
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    variant = relationship("ProductVariant", back_populates="order_items")
