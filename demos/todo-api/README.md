# 📝 Todo API — Python + Flask + OOP + PostgreSQL

A simple educational **Todo REST API**, designed to teach:

* Python fundamentals
* Object-Oriented Programming (OOP)
* Clean backend architecture
* PostgreSQL integration using `psycopg2`
* Classic “Repository → Service → API” structure
* REST endpoint design

The API automatically creates database tables on startup using the `init_db()` function in `repo.py`.
**No manual SQL commands are needed.**

---

# 📁 Project Structure

```
todo-api/
│── app.py              # Flask routes + app startup (calls init_db)
│── domain.py           # Todo domain model (OOP)
│── service.py          # Business logic (TodoService)
│── repo.py             # Repository layer (PostgreSQL adapter + init_db)
│── schema.sql          # Schema executed automatically at startup
│── requirements.txt
│── README.md
```

---

# 🚀 Quick Start

## 1️⃣ Create & activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
.\.venv\Scripts\activate        # Windows
```

---

## 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ PostgreSQL Setup (Simple Version)

Your repository uses **default values** for database config:

```python
DB_NAME = os.getenv("PGDB", "todo_db")
DB_USER = os.getenv("PGUSER", "postgres")
DB_PASS = os.getenv("PGPASS", "final2kk") # change to your password
DB_HOST = os.getenv("PGHOST", "127.0.0.1")
DB_PORT = int(os.getenv("PGPORT", "5432"))
```

So you only need to create the database itself.

### 👉 Create empty DB

```bash
psql -U postgres
```

Inside psql:

```sql
CREATE DATABASE todo_db;
\q
```

### The API will create tables automatically.

---

# ▶️ Start the API

```bash
python app.py
```

You should see:

```
init_db(): schema loaded
Running on http://127.0.0.1:8000
```

- You can now test your endpoints using postman, details below. 
---

# ✨ API Endpoints

### ➕ Create Todo

`POST /todos`

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

---

### 📄 List Todos

`GET /todos`

---

### 🔍 Get Single Todo

`GET /todos/<id>`

---

### ✏️ Update Todo

`PUT /todos/<id>`

```json
{
  "title": "Buy groceries and cleaner",
  "description": "Milk, eggs, bread, detergent",
  "is_done": false
}
```

---

### ✔️ Mark as Done

`PATCH /todos/<id>/done`

---

### 🗑 Delete Todo

`DELETE /todos/<id>`

---

# 🧠 Architecture Overview (OOP-Friendly)

This project demonstrates a clean OOP + layered backend design.

---

## 1. **Domain Layer** — Entity/Object

Represents application data:

```python
class Todo:
    def __init__(self, id, title, description, is_done=False):
        self.id = id
        self.title = title
        self.description = description
        self.is_done = is_done
```

You work with Todo objects, not raw dictionaries or SQL rows.

---

## 2. **Repository Layer** — Low-level DB adapter

* Handles SQL
* Opens DB connections (`psycopg2.connect`)
* Translates DB rows → Todo objects
* Loads `schema.sql` on application start

```python
def init_db():
    with open("schema.sql") as f:
        cur.execute(f.read())
```

This hides SQL from the rest of the app (**abstraction**).

---

## 3. **Service Layer** — Business rules

Implements behavior:

```python
class TodoService:
    def create_todo(...):
        ...
    def update_todo(...):
        ...
```

Keeps API clean by separating logic from HTTP.

---

## 4. **API Layer** — Flask routes

Receives JSON → calls service → returns JSON.

```
POST /todos → TodoService.create → TodoRepo.create
```

This is **Separation of concerns**.

---

# 🧪 Postman Test JSON

### Create

```json
{
  "title": "Do laundry",
  "description": "Wash + dry"
}
```

### Update

```json
{
  "title": "Finish laundry",
  "description": "Wash, dry, fold",
  "is_done": true
}
```

---

# 🎓 Teaching Notes

This project teaches:

* OOP modeling
* Layered architecture
* Encapsulation (Repository hides SQL)
* Abstraction (Service hides rules from API)
* PostgreSQL connections
* SQL CRUD
* REST principles
* JSON request/response
* API testing using Postman

Can easily extend this into:

* authentication
* pagination
* FastAPI
* SQLAlchemy ORM
* full ETL pipelines
* integration with Pandas
