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
    return jsonify({"categories":categories_data}), 200

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

@app.route('/category/<int:id>/product', methods=['POST'])
@jwt_required()
def create_product(id):
    this_user = get_jwt_identity()
    if this_user["role"] == "user":
        return {"error": "Unauthorized"}, 401
    
    data = request.json
    name = data["name"]
    unit = data["unit"]
    rateperunit = data["rateperunit"]
    quantity = data["quantity"]

    if not name or not unit or not rateperunit or not quantity:
        return {"error": "Required Fields Missing"}, 400
    if quantity <= 0:
        return {"error": "Quantity must be greater than 0"}, 400
    if rateperunit <= 0:
        return {"error": "Rate per unit must be greater than 0"}, 400
    category = Category.query.filter_by(id=id).first()
    if not category:
        return {"error": "Category not found"}, 404
    new_product = Product(name=name,
                          unit=unit,
                          rateperunit=rateperunit,
                          quantity=quantity,
                          category_id=id,
                          creator_email=this_user["email"])
    try:
        db.session.add(new_product)
        db.session.commit()
        return {"message": "Product created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to create product"}, 500

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_data = products_schema.dump(products)
    return jsonify(products_data), 200

@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.filter_by(id=id).first()
    if not product:
        return {"error": "Product not found"}, 404
    product_data = product_schema.dump(product)
    return jsonify(product_data), 200


@app.route('/product/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    this_user = get_jwt_identity()
    if this_user["role"] == "user":
        return {"error": "Unauthorized"}, 401
    data = request.json
    name = data["name"]
    unit = data["unit"]
    rateperunit = data["rateperunit"]
    quantity = data["quantity"]
    if not name or not unit or not rateperunit or not quantity:
        return {"error": "Required Fields Missing"}, 400
    if quantity <= 0:
        return {"error": "Quantity must be greater than 0"}, 400
    if rateperunit <= 0:
        return {"error": "Rate per unit must be greater than 0"}, 400
    product = Product.query.filter_by(id=id).first()
    if not product:
        return {"error": "Product not found"}, 404
    product.name = name
    product.unit = unit
    product.rateperunit = rateperunit
    product.quantity = quantity
    try:
        db.session.commit()
        return {"message": "Product updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to update product"}, 500
    
@app.route('/product/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    this_user = get_jwt_identity()
    if this_user["role"] == "user":
        return {"error": "Unauthorized"}, 401
    product = Product.query.filter_by(id=id).first()
    if not product:
        return {"error": "Product not found"}, 404
    try:
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to delete product"}, 500

@app.route("/add-to-cart", methods=["POST"])
@jwt_required()
def add_to_cart():
    this_user = get_jwt_identity()
    # if this_user["role"] != "user":
    #     return {"error": "Unauthorized"}, 401

    data = request.json
    product_id = data["product_id"]
    quantity = request.json.get("quantity", 1)

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return {"error": "Product not found"}, 404

    if quantity <= 0:
        return {"error": "Quantity must be greater than 0"}, 400
    if product.quantity < quantity:
        return {"error": "Insufficient quantity"}, 400

    user_cart = ShoppingCart.query.filter_by(user_email=this_user["email"]).first()

    if not user_cart:
        user_cart = ShoppingCart(user_email=this_user["email"])
        try:
            db.session.add(user_cart)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": "Failed to create cart"}, 500
    
    cart_item = CartItems.query.filter_by(shoppingcart_id=user_cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItems(shoppingcart_id=user_cart.id, product_id=product_id, quantity=quantity)
    try:
        db.session.add(cart_item)
        db.session.commit()
        return {"message": "Item added to cart successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to add item to cart"}, 500


@app.route('/view-cart', methods=['GET'])
@jwt_required()
def view_cart():
    this_user = get_jwt_identity()
    user_cart = ShoppingCart.query.filter_by(user_email=this_user["email"]).first()
    if not user_cart:
        return {"msg": "Cart is empty"}, 200
    cart_items = CartItems.query.filter_by(shoppingcart_id=user_cart.id).all()
    cart_items_data = []
    for item in cart_items:
        cart_items_data.append({
            'cart_id': item.id,
            'product_id': item.product_id,
            'quantity': item.quantity,
            'product_name':item.product.name,
            'rateperunit':item.product.rateperunit,
            'unit':item.product.unit,
            'total': item.product.rateperunit * item.quantity
        })
    return jsonify({"cart":cart_items_data}), 200

@app.route('/place-order', methods=['POST'])
@jwt_required()
def place_order():
    this_user = get_jwt_identity()
    user_cart = ShoppingCart.query.filter_by(user_email=this_user["email"]).first()
    if not user_cart or not user_cart.items:
        return {"message":"Cart is Empty"}, 200
    total_amount = 0
    order_items = []
    for item in user_cart.items:
        if item.quantity > item.product.quantity:
            return {"error":"Out of Stock"}, 400
        total_amount += item.product.rateperunit * item.quantity
        order_item = OrderItems(
            product_id = item.product_id,
            quantity = item.quantity
        )
        order_items.append(order_item)
        product = Product.query.filter_by(id = item.product_id).first()
        product.quantity -= item.quantity
    new_order = Order(
        user_email = this_user["email"],
        total_amount = total_amount,
        order_date = datetime.now()
    )
    new_order.items = order_items
    print(product.quantity)
    try:
        db.session.add(new_order)
        db.session.delete(user_cart)
        db.session.commit()
        return {"message":"Order Placed Successfully"} , 200
    except Exception as e:
        db.session.rollback()
        return {"error":"Failed to place order"}, 500



if __name__ == "__main__":
    app.run(debug=True)