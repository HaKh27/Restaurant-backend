from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance (used to interact with the database)
db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)

    #Relationship: one catergory has many inventory items
    items = db.relationship("InventoryItem", backref="category", lazy=True)

class InventoryItem(db.Model):
    __tablename__ = "inventory_items"
    """
    Represents a single inventory item in the database.
    Each instance of this class maps to a row in the inventory table.
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    name = db.Column(db.String(100), nullable=False)  # Item name
    quantity = db.Column(db.Integer, nullable=False)  # Item quantity

    category_id = db.Column (
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable= True
    )


