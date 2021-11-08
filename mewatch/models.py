#this is the database of the project
from datetime import datetime
from enum import unique

from sqlalchemy.orm import relation
from . import db

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    watches = db.relationship('Product', backref = 'Category', cascade = "all,delete-orphan")

    def __repr__(self):
        str = "ID: {}, Name: {}, Image: {}"
        str = str.format(self.id, self.name, self.image)
        return str 

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), nullable = False),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), nullable = False),
    db.PrimaryKeyConstraint('order_id', 'product_id'))

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    material = db.Column(db.String(64), nullable=False)
    size = db.Column(db.Integer, primary_key=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(64), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    def __repr__(self):
        str = "ID: {}, Name: {}, Type: {}, Description: {}, Material: {}, Size: {}, Price: {}, Image: {}, Category: {}\n"
        str = str.format(self.id, self.name, self.type, self.description, self.material, self.size, self.price, self.image, self.category_id)
        return str



class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    address = db.Column(db.String(128))
    postcode = db.Column(db.Integer)
    email = db.Column(db.String(128))
    phone = db.Column(db.String(64))
    totalcost = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    watches = db.relationship('Product', secondary = orderdetails, backref = "Order")

    def __repr__(self):
        str = "ID: {}, Status: {}, Date: {}, Firstname: {}, Lastname: {}, Address: {}, Postcode: {}, Email: {}, Phone: {}, Date: {}, Product: {}, Total Cost: {}"
        str = str.format(self.id, self.status, self.date, self.firstname, self.lastname, self.address, self.postcode, self.email, self.phone, self.date, self.watches, self.totalcost)