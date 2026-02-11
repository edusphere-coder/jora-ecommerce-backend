from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Cart(Base):
    __tablename__ = "cart"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_variant_id = Column(Integer, ForeignKey("product_variants.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="cart_items")
    variant = relationship("ProductVariant", back_populates="cart_items")

class Wishlist(Base):
    __tablename__ = "wishlist"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(CHAR(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="wishlist_items")
    product = relationship("Product", back_populates="wishlist_items")
