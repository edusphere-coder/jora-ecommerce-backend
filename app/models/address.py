from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class AddressType(str, enum.Enum):
    SHIPPING = "shipping"
    BILLING = "billing"

class Address(Base):
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(SQLEnum(AddressType), nullable=False)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=False)
    country = Column(String(100), default="India", nullable=False)
    is_default = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="addresses")
