# Restaurant Inventory Backend

A Flask-based REST API for managing restaurant inventory items.  
This project demonstrates backend fundamentals including CRUD operations, data validation, and clean project structure using Flask and SQLAlchemy.

---

## Features
- Create, read, update, and delete inventory items
- Prevent negative inventory quantities
- Support partial updates (name and/or quantity)
- Clear, meaningful API responses
- SQLite database with SQLAlchemy ORM
- Clean separation of models, routes, and app setup

---

## Tech Stack
- Python
- Flask
- SQLAlchemy
- SQLite

---

## How to Run Locally

1. Clone the repository:
```bash
git clone <https://github.com/HaKh27/Restaurant-backend>
cd restaurant-backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install flask flask-sqlalchemy
```

4. Run the application:
```bash
python app.py
```

The API will be available at:
```
http://127.0.0.1:5001
```

---

## API Endpoints

### Get all inventory items
```
GET /api/inventory
```

---

### Add a new inventory item
```
POST /api/inventory
```

Request body:
```json
{
  "name": "Tomatoes",
  "quantity": 10
}
```

---

### Update an inventory item
```
PUT /api/inventory/<id>
```

Request body:
```json
{
  "name": "Cherry Tomatoes",
  "quantity": 25
}
```

---

### Delete an inventory item
```
DELETE /api/inventory/<id>
```

---

Built as a backend learning project using Flask and SQLAlchemy.
