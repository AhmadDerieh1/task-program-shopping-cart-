import logging
import traceback
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ORM import Items 
logging.basicConfig(filename='item.log', level=logging.INFO)

app = Flask(__name__)

try:
    db_url = 'mysql+mysqlconnector://root:Ahmadayham20@localhost:3306/shopping_cart'
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
except SQLAlchemyError as e:
    # Log the error
     logging.error(str(e))


@app.route('/add_item',methods=['POST'])
def add_item():
    try:
        data =  request.json
        # Validate input using the invalid_input function
        invalid_input_response = invalid_input(data)
        if invalid_input_response:
            return invalid_input_response

        item_name = data.get('item_name')
        price = data.get('price')

        existing_item = session.query(Items).filter_by(item_name=item_name, price=price).first()  
        if existing_item:
            return jsonify({"error": "item with the same name and price already exists."}), 400
        
        # Validate data 
        validation_result = text_len(data)
        if validation_result:
            return validation_result 
   
        customer = Items(item_name, price)
        session.add(customer)
        session.commit()

        logging.info(f"Added item: {item_name}, price: {price}")
        return jsonify({'message':'item added successfully!'}),201

    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
        return jsonify({"error": "An error occurred."}), 500
  
    except ValueError: 
        return jsonify({"Error: You did not enter a valid integer."})

    except Exception as e:
        handle_generic_exception(e)
        return jsonify({"message": "An unexpected error occurred."}), 403
       
@app.route('/delete_item',methods= ['DELETE'])
def delete_item():
    try:
        data= request.json
        # Validate input using the invalid_input function
        invalid_input_response = invalid_input(data)
        if invalid_input_response:
            return invalid_input_response

        item_name = data.get('item_name')
        price = data.get('price')

      # Validate data using rules function
        validation_result = text_len(data)
        if validation_result:
            return validation_result 
                
    
        # Check if the customer exists
        not_found_response = item_not_found(data)
        if not_found_response:
            return not_found_response
        
        deleted_customer  = session.query(Items).filter_by(item_name=item_name, price=price).first()        
        session.delete(deleted_customer)
        session.commit()
        logging.info(f"Deleted item: {item_name}")
        return({"message": "item deleted successfully!"}),200
    
    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
        return jsonify({"error": "An error occurred while delete"}), 500 # error in deleting in database
    
    except ValueError: 
        return jsonify({"Error: You did not enter a valid integer."})

    except Exception as e:
        handle_generic_exception(e)
        return jsonify({"error": "An unexpected error occurred."}), 500
    
@app.route('/get_item',methods= ['GET'])
def get_item():
    try:    
        data= request.json
        #Validate input 
        invalid_input_response = invalid_input(data)
        if invalid_input_response:
            return invalid_input_response
       
        item_name = data.get('item_name')
        price = data.get('price')
        
        # Validate data using rules function
        validation_result = text_len(data)
        if validation_result:
            return validation_result 

        # Check if the customer exists
        not_found_response = item_not_found(data)
        if not_found_response:
            return not_found_response 
        item = session.query(Items).filter_by(item_name=item_name, price=price).first()
        item_data = {
            "itme_name": item.item_name,
            "email": item.price
            }
        return jsonify(item_data), 200
    
    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
        return jsonify({"error": "An error occurred."}), 500
    
    except ValueError: 
         return jsonify({"Error: You did not enter a valid integer."})
    
    except Exception as e:
        handle_generic_exception(e)
        return jsonify({"error": "An unexpected error occurred."}), 500
    
 

def handle_sqlalchemy_error(exception):
    # you don't want to display what the error details  for user 
    error_message = "An error occurred " #+ str(exception) # to the database:
    logging.error(error_message)

def handle_generic_exception(exception):
    error_message = "An unexpected error occurred: " + str(exception)
    traceback.print_exc()  # Log the exception stack trace
    logging.error(error_message)

def text_len(data):
    item_name = data.get('item_name')
    price = data.get('price')
    if len(item_name) > 100:
        return jsonify({"error": "Item name is too long."}), 400
    if  price < 0:
        return jsonify({"error": "Invalid price."}), 400
    return None

def invalid_input(data):
    item_name = data.get('item_name')
    price = data.get('price')
    if not item_name or not price :
            return jsonify({"error": "Invalid input. Please provide item name, price."}),400

def item_not_found(data):
    item_name = data.get('item_name')
    price = data.get('price')
    deleted_customer = session.query(Items).filter_by(item_name=item_name, price=price).first()
    if not deleted_customer:
        return jsonify({"error": "item not found."}), 404

if __name__ == '__main__':
    app.run(debug=True) 