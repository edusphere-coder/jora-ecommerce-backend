from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import B2BRegistration, B2BResponse
from app.models.b2b import B2BCustomer
from app.models.user import User, UserRole
from app.dependencies import get_current_active_user, get_admin_user

router = APIRouter(prefix="/api/b2b", tags=["B2B"])

@router.post("/register", response_model=B2BResponse, status_code=201)
async def register_b2b(
    b2b_data: B2BRegistration,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Register as B2B customer"""
    # Check if already registered
    existing = db.query(B2BCustomer).filter(B2BCustomer.user_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already registered as B2B customer")
    
    b2b_customer = B2BCustomer(
        user_id=current_user.id,
        business_name=b2b_data.business_name,
        gst_number=b2b_data.gst_number
    )
    
    db.add(b2b_customer)
    db.commit()
    db.refresh(b2b_customer)
    
    return b2b_customer

@router.get("/profile", response_model=B2BResponse)
async def get_b2b_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get B2B profile"""
    b2b_profile = db.query(B2BCustomer).filter(B2BCustomer.user_id == current_user.id).first()
    if not b2b_profile:
        raise HTTPException(status_code=404, detail="B2B profile not found")
    
    return b2b_profile

@router.put("/{b2b_id}/approve")
async def approve_b2b(
    b2b_id: int,
    discount_tier: float = 10.0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Approve B2B customer (Admin only)"""
    b2b_customer = db.query(B2BCustomer).filter(B2BCustomer.id == b2b_id).first()
    if not b2b_customer:
        raise HTTPException(status_code=404, detail="B2B customer not found")
    
    b2b_customer.approval_status = "approved"
    b2b_customer.discount_tier = discount_tier
    
    # Update user role
    user = db.query(User).filter(User.id == b2b_customer.user_id).first()
    if user:
        user.role = UserRole.B2B
    
    db.commit()
    db.refresh(b2b_customer)
    
    return b2b_customer
