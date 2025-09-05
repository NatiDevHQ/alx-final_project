

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
- 🟡 **Frontend:** Under development (to be pushed soon)  

---

## 🛠️ Tech Stack
- **Backend:** Django, Django REST Framework  
- **Database:** SQLite (development), PostgreSQL (production-ready)  
- **Auth:** DRF Token Authentication  
- **Frontend:** React + TailwindCSS (in progress)  

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/NatiDevHQ/alx-final_project.git
   cd alx-final_project
````

2. **Create & activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

   Or, if you’re using Pipenv:

   ```bash
   pipenv install
   pipenv shell
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:

   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3   # or your PostgreSQL URL
   ```

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

6. **Run the server**

   ```bash
   python manage.py runserver
   ```

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 👤 User App Features

### 🔹 Custom User Model

* Extends `AbstractUser`
* Unique **email-based authentication**
* Added `name` field
* Admin panel customized to display user details

### 🔹 API Endpoints

| Method | Endpoint               | Description                       | Auth Required |
| ------ | ---------------------- | --------------------------------- | ------------- |
| POST   | `/api/users/register/` | Register a new user               | ❌             |
| POST   | `/api/users/login/`    | Login & get **token + user data** | ❌             |

---

## 📋 Tasks App Features

### 🔹 Task Model

* `title` (string)
* `description` (text)
* `completed` (boolean)
* `owner` (ForeignKey → User)

### 🔹 API Endpoints

| Method | Endpoint           | Description                    | Auth Required |
| ------ | ------------------ | ------------------------------ | ------------- |
| GET    | `/api/tasks/`      | List all tasks (user-specific) | ✅             |
| POST   | `/api/tasks/`      | Create a new task              | ✅             |
| GET    | `/api/tasks/{id}/` | Retrieve a single task         | ✅             |
| PUT    | `/api/tasks/{id}/` | Update a task (replace)        | ✅             |
| PATCH  | `/api/tasks/{id}/` | Update a task (partial)        | ✅             |
| DELETE | `/api/tasks/{id}/` | Delete a task                  | ✅             |

🔒 **Ownership rules enforced** → Only task owners can update/delete their tasks.

---

## 🔑 Authentication

Uses **DRF Token Authentication**.
After login, include the token in headers for all requests:

```http
Authorization: Token your_token_here
```

---

## 🧪 API Testing with Postman

You can copy-paste these request payloads directly into Postman to test the endpoints.

---

### 👤 User API

#### 1. Register

```http
POST /api/users/register/
Content-Type: application/json

{
  "email": "john@example.com",
  "username": "John",
  "password": "TestPass123"
}
```

#### 2. Login

```http
POST /api/users/login/
Content-Type: application/json

{
  "username": "john",
  "password": "TestPass123"
}
```

🔑 **Sample Response**

```json
{
  "token": "abcdef123456",
}
```

---

### 📋 Task API

#### 1. Create Task

```http
POST /api/tasks/
Authorization: Token your_token_here
Content-Type: application/json

{
  "title": "Finish ALX Project",
  "description": "Complete backend and frontend integration",
  "completed": false
}
```

**Sample Response**

```json
{
  "id": 1,
  "title": "Finish ALX Project",
  "description": "Complete backend and frontend integration",
  "completed": false,
  "owner": "john"
}
```

#### 2. List Tasks

```http
GET /api/tasks/
Authorization: Token your_token_here
```

#### 3. Get Task by ID

```http
GET /api/tasks/1/
Authorization: Token your_token_here
```

#### 4. Update Task (Full Replace)

```http
PUT /api/tasks/1/
Authorization: Token your_token_here
Content-Type: application/json

{
  "title": "Updated Task Title",
  "description": "Updated description here",
  "completed": true
}
```

#### 5. Update Task (Partial)

```http
PATCH /api/tasks/1/
Authorization: Token your_token_here
Content-Type: application/json

{
  "completed": true
}
```

#### 6. Delete Task

```http
DELETE /api/tasks/1/
Authorization: Token your_token_here
```

---

## 🚀 Frontend (Coming Soon)

The frontend will be built with **React + TailwindCSS** and will include:

* 🔐 User authentication (register/login/logout)
* 📝 Task dashboard with CRUD functionality
* 📱 Modern & responsive UI

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Add feature"`)
4. Push to branch (`git push origin feature-name`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🚀 Future Enhancements

* Implement **Pagination** for task lists
* Add **Search/Filter** by title or completion status
* Enhance **Error Handling** with standardized responses
* Integrate **Swagger/OpenAPI** for auto-generated docs
* Upgrade authentication with **JWT** + refresh tokens

---

```


