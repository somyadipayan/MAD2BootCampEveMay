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

    def __init__(self, name, unit, rateperunit, category_id, creator_email):
        self.name = name
        self.unit = unit
        self.rateperunit = rateperunit
        self.category_id = category_id
        self.creator_email = creator_email

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "creator_email", "verified")

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)