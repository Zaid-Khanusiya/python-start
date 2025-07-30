from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

'''
curl -X POST http://127.0.0.1:5008/contact/1 \
-H "Content-Type: application/json" \
-d '{"name": "Nemesis", "phone": "9844558007"}'
-------------------------------------------------------
curl -X PUT http://127.0.0.1:5008/contact/1 \
-H "Content-Type: application/json" \
-d '{"name": "Nemesis Updated", "phone": "0001112222"}'
-------------------------------------------------------
curl -X DELETE http://127.0.0.1:5008/contact/1
'''

app = Flask(__name__)  # This thing will create a flask app 
api = Api(app)  # This will connect Flask-RESTful to the app we created one the line before

# This thing just connects to our sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# this is our model in sqlite
class ContactModel(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))

# This are the classes we defined to route by resourceful
class AllContacts(Resource):
    def get(self):
        all_contacts = ContactModel.query.all()
        result = []
        for contact in all_contacts:
            result.append({
                "id": contact.id,
                "name": contact.name,
                "phone": contact.phone
            })
        return result

class Contact(Resource):
    def post(self, contact_id):
        data = request.get_json()
        contact = ContactModel(id=contact_id, name=data['name'], phone=data['phone'])
        db.session.add(contact)
        db.session.commit()
        return f"Your Data Is Saved: {data}"

    def get(self, contact_id):
        contact = ContactModel.query.get(contact_id)
        if contact:
            return {
                "id": contact.id,
                "name": contact.name,
                "phone": contact.phone
            }
        else:
            return "The Specified Contact Is Not Found!", 404
    
    def put(self, contact_id):
        contact = ContactModel.query.get(contact_id)
        if contact:
            data = request.get_json()
            contact.name = data['name']
            contact.phone = data['phone']
            db.session.commit()
            return "Contact Is Updated Successfully!"
        else:
            return "The Specified Contact Is Not Found!", 404
        
    def delete(self, contact_id):
        contact = ContactModel.query.get(contact_id)
        if contact:
            db.session.delete(contact)
            db.session.commit()
            return "Contact Deleted Successfully!"
        else:
            return "The Specified Contact Is Not Found!", 404


api.add_resource(AllContacts, '/contacts')
api.add_resource(Contact, '/contact/<string:contact_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create the table if it doesn't exist
    app.run(debug=True, port=5008)