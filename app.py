from flask import Flask
from models import db
from routes import inventory_bp
from models import Category, InventoryItem
from flask import send_from_directory

# Create Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurant.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database with app
db.init_app(app)

# Register API routes
app.register_blueprint(inventory_bp)

if __name__ == "__main__":
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Run the server
    app.run(debug=True, port=5001)
