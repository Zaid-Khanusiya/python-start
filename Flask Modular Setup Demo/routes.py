from app import myapp,api
from views import *


api.add_resource(Home, '/')
api.add_resource(AllCustomers, '/customers')
api.add_resource(AllOrders, '/orders')
api.add_resource(AddCustomer, '/add_customer')
api.add_resource(AddOrder, '/add_order')
api.add_resource(EditCustomer, '/edit_customer/<int:id>')
api.add_resource(EditOrder, '/edit_order/<int:id>')
api.add_resource(DeleteCustomer, '/delete_customer/<int:id>')
api.add_resource(DeleteOrder, '/delete_order/<int:id>')