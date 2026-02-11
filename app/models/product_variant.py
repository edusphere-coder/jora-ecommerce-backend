from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, JSON
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from app.database import Base

class ProductVariant(Base):
    __tablename__ = "product_variants"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(CHAR(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    size = Column(String(20), nullable=False)
    color = Column(String(50), nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    price_override = Column(Numeric(10, 2))  # Optional price override for specific variants
    images = Column(JSON)  # Array of image URLs
    
    # Relationships
    product = relationship("Product", back_populates="variants")
    cart_items = relationship("Cart", back_populates="variant")
    order_items = relationship("OrderItem", back_populates="variant")
