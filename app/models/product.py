from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, Boolean, DateTime
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    name = Column(String(255), nullable=False)
    slug = Column(String(300), unique=True, nullable=False, index=True)
    description = Column(Text)
    fabric_details = Column(Text)
    care_instructions = Column(Text)
    base_price = Column(Numeric(10, 2), nullable=False)
    discount_percentage = Column(Numeric(5, 2), default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    wishlist_items = relationship("Wishlist", back_populates="product")
