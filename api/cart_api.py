import logging
import traceback
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ORM import Carts ,Customers ,Items  # Import the Cart model

logging.basicConfig(filename='cart.log', level=logging.INFO)
app = Flask(__name__)

# Database setup
try:
    db_url = 'mysql+mysqlconnector://root:Ahmadayham20@localhost:3306/shopping_cart'
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
except SQLAlchemyError as e:
    # Log the error
    logging.error(str(e))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.json
        customer_id = data.get('customer_id')
        
        # Validate input using the invalid_input function
        invalid_input_response = invalid_input(data)
        if invalid_input_response:
            return invalid_input_response
        
        item_id = data.get('item_id')
        quantity = data.get('quantity')
        
        # Check if the cart and item exist
        customer = session.query(Customers).filter_by(customer_id=customer_id).first()
        item = session.query(Items).filter_by(item_id=item_id).first()

        if not customer:
            return jsonify({"error": "Customer not found."}), 404
        if not item:
            return jsonify({"error": "Item not found."}), 404

        # Calculate the total price based on item price and quantity
        if item.price is not None and quantity is not None and quantity > 0:
            total = item.price * quantity
        else:
            return jsonify({"error": "Invalid price or quantity."}), 400

        cart_entry = Carts(customer_id, item_id, quantity,customer_id,total)
        
        session.add(cart_entry)
        session.commit()

        logging.info(f"Added item to cart: Customer {customer_id}, Item {item_id}, Quantity {quantity}, Total {total}")
        return jsonify({"message": "Item added to cart successfully!"}), 201

    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
        return jsonify({"error": "An error occurred."}), 500

    except Exception as e:
        handle_generic_exception(e)
        return jsonify({"message": "An unexpected error occurred."}), 403

@app.route('/delete_cart', methods=['DELETE'])
def delete_cart():
    try:
        data = request.json
        invalid_input_response = invalid_input(data)
        if invalid_input_response:
            return invalid_input_response
       
        # Check if the customer exists
        not_found_response = cart_not_found(data)
        if not_found_response:
            return not_found_response 
        customer_id = data.get('customer_id')
        item_id = data.get('item_id')
        quantity = data.get('quantity')
    
        # Check if the cart entry exists
        cart_entry = session.query(Carts).filter_by(customer_id=customer_id, item_id=item_id, quantity=quantity).first()

        if not cart_entry:
            return jsonify({"error": "Cart entry not found."}), 404

            # Delete the cart entry
        session.delete(cart_entry)
        session.commit()

        logging.info(f"Deleted cart entry: Customer {customer_id}, Item {item_id}, Quantity {quantity}")
        return jsonify({"message": "Cart entry deleted successfully!"}), 200

    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
        return jsonify({"error": "An error occurred while accessing the database."}), 500

    except Exception as e:
        handle_generic_exception(e)
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/get_cart', methods=['GET'])
def get_cart():
    try:
        data = request.json
      # Validate input using the invalid_input function
        invalid_input_response = invalid_input(data)
        if invalid_input_response:
            return invalid_input_response
        
        customer_id = data.get('customer_id') 

           # Check if the customer exists
        not_found_response = cart_not_found(data)
        if not_found_response:
            return not_found_response 

        cart_entries = session.query(Carts).filter_by(customer_id=customer_id).all()

        if not cart_entries:
            return jsonify({"error": "Cart is empty for the specified customer."}), 404

        cart_data = [{"item_id": entry.item_id, "quantity": entry.quantity} for entry in cart_entries]

        return jsonify({"cart": cart_data}), 200

    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
        return jsonify({"error": "An error occurred while accessing the database."}), 500

    except Exception as e:
        handle_generic_exception(e)
        return jsonify({"error": "An unexpected error occurred."}), 500


def handle_sqlalchemy_error(exception):
    # you don't want to display what the error details  for user 
    error_message = "An error occurred " #+ str(exception) # to the database:
    logging.error(error_message)

def handle_generic_exception(exception):
    error_message = "An unexpected error occurred: " + str(exception)
    traceback.print_exc()  
    logging.error(error_message)

def invalid_input(data):
    customer_id = data.get('customer_id')
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    if customer_id < 0 or item_id < 0 or quantity < 0 :
            return jsonify({"error": "Invalid input. Please provide customer_id, item_id, and quantity."}), 400
    if not customer_id or not item_id  or not quantity:
            return jsonify({"error": "Invalid input. Please provide customer_id, item_id, and quantity."}), 400

def cart_not_found(data):
    customer_id = data.get('customer_id')
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    deleted_customer = session.query(Carts).filter_by(customer_id=customer_id, item_id=item_id, quantity=quantity).first()
    if not deleted_customer:
        return jsonify({"error": "cart not found."}), 404


if __name__ == '__main__':
    app.run(debug=True)