from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash  # Import generate_password_hash
from functools import wraps
import secrets
app = Flask(__name__)

def generate_token():
    token = secrets.token_hex(16)  # Generate a random token (hexadecimal representation)
    return token
try:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Ahmadayham20@localhost:3306/shopping_cart'
    app.config['SECRET_KEY'] = 'SECRET_KEY'
    db = SQLAlchemy(app)
except Exception as e:
    print(f"Error: {str(e)}")  # Log the error for debugging purposes
    raise  # Re-raise the exception to halt the program execution

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    token = db.Column(db.String(32), unique=True, nullable=True)  # Add a token field to the User model
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
            token = generate_token()
            user.token = token
            db.session.commit()
            # Create a response object
            response = jsonify({'access_token': token})

            # Set the access token as a cookie in the response
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

        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'message': 'Username already exists'}, 400

        # Hash the password before storing it in the database
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
            print(f"Error: {str(e)}")  # Log the error for debugging purposes
            return jsonify({'message': 'An error occurred while processing your request'}), 500
    return decorated_function

@app.route('/protected-resource', methods=['GET'])
@token_required
def protected_resource():
    return {'message': 'This is a protected resource'}, 200


if __name__ == "__main__":
    app.run(debug=True, port=3000)
