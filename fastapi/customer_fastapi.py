from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ORM import Customers
import logging
logging.basicConfig(filename='customer_fastapi.log', level=logging.INFO)
app = FastAPI()

class CustomerBase(BaseModel):
    name: str
    email: str
    phone_number: str

# Database Connection
db_url = 'mysql+mysqlconnector://root:Ahmadayham20@localhost:3306/shopping_cart'
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/customers/{customer_id}")
def read_customer(customer_id: int):
    db = SessionLocal()
    customer = db.query(Customers).filter(Customers.customer_id == customer_id).first()
    db.close()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/add_customer/")
def create_customer(customer: CustomerBase):
    try:
       db = SessionLocal()

    # Check if the customer already exists
       existing_customer = db.query(Customers).filter_by(name=customer.name, phone_number=customer.phone_number).first()
       if existing_customer:
          db.close()
          return {"error": "Customer with the same name and phone number already exists."}, 400

       db_customer = Customers(name=customer.name, email=customer.email, phone_number=customer.phone_number)
    
    # Validate data using rules function
       validation_result = text_len(db_customer)
       if validation_result:
          return validation_result 
        
    # Validate input 
       invalid_input_response = invalid_input(db_customer)
       if invalid_input_response:
          return invalid_input_response
        
       db.add(db_customer)
       db.commit()
       db.refresh(db_customer)
       db.close()
       return db_customer

    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
        return ({"error": "An error occurred."}), 500

    except Exception as e:
        handle_generic_exception(e)
        return ({"message": "An unexpected error occurred."}), 403


@app.delete("/delete_customer/{customer_id}")
def delete_customer(customer_id: int):
    try:
        db = SessionLocal()
    
        customer = db.query(Customers).filter(Customers.customer_id == customer_id).first()
    
    # Check if the customer exists
        if customer is None or  not customer :
            db.close()
            raise HTTPException(status_code=404, detail="Customer not found")
    
    # Delete the customer
        db.delete(customer)
        db.commit()
        db.close()
        return {"message": "Customer deleted successfully"}
   
    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
        return ({"error": "An error occurred."}), 500

    except Exception as e:
        handle_generic_exception(e)
        return ({"message": "An unexpected error occurred."}), 403


def text_len(customer):
    name = customer.name
    email = customer.email
    phone_number = customer.phone_number
        # Check phone number length
    if len(phone_number) < 10 and len(name) < 50 and len(email) < 100:
        return ({"error": "Phone number must have at least 10 digits, name must have at least 50 characters, email must have at least 100 characters"}), 400

def invalid_input(customer):
    name = customer.name
    email = customer.email
    phone_number = customer.phone_number
    if not name or not email or not phone_number:
            return ({"error": "Invalid input. Please provide name, email, and phone_number."}),400
    

def handle_sqlalchemy_error(exception):
    # you don't want to display what the error details  for user 
    error_message = "An error occurred " + str(exception) # to the database:
    logging.error(error_message)

def handle_generic_exception(exception):
    # you don't want to display what the error details  for user 
    error_message = "An unexpected error occurred: "  + str(exception)
    logging.exception(error_message)