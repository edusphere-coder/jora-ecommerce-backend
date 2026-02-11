# JORA E-commerce Backend API

A luxury clothing brand e-commerce platform built with FastAPI, MySQL, and modern Python technologies.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/edusphere-coder/jora-ecommerce-backend.git
   cd jora-ecommerce-backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   ```

5. **Set up the database**
   - Create a MySQL database named `jora_ecommerce`
   - Update the `DATABASE_URL` in `.env` with your MySQL credentials

6. **Run the application**
   ```bash
   # Development server with auto-reload
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive API Docs: `http://localhost:8000/api/docs`
   - ReDoc Documentation: `http://localhost:8000/api/redoc`

## 📋 Environment Variables

The `.env.example` file contains all required environment variables. Copy it to `.env` and configure:

### Database Configuration
- `DATABASE_URL`: MySQL connection string
  - Format: `mysql+mysqlconnector://username:password@host:port/database`
  - Example: `mysql+mysqlconnector://jora_user:jora_password@localhost:3306/jora_ecommerce`

### Authentication & Security
- `SECRET_KEY`: JWT secret key (minimum 32 characters, change in production)
- `ALGORITHM`: JWT algorithm (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration time (default: `30`)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration time (default: `7`)

### CORS Configuration
- `FRONTEND_URL`: Frontend application URL (default: `http://localhost:3000`)

### Payment Gateways
- **Razorpay**
  - `RAZORPAY_KEY_ID`: Your Razorpay API key
  - `RAZORPAY_KEY_SECRET`: Your Razorpay secret key

- **Stripe**
  - `STRIPE_SECRET_KEY`: Your Stripe secret key
  - `STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key

### Email Configuration (SMTP)
- `SMTP_HOST`: SMTP server host (default: `smtp.gmail.com`)
- `SMTP_PORT`: SMTP server port (default: `587`)
- `SMTP_USER`: Your email address
- `SMTP_PASSWORD`: Your email app password
- `FROM_EMAIL`: Sender email address

### Shipping Integration
- `SHIPROCKET_EMAIL`: Shiprocket account email
- `SHIPROCKET_PASSWORD`: Shiprocket account password

### WhatsApp Integration
- `WHATSAPP_API_KEY`: WhatsApp Business API key
- `WHATSAPP_PHONE_NUMBER`: WhatsApp business phone number

## 🛣️ API Routes

### Authentication (`/api/auth`)
Handles user registration, login, and authentication.

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/auth/register` | Register a new user account | ❌ |
| `POST` | `/api/auth/login` | Login and receive JWT tokens | ❌ |

**Registration Fields:**
- `email`, `password`, `first_name`, `last_name`, `phone`

**Login Response:**
- Returns `access_token`, `refresh_token`, and `token_type`

---

### Products (`/api/products`)
Manage product catalog with filtering, search, and CRUD operations.

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/products` | Get all products with filters | ❌ |
| `GET` | `/api/products/{slug}` | Get product by slug | ❌ |
| `POST` | `/api/products` | Create a new product | ✅ Admin |
| `PUT` | `/api/products/{product_id}` | Update product details | ✅ Admin |
| `DELETE` | `/api/products/{product_id}` | Delete a product | ✅ Admin |

**Query Parameters for GET `/api/products`:**
- `skip`: Pagination offset (default: `0`)
- `limit`: Number of items per page (default: `20`)
- `category_id`: Filter by category ID
- `search`: Search in product name and description
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter

---

### Cart (`/api/cart`)
Shopping cart management for authenticated users.

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/cart` | Get user's cart items | ✅ User |
| `POST` | `/api/cart/add` | Add item to cart | ✅ User |
| `PUT` | `/api/cart/{cart_item_id}` | Update cart item quantity | ✅ User |
| `DELETE` | `/api/cart/{cart_item_id}` | Remove item from cart | ✅ User |
| `DELETE` | `/api/cart` | Clear all cart items | ✅ User |

**Features:**
- Automatic quantity update if item already exists
- Stock validation before adding to cart
- Prevents adding out-of-stock items

---

### Orders (`/api/orders`)
Order processing, tracking, and management.

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/orders` | Create a new order | ✅ User |
| `GET` | `/api/orders` | Get all user orders | ✅ User |
| `GET` | `/api/orders/{order_id}` | Get order details | ✅ User |
| `POST` | `/api/orders/{order_id}/cancel` | Cancel an order | ✅ User |
| `PUT` | `/api/orders/{order_id}/status` | Update order status | ✅ Admin |

**Order Creation Features:**
- Automatic order number generation (format: `JORA{YYYYMMDD}{6-digit-random}`)
- Coupon code validation and discount application
- Tax calculation (18% GST)
- Free shipping for orders above ₹1000
- Stock validation and automatic stock deduction
- Supports both percentage and fixed-amount coupons

**Order Statuses:**
- `PENDING`, `CONFIRMED`, `PROCESSING`, `SHIPPED`, `DELIVERED`, `CANCELLED`, `RETURNED`

---

### Categories (`/api/categories`)
Product category management.

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/categories` | Get all categories | ❌ |
| `POST` | `/api/categories` | Create a new category | ✅ Admin |

**Features:**
- Categories ordered by `display_order`
- Hierarchical category support

---

### B2B (`/api/b2b`)
Business-to-Business customer registration and management.

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/b2b/register` | Register as B2B customer | ✅ User |
| `GET` | `/api/b2b/profile` | Get B2B profile | ✅ User |
| `PUT` | `/api/b2b/{b2b_id}/approve` | Approve B2B customer | ✅ Admin |

**B2B Registration Fields:**
- `business_name`: Company/business name
- `gst_number`: GST registration number

**Approval Process:**
- Admin approves B2B registration
- Sets discount tier (percentage)
- User role upgraded to `B2B`

---

### Health Check
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/` | API root endpoint | ❌ |
| `GET` | `/health` | Health check endpoint | ❌ |

## 🔐 Authentication

The API uses **JWT (JSON Web Tokens)** for authentication.

### How to Authenticate

1. **Register or Login** to receive tokens
2. **Include the access token** in the `Authorization` header:
   ```
   Authorization: Bearer <your_access_token>
   ```

### Token Types
- **Access Token**: Short-lived (30 minutes), used for API requests
- **Refresh Token**: Long-lived (7 days), used to obtain new access tokens

### User Roles
- **USER**: Regular customer (default)
- **B2B**: Business customer with special pricing
- **ADMIN**: Full access to admin endpoints

## 🗄️ Database Models

### Core Models
- **User**: Customer accounts with authentication
- **Product**: Product catalog with variants
- **ProductVariant**: Size, color, and stock variations
- **Category**: Product categorization
- **Cart**: Shopping cart items
- **Order**: Order records with items
- **OrderItem**: Individual items in an order
- **Address**: Shipping and billing addresses
- **Coupon**: Discount coupons
- **B2BCustomer**: Business customer profiles

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── models/          # Database models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   ├── category.py
│   │   └── b2b.py
│   ├── routes/          # API route handlers
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   ├── orders.py
│   │   ├── categories.py
│   │   └── b2b.py
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # Authentication utilities
│   └── dependencies.py  # Dependency injection
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── Dockerfile           # Docker configuration
```

## 🐳 Docker Support

The project includes a Dockerfile for containerization.

```bash
# Build the Docker image
docker build -t jora-backend .

# Run the container
docker run -p 8000:8000 --env-file .env jora-backend
```

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.115.0
- **Database**: MySQL 8.0+ with SQLAlchemy 2.0
- **Authentication**: JWT with python-jose
- **Password Hashing**: Bcrypt via passlib
- **Validation**: Pydantic 2.10
- **ASGI Server**: Uvicorn
- **Payment Gateways**: Razorpay, Stripe
- **Database Migrations**: Alembic

## 📝 Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🔒 Security Notes

- Always change the `SECRET_KEY` in production
- Use strong passwords for database and admin accounts
- Enable HTTPS in production
- Keep dependencies updated
- Use environment variables for sensitive data
- Never commit `.env` file to version control

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`

These interactive documentation pages allow you to:
- Explore all available endpoints
- Test API requests directly from the browser
- View request/response schemas
- Understand authentication requirements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is proprietary software for JORA E-commerce.

## 📧 Support

For issues or questions, please contact the development team or create an issue in the repository.

---

**Built with ❤️ for JORA - Luxury Clothing Brand**
