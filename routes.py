from flask import Blueprint, jsonify, request
from models import db, InventoryItem

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
        {"id": item.id, "name": item.name, "quantity": item.quantity}
        for item in items
    ])


@inventory_bp.route("/api/inventory", methods=["POST"])
def add_inventory():
    """
    Adds a new item to the inventory.
    """
    data = request.get_json()

    # Prevent negative quantities
    if data["quantity"] < 0:
        return jsonify({"error": "Quantity cannot be negative"}), 400

    item = InventoryItem(
        name=data["name"],
        quantity=data["quantity"]
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Item added"}), 201


@inventory_bp.route("/api/inventory/<int:item_id>", methods=["PUT"])
def update_inventory(item_id):
    """
    Updates the name and/or quantity of an existing inventory item.
    """
    data = request.get_json()
    item = InventoryItem.query.get(item_id)

    # Check if item exists
    if not item:
        return jsonify({"error": "Item not found"}), 404

    updates = []

    # Update quantity if provided and different
    if "quantity" in data:
        if data["quantity"] < 0:
            return jsonify({"error": "Quantity cannot be negative"}), 400
        if data["quantity"] != item.quantity:
            item.quantity = data["quantity"]
            updates.append("quantity")

    # Update name if provided and different
    if "name" in data:
        if data["name"] != item.name:
            item.name = data["name"]
            updates.append("name")

    # If nothing actually changed
    if not updates:
        return jsonify({"message": "No changes made"}), 200

    db.session.commit()

    message = " and ".join(updates).capitalize() + " updated"
    return jsonify({"message": message})


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
