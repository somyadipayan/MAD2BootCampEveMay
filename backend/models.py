from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship

db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = "user"

    email = Column(Text, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    city = Column(Text)
    role = Column(Text, nullable=False) # "admin" or "user" or "manager"
    last_loggedin = Column(DateTime, nullable=False)

    def __init__(self, email, name, password, city, role, last_loggedin):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.city = city
        self.role = role
        self.last_loggedin = last_loggedin

class UserSchema(ma.Schema):
    class Meta:
        fields = ("email", "name", "password", "city", "role", "last_loggedin")

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Category(db.Model):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    creator_email = Column(Text, ForeignKey("user.email"),nullable=False)
    creator = relationship("User", backref="categories")
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    verified = Column(Boolean, default=False)

    def __init__(self, name, creator_email, verified=False):
        self.name = name
        self.creator_email = creator_email
        self.verified = verified

class Product(db.Model):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    unit = Column(Text, nullable=False)
    rateperunit = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    category = relationship("Category", back_populates="products")
    creator_email = Column(Text, ForeignKey("user.email"),nullable=False)
    creator = relationship("User", backref="products")
    quantity = Column(Integer, nullable=False)
    shoppingcarts = relationship("CartItems", back_populates="product", cascade="all, delete-orphan")
    order = relationship("OrderItems", back_populates="product", cascade="all, delete-orphan")
    def __init__(self, name, unit, rateperunit, category_id, creator_email, quantity):
        self.name = name
        self.unit = unit
        self.rateperunit = rateperunit
        self.category_id = category_id
        self.creator_email = creator_email
        self.quantity = quantity

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "creator_email", "verified")

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "unit", "rateperunit", "category_id", "creator_email", "quantity")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class ShoppingCart(db.Model):
    __tablename__ = "shopping_cart"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(Text, ForeignKey("user.email"),nullable=False)
    user = relationship("User", backref="shoppingcart")
    items = relationship("CartItems", back_populates="shoppingcart", cascade="all, delete-orphan")


class CartItems(db.Model):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    shoppingcart_id = Column(Integer, ForeignKey("shopping_cart.id"), nullable=False)
    shoppingcart = relationship("ShoppingCart", back_populates="items")
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product", back_populates="shoppingcarts")
    quantity = Column(Integer, nullable=False)

class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(Text, ForeignKey("user.email"),nullable=False)
    user = relationship("User", backref="order")
    total_amount = Column(Integer, nullable=False)
    order_date = Column(DateTime, nullable=False)
    items = relationship("OrderItems", back_populates="order", cascade = "all, delete-orphan")

class OrderItems(db.Model):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    order = relationship("Order", back_populates="items")
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product", back_populates="order")
    quantity = Column(Integer, nullable=False)

class Image(db.Model):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(Text, nullable=False)