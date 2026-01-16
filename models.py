from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance (used to interact with the database)
db = SQLAlchemy()

class InventoryItem(db.Model):
    """
    Represents a single inventory item in the database.
    Each instance of this class maps to a row in the inventory table.
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    name = db.Column(db.String(100), nullable=False)  # Item name
    quantity = db.Column(db.Integer, nullable=False)  # Item quantity
