from flask import Flask, render_template, request, redirect, url_for
from models import db, Customer, Employee, Order, Food
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Homepage
@app.route('/')
def index():
    foods = Food.query.all()
    return render_template('index.html', foods=foods)

# Order form and submission
@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # Save customer info
        customer = Customer(
            street=request.form['street'],
            house=request.form['house'],
            city=request.form['city'],
            phone=request.form['phone']
        )
        db.session.add(customer)
        db.session.commit()

        # Get selected food items
        selected_food_ids = request.form.getlist('food_ids')
        total = 0
        foods = []

        for food_id in selected_food_ids:
            food = Food.query.get(food_id)
            if food:
                total += food.price
                foods.append(food)

        # Create order
        new_order = Order(
            dateTime=datetime.now(),
            total=total,
            status='Pending',
            customer_id=customer.id,
            employee_id=1  # Dummy employee ID
        )
        new_order.foods.extend(foods)
        db.session.add(new_order)
        db.session.commit()

        print(f"New order added with ID {new_order.id} and total {new_order.total}")

        return render_template('success.html', order=new_order)

    else:
        foods = Food.query.all()
        return render_template('order.html', foods=foods)

# Success test page (optional)
@app.route('/test-success')
def test_success():
    class FakeOrder:
        id = 123
        total = 25.99
    return render_template('success.html', order=FakeOrder())

# Admin view of all orders
@app.route('/admin/orders')
def admin_orders():
    orders = Order.query.all()
    print(f"[DEBUG] Fetched {len(orders)} orders from database")
    return render_template('admin_orders.html', orders=orders)

# Route to update order status
@app.route('/admin/orders/<int:order_id>/update_status', methods=['POST'])
def update_order_status(order_id):
    new_status = request.form.get('status')
    valid_statuses = ['Pending', 'Preparing Order', 'Rider on the Way', 'Order Complete']
    if new_status not in valid_statuses:
        return "Invalid status", 400
    order = Order.query.get_or_404(order_id)
    order.status = new_status
    db.session.commit()
    return redirect(url_for('admin_orders'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        if not Food.query.first():
            sample_foods = [
                Food(name="Burger", amount=10, price=5.99, description="Juicy beef burger"),
                Food(name="Pizza", amount=5, price=8.99, description="Cheesy pepperoni pizza"),
                Food(name="Fries", amount=15, price=2.99, description="Golden crispy fries"),
            ]
            db.session.add_all(sample_foods)
            db.session.commit()
            print("[DEBUG] Sample food items added.")

    app.run(debug=True)
