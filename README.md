
```markdown
# Task & User Management App Alx Final Project

## Overview

This project includes backend functionality for **User management** and lays the foundation for a **Tasks app**. The User app is fully implemented and tested. The frontend is under development and will be pushed soon.

### Status (as of 27/Aug/2025)
- **User app backend:** ✅ Completed and tested
- **Tasks app backend:** ⚠️ In progress
- **Frontend:** In progress (not yet pushed to Git)

---

## User App Features

### 1. Custom User Model
- `CustomUser` extends `AbstractUser`
- Added `name` field
- Unique email enforced
- Admin interface customized to include `name`

### 2. Serializers
- `UserCreateSerializer` for registration with password hashing
- `UserSerializer` for listing users
- Token created automatically upon registration

### 3. Views
- `UserCreateView`: Allows user registration (`POST /api/users/register/`)
- `UserListView`: Returns list of users (`GET /api/users/`) – **authentication required**
- `CustomAuthToken`: Returns token **and** user data on login (`POST /api/users/login/`)

### 4. URLs
```

/api/users/           -> List users (auth required)
/api/users/register/  -> Register new user
/api/users/login/     -> Login and get token + user data

````

### 5. Admin
- `CustomUserAdmin` registered
- Fields displayed: `id`, `username`, `email`, `name`, `is_staff`, `is_active`
- Forms customized for `add` and `change` with `name` included

### 6. Tests
- `tests.py` covers:
  - User registration (normal & edge cases)
  - Login
  - Missing fields
  - Duplicate username
  - Password length validation
- Tests run successfully:
```bash
python manage.py test users
````

---

## Notes

* **Frontend:** React + Vite + Tailwind frontend is in progress with `AuthContext`, `Login`, `Register`, and `UserList` components. It is **not pushed yet**, but will be pushed tomorrow if possible.
* **Next steps:** Complete backend for the **Tasks app**, then integrate the frontend.

---

## How to Run Backend

1. Clone the repository:

```bash
git clone https://github.com/NatiDevHQ/alx-final_project.git<repo-url>
cd alx-final_project

```

2. Set up virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Run the development server:

```bash
python manage.py runserver
```

5. Run tests (optional):

```bash
python manage.py test users
```

---

## API Usage

### Register

```http
POST /api/users/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "StrongPass123"
}
```

### Login

```http
POST /api/users/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "StrongPass123"
}
```

**Response:**

```json
{
  "token": "<auth_token>",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "name": "Test User"
  }
}
```

### List Users (requires token)

```http
GET /api/users/
Authorization: Token <auth_token>
```

---

