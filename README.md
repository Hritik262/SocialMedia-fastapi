# FastAPI Social Media API

A RESTful API built with FastAPI for a social media platform with JWT Bearer token authentication, user management, and post CRUD operations.

## Features

- 🔐 **JWT Bearer Authentication** - Secure token-based authentication
- 👤 **User Management** - User registration and profile retrieval
- 📝 **Post Management** - Create, read, update, and delete posts
- 🔒 **Authorization** - Owner-based access control for posts
- 🗄️ **PostgreSQL Database** - Robust data persistence with SQLAlchemy ORM
- 🔄 **Database Migrations** - Alembic for version-controlled schema changes

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Relational database
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations
- **Jose** - JWT token encoding/decoding
- **Passlib** - Password hashing with bcrypt

## Installation

### Prerequisites

- Python 3.7+
- PostgreSQL

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hritik262/SocialMedia-fastapi.git
   cd SocialMedia-fastapi
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic python-jose[cryptography] passlib[bcrypt] python-multipart email-validator
   ```

4. **Configure Database**
   
   Update the database URL in `app/database.py`:
   ```python
   SQL_ALCHEMY_DATABASE_URL = 'postgresql://username:password@localhost:5432/your_database'
   ```

5. **Run Database Migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Authentication

#### Register User
```http
POST /users/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

#### Login
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=yourpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Posts

All post endpoints require authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

#### Get All Posts
```http
GET /posts/
Authorization: Bearer <token>
```

#### Create Post
```http
POST /posts/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My First Post",
  "content": "This is the content of my post",
  "published": true
}
```

#### Get Single Post
```http
GET /posts/{id}
Authorization: Bearer <token>
```

#### Update Post
```http
PUT /posts/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content",
  "published": true
}
```

**Note:** Only the post owner can update their posts.

#### Delete Post
```http
DELETE /posts/{id}
Authorization: Bearer <token>
```

**Note:** Only the post owner can delete their posts.

### Users

#### Get User by ID
```http
GET /users/{id}
```

## Project Structure

```
Fastapi/
├── alembic/                 # Database migrations
│   └── versions/           # Migration scripts
├── app/
│   ├── routers/
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── post.py         # Post CRUD endpoints
│   │   └── user.py         # User endpoints
│   ├── __init__.py
│   ├── database.py         # Database connection
│   ├── main.py             # FastAPI app entry point
│   ├── models.py           # SQLAlchemy models
│   ├── oauth2.py           # JWT authentication logic
│   ├── schemas.py          # Pydantic schemas
│   └── utils.py            # Utility functions (password hashing)
├── .gitignore
├── alembic.ini             # Alembic configuration
└── README.md
```

## Security Features

- **Password Hashing**: Passwords are hashed using bcrypt before storage
- **JWT Tokens**: Stateless authentication with 30-minute token expiry
- **Owner Authorization**: Users can only modify/delete their own posts
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection attacks

## Environment Variables

For production, consider using environment variables for sensitive data:

```python
# Example .env file (not included in repo)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Development

### Running Tests
```bash
# Add your test commands here
pytest
```

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

Hritik - [@Hritik262](https://github.com/Hritik262)

Project Link: [https://github.com/Hritik262/SocialMedia-fastapi](https://github.com/Hritik262/SocialMedia-fastapi)
