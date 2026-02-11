from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class ApprovalStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class B2BCustomer(Base):
    __tablename__ = "b2b_customers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    business_name = Column(String(255), nullable=False)
    gst_number = Column(String(20), unique=True)
    approval_status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING, nullable=False)
    discount_tier = Column(Numeric(5, 2), default=0)  # Percentage discount
    moq_requirement = Column(Integer, default=10)  # Minimum order quantity
    credit_limit = Column(Numeric(12, 2))
    
    # Relationships
    user = relationship("User", back_populates="b2b_profile")
