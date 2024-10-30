
# Email-VAULT_BACKEND Backend

This project is a backend API built with FastAPI. It includes user authentication (registration, login, email verification, password reset) and supports a relational database using SQLAlchemy.

## Features

- User registration with email verification
- User login with password hashing
- Password reset functionality
- Failed login attempt logging
- JWT-based authentication (optional, if you plan to implement token-based sessions)
- CORS support for frontend-backend communication

## Prerequisites

- **Python 3.8+**
- **Docker** (optional, if using Docker to run the application)
- **Mailjet API credentials** (for email sending functionality)

## Getting Started

### 1. Clone the repository

```bash
git clone git@github.com:NabeekhAbid/email-vault-backend.git
cd email-vault-backend
```

### 2. Set up a virtual environment

```bash
python3 -m venv env
source env/bin/activate  # For Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

<Create a `.env` file in the root directory with the following variables:

```plaintext
DATABASE_URL="sqlite:///./test.db"    # Or the URL for your PostgreSQL/MySQL database
MAILJET_API_KEY="your-mailjet-api-key"
MAILJET_API_SECRET="your-mailjet-api-secret"
FRONT_END_BASE_UR>L="http://localhost:3000"  # Your frontend URL for email verification links
```

### 5. Run database migrations

Rococo for migrations, apply migrations as follows:

```bash
 rococo-mysql --migrations-dir common/migrations --env-files=.env rf
```

### 6. Start the application

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## Docker Setup

To run the application in Docker:

1. **Build the Docker image:**

    ```bash
    docker build -t fastapi-backend .
    ```

2. **Run the Docker container:**

    ```bash
    docker run -d -p 8000:8000 --env-file .env fastapi-backend
    ```

## API Endpoints

### Authentication & User Management

#### Register a New User

**Endpoint:** `/register`  
**Method:** `POST`  
**Body:** 

```json
{
    "firstName": "John",
    "lastName": "Doe",
    "companyName": "Example Inc.",
    "email": "user@example.com",
    "password": "password123"
}
```

#### Verify Email

**Endpoint:** `/verify-email`  
**Method:** `POST`  
**Body:** 

```json
{
    "token": "unique-verification-token"
}
```

#### User Login

**Endpoint:** `/login`  
**Method:** `POST`  
**Body:** 

```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

#### Reset Password

**Endpoint:** `/reset-password`  
**Method:** `POST`  
**Body:** 

```json
{
    "email": "user@example.com"
}
```

## Project Structure

```plaintext
app/
├── models/             # SQLAlchemy models for User, EmailVerification, PasswordReset, etc.
├── routes/             # FastAPI route handlers for user-related endpoints
├── services/           # Service layer for business logic, such as UserService
├── utils/              # Utility functions, like password hashing and email validation
├── database.py         # Database setup and session handling
├── main.py             # FastAPI application setup and middleware
```

## Testing

1. **Run Tests:**

    To run tests, use:

    ```bash
    pytest
    ```

2. **Configure Test Database:**

    Ensure your test database is set up separately in your `.env` file.

## Environment Variables

Here are the environment variables required for the app:

| Variable             | Description                                     |
| -------------------- | ----------------------------------------------- |
| `DATABASE_URL`       | Database connection URL                         |
| `MAILJET_API_KEY`    | API key for Mailjet                             |
| `MAILJET_API_SECRET` | API secret for Mailjet                          |
| `FRONT_END_BASE_URL` | Frontend URL for email verification links       |

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Open a pull request.

## License

This project is licensed under the MIT License.

---