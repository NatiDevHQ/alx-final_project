
````markdown
# ✨ Task & User Management App – ALX Final Project

## 📖 Overview
This project is a **Django REST Framework (DRF)** powered application that provides:  
- 🔐 **User Management** with a custom user model & token authentication  
- ✅ **Task Management** with full CRUD operations, tied to authenticated users  

A **React + TailwindCSS frontend** will connect to these APIs (currently under development).  

---

## 📌 Project Status (as of 29/Aug/2025)
- 🟢 **User App Backend:** Fully completed & tested  
- 🟢 **Tasks App Backend:** Completed with CRUD functionality & tested  
- 🟡 **Frontend:** Under development (will be pushed soon)  

---

## 👤 User App Features

### 🔹 Custom User Model
- Extends `AbstractUser`
- Unique **email-based authentication**
- Added `name` field
- Admin panel customized to display user details  

### 🔹 API Endpoints
| Method | Endpoint                  | Description                      | Auth Required |
|--------|---------------------------|----------------------------------|---------------|
| POST   | `/api/users/register/`    | Register a new user              | ❌ |
| POST   | `/api/users/login/`       | Login & get **token + user data**| ❌ |
| GET    | `/api/users/`             | List all users                   | ✅ |

---

## 📋 Tasks App Features

### 🔹 Task Model
- `title` (string)  
- `description` (text)  
- `completed` (boolean)  
- `owner` (ForeignKey → User)  

### 🔹 API Endpoints
| Method | Endpoint             | Description                     | Auth Required |
|--------|----------------------|---------------------------------|---------------|
| GET    | `/api/tasks/`        | List all tasks (user-specific)  | ✅ |
| POST   | `/api/tasks/`        | Create a new task               | ✅ |
| GET    | `/api/tasks/{id}/`   | Retrieve a single task          | ✅ |
| PUT    | `/api/tasks/{id}/`   | Update a task (replace)         | ✅ |
| PATCH  | `/api/tasks/{id}/`   | Update a task (partial)         | ✅ |
| DELETE | `/api/tasks/{id}/`   | Delete a task                   | ✅ |

🔒 **Ownership rules enforced** → Only task owners can update/delete their tasks.  

---

## 🔑 Authentication
Uses **DRF Token Authentication**.  
After login, include the token in headers for all requests:  

```http
Authorization: Token your_token_here
````

---

## 🧪 Testing

Automated tests are written using `APITestCase`.

### ✅ Coverage

* User registration, login & listing
* Password validation
* Task CRUD operations
* Ownership restrictions

### ▶ Run Tests

```bash
python manage.py test
```

---

## 🚀 Frontend (Coming Soon)

The frontend will be built with **React + TailwindCSS** and will include:

* 🔐 User authentication (register/login/logout)
* 📝 Task dashboard with CRUD functionality
* 📱 Modern & responsive UI

---

## 🛠️ Tech Stack

* **Backend:** Django, Django REST Framework
* **Database:** SQLite (development), PostgreSQL (production ready)
* **Auth:** DRF Token Authentication
* **Frontend:** React + TailwindCSS (in progress)

```

