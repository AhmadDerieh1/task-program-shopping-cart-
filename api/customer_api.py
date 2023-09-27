import logging
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ORM import Customers 

logging.basicConfig(filename='customer.log', level=logging.INFO)
app = Flask(__name__)
try:
    db_url = 'mysql+mysqlconnector://root:Ahmadayham20@localhost:3306/shopping_cart'
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

except SQLAlchemyError as e:
    # Log the error
     logging.error(str(e))

finally:
        session.close()
@app.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')

        existing_customer = session.query(Customers).filter_by(name=name, phone_number=phone_number).first()  
        if existing_customer:
            return jsonify({"error": "Customer with the same name and phone number already exists."}), 400

        # Validate data using rules function
        validation_result = text_len(data)
        if validation_result:
            return validation_result 
        
        # Validate input 
        invalid_input_response = invalid_input(data)
        if invalid_input_response:
            return invalid_input_response

        customer = Customers(name, email, phone_number)
        session.add(customer)
        session.commit()
        logging.info(f"Added customer: {name}, Email: {email}, Phone: {phone_number}")
        return jsonify({"message": "Customer added successfully!"}), 201

    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
        return jsonify({"error": "An error occurred."}), 500

    except Exception as e:
        handle_generic_exception(e)
        return jsonify({"message": "An unexpected error occurred."}), 403

@app.route('/delete_customer',methods=['DELETE'] )
def delete_customer():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')

        # Validate data using rules function
        validation_result = text_len(data)
        if validation_result:
            return validation_result
        
        # Validate input using the invalid_input function
        invalid_input_response = invalid_input(data)
        if invalid_input_response:
            return invalid_input_response

         # Check if the customer exists
        not_found_response = customer_not_found(data)
        if not_found_response:
            return not_found_response

        deleted_customer  = session.query(Customers).filter_by(name=name, email=email, phone_number=phone_number).first()        
        session.delete(deleted_customer)
        session.commit()
        logging.info(f"Deleted customer: {name}, Email: {email}, Phone: {phone_number}")
        return({"message": "Customer deleted successfully!"}),200
    
    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
        return jsonify({"error": "An error occurred while delete"}), 500 # error in deleting in database

    except Exception as e:
        handle_generic_exception(e)
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/get_customer', methods=['GET'])
def get_customer():
    try:
        data = request.json
        # Validate input using the invalid_input function
        invalid_input_response = invalid_input(data)
        if invalid_input_response:
            return invalid_input_response

        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')

     # Validate data using rules function
        validation_result = text_len(data)
        if validation_result:
            return validation_result 

        # Check if the customer exists
        not_found_response = customer_not_found(data)
        if not_found_response:
            return not_found_response

        customer = session.query(Customers).filter_by(name=name, email=email, phone_number=phone_number).first()
        customer_data = {
            "name": customer.name,
            "email": customer.email,
            "phone_number": customer.phone_number
        }
        return jsonify(customer_data), 200

    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
        return jsonify({"error": "An error occurred."}), 500
    
    except Exception as e:
        handle_generic_exception(e)
        return jsonify({"error": "An unexpected error occurred."}), 500

def handle_sqlalchemy_error(exception):
    # you don't want to display what the error details  for user 
    error_message = "An error occurred " #+ str(exception) # to the database:
    logging.error(error_message)

def handle_generic_exception(exception):
    # you don't want to display what the error details  for user 
    error_message = "An unexpected error occurred: "#  + str(exception)
    logging.exception(error_message)

def customer_not_found(data):
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    deleted_customer = session.query(Customers).filter_by(name=name, email=email, phone_number=phone_number).first()
    if not deleted_customer:
        return jsonify({"error": "Customer not found."}), 404

def text_len(data):
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
        # Check phone number length
    if len(phone_number) < 10 and len(name) < 50 and len(email) < 100:
        return jsonify({"error": "Phone number must have at least 10 digits, name must have at least 50 characters, email must have at least 100 characters"}), 400

def invalid_input(data):
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    if not name or not email or not phone_number:
            return jsonify({"error": "Invalid input. Please provide name, email, and phone_number."}),400


if __name__ == '__main__':
    app.run(debug=True) 