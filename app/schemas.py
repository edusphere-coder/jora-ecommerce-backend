from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    role: UserRole
    is_verified: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

# Token Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

# Address Schemas
class AddressBase(BaseModel):
    type: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    country: str = "India"
    is_default: bool = False

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: int
    user_id: str
    
    model_config = ConfigDict(from_attributes=True)

# Product Schemas
class ProductVariantBase(BaseModel):
    sku: str
    size: str
    color: str
    stock_quantity: int
    price_override: Optional[float] = None
    images: Optional[list[str]] = None

class ProductVariantCreate(ProductVariantBase):
    pass

class ProductVariantResponse(ProductVariantBase):
    id: int
    product_id: str
    
    model_config = ConfigDict(from_attributes=True)

class ProductBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    fabric_details: Optional[str] = None
    care_instructions: Optional[str] = None
    base_price: float
    discount_percentage: float = 0
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    variants: list[ProductVariantCreate] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    fabric_details: Optional[str] = None
    care_instructions: Optional[str] = None
    base_price: Optional[float] = None
    discount_percentage: Optional[float] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: str
    is_active: bool
    created_at: datetime
    variants: list[ProductVariantResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None
    display_order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Cart Schemas
class CartItemAdd(BaseModel):
    product_variant_id: int
    quantity: int = Field(ge=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)

class CartItemResponse(BaseModel):
    id: int
    product_variant_id: int
    quantity: int
    variant: ProductVariantResponse
    
    model_config = ConfigDict(from_attributes=True)

# Order Schemas
class OrderItemCreate(BaseModel):
    product_variant_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: list[OrderItemCreate]
    shipping_address_id: int
    billing_address_id: int
    coupon_code: Optional[str] = None

class OrderItemResponse(BaseModel):
    id: int
    product_name: str
    variant_details: str
    quantity: int
    unit_price: float
    total_price: float
    
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: str
    order_number: str
    status: str
    payment_status: str
    subtotal: float
    shipping_cost: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    created_at: datetime
    items: list[OrderItemResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# Coupon Schemas
class CouponCreate(BaseModel):
    code: str
    discount_type: str
    discount_value: float
    min_order_value: float = 0
    max_discount: Optional[float] = None
    valid_from: datetime
    valid_until: datetime
    usage_limit: Optional[int] = None

class CouponResponse(BaseModel):
    id: int
    code: str
    discount_type: str
    discount_value: float
    min_order_value: float
    max_discount: Optional[float]
    valid_from: datetime
    valid_until: datetime
    
    model_config = ConfigDict(from_attributes=True)

# B2B Schemas
class B2BRegistration(BaseModel):
    business_name: str
    gst_number: Optional[str] = None

class B2BResponse(BaseModel):
    id: int
    business_name: str
    gst_number: Optional[str]
    approval_status: str
    discount_tier: float
    moq_requirement: int
    
    model_config = ConfigDict(from_attributes=True)
