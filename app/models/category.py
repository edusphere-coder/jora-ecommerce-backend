from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(150), unique=True, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    description = Column(Text)
    image_url = Column(String(500))
    display_order = Column(Integer, default=0)
    
    # Self-referential relationship for subcategories
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    
    # Products in this category
    products = relationship("Product", back_populates="category")
