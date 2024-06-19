from flask import Flask, request, jsonify
from config import Config
from models import *
from datetime import datetime
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)
db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)

def CreateAdmin():
    user = User.query.filter_by(role="admin").first()
    if not user:
        new_user = User(email="admin@store.com", name="Admin", password="1", city="Bbsr", role="admin", last_loggedin=datetime.now())
        try:
            db.session.add(new_user)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
    return "Admin Created"

with app.app_context():
    db.create_all()
    CreateAdmin()

CORS(app, supports_credentials=True)

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

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    if not email or not password:
        return {"error": "All fields are required"}, 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        return {"error": "Invalid email or password"}, 401
    
    user.last_loggedin = datetime.now()
    db.session.commit()

    access_token = create_access_token(identity={
        "email": user.email,
        "role": user.role
    })

    return jsonify({"access_token": access_token, "message": "Login successful"}), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    print(current_user)
    return "You are the lucky one!, " + current_user["email"] + "!", 200

@app.route('/getuserinfo', methods=['GET'])
@jwt_required()
def getuserinfo():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user["email"]).first()
    user_data = user_schema.dump(user)
    return jsonify(user_data), 200
    
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'logout successful'})
    unset_jwt_cookies(response)
    return response

# CRUD ON CATEGORIES
# CREATE
@app.route('/category', methods=['POST'])
@jwt_required()
def create_category():
    this_user = get_jwt_identity()
    if this_user["role"] == "user":
        return {"error": "Unauthorized"}, 401
    data = request.json
    name = data["name"]
    if not name:
        return {"error": "Name is required"}, 400
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        return {"error": "Category already exists"}, 409
    verified = True if (this_user["role"] == 'admin')  else False
    new_category = Category(name=name, creator_email=this_user["email"], verified=verified)
    try:
        db.session.add(new_category)
        db.session.commit()
        if verified:
            return {"message": "Category created successfully"}, 201
        return {"message": "Category Application Submitted, Wait for Admin Approval"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to create category"}, 500

# READ ALL CATEGORIES
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_data = categories_schema.dump(categories)
    return jsonify(categories_data), 200

# READ ONE CATEGORIES
@app.route('/category/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.filter_by(id=id).first()
    if not category:
        return {"error": "Category not found"}, 404
    category_data = category_schema.dump(category)
    return jsonify(category_data), 200

# UPDATE CATEGORIES
@app.route('/category/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    this_user = get_jwt_identity()
    if this_user["role"] == "user":
        return {"error": "Unauthorized"}, 401
    data = request.json
    name = data["name"]
    if not name:
        return {"error": "Name is required"}, 400
    category = Category.query.filter_by(id=id).first()
    if not category:
        return {"error": "Category not found"}, 404
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category and existing_category.id != category.id:
        return {"error": "Category already exists"}, 409
    category.name = name
    try:
        db.session.commit()
        return {"message": "Category updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to update category"}, 500

# DELETE CATEGORIES
@app.route('/category/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    this_user = get_jwt_identity()
    if this_user["role"] != "admin":
        return {"error": "Unauthorized"}, 401
    category = Category.query.filter_by(id=id).first()
    if not category:
        return {"error": "Category not found"}, 404
    try:
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to delete category"}, 500

if __name__ == "__main__":
    app.run(debug=True)