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
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
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
        return "Send a POST request with JSON data to add a customer."
    
class AddOrder(Resource):
    def post(self):
        data = request.get_json()
        customer_id = data.get('customer_id')
        total_amount = data.get('total_amount')
        status = data.get('status')
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
        return "Send a POST request with JSON data to add an order."

class EditCustomer(Resource):
    def put(self, id):
        customer = Customer.query.get_or_404(id)
        data = request.get_json()
        customer.first_name = data.get('first_name', customer.first_name)
        customer.last_name = data.get('last_name', customer.last_name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)
        db.session.commit()
        return f"Customer {customer.first_name} updated successfully!"
    def get(self, id):
        customer = Customer.query.get_or_404(id)
        return {
            "id": customer.id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone
        }

class EditOrder(Resource):
    def put(self, id):
        order = Order.query.get_or_404(id)
        data = request.get_json()
        order.customer_id = data.get('customer_id', order.customer_id)
        order.order_date = datetime.now()  # always update to now
        order.total_amount = data.get('total_amount', order.total_amount)
        order.status = data.get('status', order.status)
        db.session.commit()
        return f"Order {order.order_id} updated successfully!"
    def get(self, id):
        order = Order.query.get_or_404(id)
        return {
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "total_amount": order.total_amount,
            "status": order.status
        }

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