from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash  # Import generate_password_hash
from functools import wraps
import secrets
app = Flask(__name__)

def generate_token():
    token = secrets.token_hex(16)  
    return token
try:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Ahmadayham20@localhost:3306/shopping_cart'
    app.config['SECRET_KEY'] = 'SECRET_KEY'
    db = SQLAlchemy(app)
except Exception as e:
    print(f"Error: {str(e)}")  
    raise  

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    token = db.Column(db.String(32), unique=True, nullable=True)  # Add a token 
with app.app_context():
     db.create_all()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            token = generate_token()
            user.token = token
            db.session.commit()
            response = jsonify({'access_token': token})
            response.set_cookie('access_token', token, max_age=3600, secure=True, httponly=True)

            return response, 200
        else:
            return {'message': 'Invalid credentials'}, 401

    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return {'message': 'An error occurred while processing your request'}, 500


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'message': 'Username already exists'}, 400

        hashed_password = (password)

        # Create a new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201

    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return {'message': 'An error occurred while processing your request'}, 500


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if token and User.query.filter_by(token=token).first():
                return f(*args, **kwargs)
            else:
                return jsonify({'message': 'Token is missing or invalid'}), 401
        except Exception as e:
            print(f"Error: {str(e)}")  
            return jsonify({'message': 'An error occurred while processing your request'}), 500
    return decorated_function

@app.route('/protected-resource', methods=['GET'])
def protected_resource():
    # Check if user is logged in
    if 'user_id' in session:
        return {'message': 'This is a protected resource'}, 200
    else:
        return jsonify({'message': 'Unauthorized access'}), 401

if __name__ == "__main__":
    app.run(debug=True, port=3000)
