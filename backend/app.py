from flask import Flask, request
from config import Config
from models import *
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]
    name = data["name"]
    password = data["password"]
    city = data["city"]
    role = data["role"]
    last_loggedin = datetime.now()

    if not email or not name or not password or not role:
        return {"error": "All fields are required"}, 400
    
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {"error": "User already exists"}, 409
    
    new_user = User(email=email, name=name, password=password, city=city, role=role, last_loggedin=last_loggedin)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to create user"}, 500


if __name__ == "__main__":
    app.run(debug=True)