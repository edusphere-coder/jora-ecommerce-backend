from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class DiscountType(str, enum.Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

class Coupon(Base):
    __tablename__ = "coupons"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    discount_type = Column(SQLEnum(DiscountType), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=False)
    min_order_value = Column(Numeric(10, 2), default=0)
    max_discount = Column(Numeric(10, 2))  # Max discount for percentage type
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    usage_limit = Column(Integer)  # Null = unlimited
    used_count = Column(Integer, default=0)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
