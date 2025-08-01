from flask import request,render_template,make_response
from datetime import datetime
from model import *
from flask_restful import Resource



class AllCustomers(Resource):
    def get(self):
        customers = Customer.query.all()
        result = []
        for x in customers:
            result.append({
                "Customer ID:": x.customer_id,
                "First Name": x.first_name,
                "Last Name": x.last_name,
                "E-Mail": x.email,
                "Phone": x.phone,
                "Created At:": x.created_at.isoformat()
                # datetime(2025, 7, 31, 10, 45, 30).isoformat() -> Output: "2025-07-31T10:45:30"(str)
                # normal str conversion doesnt work with datetime
            })
        return result

class AllOrders(Resource):
    def get(self):
        orders = Order.query.all()
        result = []
        for x in orders:
            result.append({
                "Order ID:": x.order_id,
                "Customer ID:": x.customer_id,
                "Order Date:": x.order_date.isoformat(),
                "Total Amount:": x.total_amount,
                "Order Status:": x.status
            })
        return result

class Home(Resource):
    def get(self):
        return "Hello, this is home page!"

class AddCustomer(Resource):
    def post(self):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        new_customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            created_at=datetime.now()
        )
        db.session.add(new_customer)
        db.session.commit()
        return f"Customer {first_name} added successfully!"
    
    def get(self):
        return make_response(render_template('add_customer.html'))
        # this make_response is used because we want to tell flask-restful to return template as it is and not in json format
    

class AddOrder(Resource):
    def post(self):
        customer_id = request.form['customer_id']
        total_amount = request.form['total_amount']
        status = request.form['status']
        new_order = Order(
            customer_id=customer_id,
            order_date=datetime.now(),
            total_amount=total_amount,
            status=status
        )
        db.session.add(new_order)
        db.session.commit()
        return "Order added successfully!"
    def get(self):
        return make_response(render_template('add_order.html'))

class EditCustomer(Resource):
    def post(self, id):
        customer = Customer.query.get_or_404(id)
        customer.first_name = request.form['first_name']
        customer.last_name = request.form['last_name']
        customer.email = request.form['email']
        customer.phone = request.form['phone']
        db.session.commit()
        return f"Customer {customer.first_name} updated successfully!"
    def get(self, id):
        customer = Customer.query.get_or_404(id)
        return make_response(render_template('edit_customer.html', user=customer))

class EditOrder(Resource):
    def post(self, id):
        order = Order.query.get_or_404(id)
        order.customer_id = request.form['customer_id']
        order.order_date = datetime.now()
        order.total_amount = request.form['total_amount']
        order.status = request.form['status']
        db.session.commit()
        return f"Order {order.order_id} updated successfully!"
    def get(self, id):
        order = Order.query.get_or_404(id)
        return make_response(render_template('edit_order.html', order=order))

class DeleteCustomer(Resource):
    def delete(self, id):
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return f"Customer {customer.first_name} deleted successfully!"
    
class DeleteOrder(Resource):
    def delete(self, id):
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return f"Order {order.order_id} deleted successfully!"