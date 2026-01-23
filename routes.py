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
    data = request.get_json()
    item = InventoryItem.query.get(item_id)

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

    # Update category (THIS IS THE IMPORTANT PART)
    if "category_id" in data:
        incoming_category_id = data["category_id"]

        # Remove category
        if incoming_category_id is None:
            if item.category_id is not None:
                item.category_id = None
                updates.append("category")

        # Assign / change category
        else:
            category = Category.query.get(incoming_category_id)
            if not category:
                return jsonify({"error": "Category not found"}), 404

            if item.category_id != incoming_category_id:
                item.category_id = incoming_category_id
                updates.append("category")

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
            "name": category.name,
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "quantity": item.quantity
                }
                for item in category.items
            ]
        }
        for category in categories
    ])

@inventory_bp.route("/api/categories/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Category name is required"}), 400

    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    new_name = data["name"]

    # Prevent duplicate category names
    existing = Category.query.filter_by(name=new_name).first()
    if existing and existing.id != category_id:
        return jsonify({"error": "Category name already exists"}), 400

    if category.name == new_name:
        return jsonify({"message": "No changes made"}), 200

    category.name = new_name
    db.session.commit()

    return jsonify({"message": "Category updated"}), 200


@inventory_bp.route("/api/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        return jsonify({"error": "Category not found"}), 404

    # 🚨 Block deletion if category has items
    if category.items:
        return jsonify({
            "error": "Cannot delete category with existing inventory items"
        }), 400

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted"}), 200

