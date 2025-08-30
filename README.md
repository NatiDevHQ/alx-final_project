# Task & User Management App – ALX Final Project

## Overview
This project is a **Django REST Framework (DRF)** based application for **User Management** and **Task Management**.  
It includes a **custom user model**, authentication system, and a **tasks API** that allows authenticated users to create, update, and manage tasks.  
Frontend development will connect to these APIs and is under active development.

---

## 📌 Project Status (as of 29/Aug/2025)
- **User App Backend:** ✅ Fully completed and tested  
- **Tasks App Backend:** ✅ Completed with CRUD functionality & tested  
- **Frontend:** ⚠️ Under development (to be pushed soon)  

---

## 🧑‍💻 User App Features

### 1. Custom User Model
- Extends `AbstractUser`
- Added `name` field
- Unique **email-based authentication**
- Admin interface customized to show `name`

### 2. Serializers
- `UserCreateSerializer` → Handles registration with password hashing  
- `UserSerializer` → For listing and returning user data  
- Token created automatically upon registration  

### 3. Views
- **Register:** `POST /api/users/register/` → Creates a new user  
- **Login:** `POST /api/users/login/` → Returns **token + user data**  
- **User List:** `GET /api/users/` → Returns all users (**authentication required**)  

### 4. URLs
```http
POST   /api/users/register/   → Register new user
POST   /api/users/login/      → Login and get token + user data
GET    /api/users/            → List all users (requires authentication)
✅ Tasks App Features
1. Task Model
title (string)

description (text)

completed (boolean)

owner (ForeignKey to User – ensures ownership)

2. Serializers
TaskSerializer → Full CRUD serialization with ownership

3. Views
Implemented via ViewSets

Permissions: Only the owner of a task can modify/delete it

4. URLs
http
Copy code
GET    /api/tasks/          → List all tasks (authenticated user only)
POST   /api/tasks/          → Create new task
GET    /api/tasks/{id}/     → Retrieve single task
PUT    /api/tasks/{id}/     → Update task
PATCH  /api/tasks/{id}/     → Partial update
DELETE /api/tasks/{id}/     → Delete task
🔑 Authentication
Uses DRF Token Authentication

Token is returned during login and must be included in headers:

http
Copy code
Authorization: Token your_token_here
🧪 Testing
Automated tests written with APITestCase

Coverage:

✅ User registration, login, and listing

✅ Password validation

✅ Task creation, listing, updating, and deletion

✅ Ownership restrictions enforced

Run tests:

bash
Copy code
python manage.py test
🚀 Frontend (Coming Soon)
The frontend will be built with React + TailwindCSS, connecting to the APIs above.
Features planned:

User authentication (register/login/logout)

Task dashboard with CRUD actions

Friendly & responsive UI

📂 Tech Stack
Backend: Django, Django REST Framework

Database: SQLite (development), PostgreSQL (production ready)

Auth: DRF Token Authentication

Frontend: React + TailwindCSS (in progress)
