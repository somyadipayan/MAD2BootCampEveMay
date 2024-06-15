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

with app.app_context():
    db.create_all()

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

if __name__ == "__main__":
    app.run(debug=True)