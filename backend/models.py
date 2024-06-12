from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, DateTime
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = "user"

    email = Column(Text, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    city = Column(Text)
    role = Column(Text, nullable=False)
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