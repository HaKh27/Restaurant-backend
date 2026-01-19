from flask import Blueprint, jsonify, request
from models import db, InventoryItem
from models import db, Category


# Blueprint groups all inventory-related routes together
inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/api/inventory", methods=["GET"])
def get_inventory():
    """
    Returns all inventory items.
    """
    min_quantity = request.args.get("min_quantity", type=int)

    query = InventoryItem.query

    if min_quantity is not None:
        query = query.filter(InventoryItem.quantity >= min_quantity)

    items = query.all()

    return jsonify([
        {
            "id": item.id, 
            "name": item.name, 
            "quantity": item.quantity,
            "category": item.category.name if item.category else None
        }
        for item in items
    ])


@inventory_bp.route("/api/inventory", methods=["POST"])
def add_inventory():
    """
    Adds a new item to the inventory.
    """
    data = request.get_json()

    name = data.get("name")
    quantity = data.get("quantity")
    category_id = data.get("category_id")

    if not name or quantity is None:
        return jsonify({"error": "Name and quantity are required"}), 400
    
    if quantity < 0:
            return jsonify({"error": "Quantity cannot be negative"}), 400
    
    #Validate category if provided
    if category_id is not None:  # don't need to specify category, if specified: must be valid  
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
    item = InventoryItem(
        name = name,
        quantity = quantity,
        category_id = category_id
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Item added"}), 201


@inventory_bp.route("/api/inventory/<int:item_id>", methods=["PUT"])
def update_inventory(item_id):
    """
    Updates the name, quantity, and/or category of an existing inventory item.
    """
    data = request.get_json()
    item = InventoryItem.query.get(item_id)

    # Check if item exists
    if not item:
        return jsonify({"error": "Item not found"}), 404

    updates = []

    # Update quantity
    if "quantity" in data:
        if data["quantity"] < 0:
            return jsonify({"error": "Quantity cannot be negative"}), 400
        if data["quantity"] != item.quantity:
            item.quantity = data["quantity"]
            updates.append("quantity")

    # Update name
    if "name" in data:
        if data["name"] != item.name:
            item.name = data["name"]
            updates.append("name")

    # Update category
    if "category_id" in data:
        category = Category.query.get(data["category_id"])
        if not category:
            return jsonify({"error": "Category not found"}), 404

        if item.category_id != data["category_id"]:
            item.category_id = data["category_id"]
            updates.append("category")

    # If nothing changed
    if not updates:
        return jsonify({"message": "No changes made"}), 200

    db.session.commit()

    message = " and ".join(updates).capitalize() + " updated"
    return jsonify({"message": message}), 200



@inventory_bp.route("/api/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory(item_id):
    """
    Deletes an inventory item by ID.
    """
    item = InventoryItem.query.get(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Item deleted"})

@inventory_bp.route("/api/categories", methods=["POST"])
def create_category():
    """
    Create a new category.
    """
    data = request.get_json()

    # Basic validation
    if not data or "name" not in data:
        return jsonify({"error": "Category name is required"}), 400

    name = data["name"]

    # Check for duplicate category
    existing = Category.query.filter_by(name=name).first()
    if existing:
        return jsonify({"error": "Category already exists"}), 400

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Category created"}), 201

@inventory_bp.route("/api/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()

    return jsonify([
        {
            "id": category.id,
            "name": category.name
        }
        for category in categories
    ])

