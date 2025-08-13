from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

order_food = db.Table('order_food',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True)
)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100))
    house = db.Column(db.String(20))
    city = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    orders = db.relationship('Order', back_populates='customer')

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    finalized_orders = db.relationship('Order', back_populates='employee')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dateTime = db.Column(db.DateTime)
    total = db.Column(db.Float)
    status = db.Column(db.String(20))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    foods = db.relationship('Food', secondary=order_food, back_populates='orders')
    customer = db.relationship('Customer', back_populates='orders')
    employee = db.relationship('Employee', back_populates='finalized_orders')

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    amount = db.Column(db.Integer)  # Inventory amount available
    price = db.Column(db.Float)
    description = db.Column(db.String(100))
    orders = db.relationship('Order', secondary=order_food, back_populates='foods')
