from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple.db'
db = SQLAlchemy(app)
# Run this only once so the Database Tables get created
db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

@app.route('/')
def index():
    users = User.query.all()
    return str([user.name for user in users])

@app.route('/add/<user>')
def add_user(user):
    new_user = User(name=user)
    db.session.add(new_user)
    db.session.commit()
    return f"User {user} added successfully."

@app.route('/delete/<user>')
def delete_user(user):
    user_to_delete = User.query.filter_by(name=user).first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return f"User {user} deleted successfully."
    else:
        return f"User {user} not found."

if __name__ == '__main__':
    app.run(debug=True,port=5003)