import logging
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ORM import Customers  

logging.basicConfig(filename='shopping_cart.log', level=logging.INFO)
app = Flask(__name__)
db_url = 'mysql+mysqlconnector://root:Ahmadayham20@localhost:3306/shopping_cart'
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        customer = Customers(name=name, email=email, phone_number=phone_number)
        session.add(customer)
        session.commit()
        
        logging.info(f"Added customer: {name}, Email: {email}, Phone: {phone_number}")
        return jsonify({"message": "Customer added successfully!"}), 201

    except SQLAlchemyError as e:
        session.rollback()
        error_message = "An error occurred while adding the customer to the database."
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

    except Exception as e:
        logging.exception("An unexpected error occurred.")
        return jsonify({"message": "Customer added successfully!"}), 403

    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)