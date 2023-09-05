from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from ORM import Customer_db, Item_db, Cart_db
from Customer import Customer
from Item import Item
from Shopping_cart import ShoppingCart

# Initialize SQLAlchemy
Base = declarative_base()
db_url = 'mysql+mysqlconnector://root:Ahmadayham20@localhost:3306/shopping_cart'
engine = create_engine(db_url)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create a session
Session = sessionmaker(bind=engine)

try:
    # Get user input for customer information
    customer_name = input("Enter your name: ")
    customer_email = input("Enter your email: ")
    customer_phone = input("Enter your phone number: ")

    # Create a Customer object
    customer = Customer(customer_name, customer_email, customer_phone)

    # Create a ShoppingCart object
    cart = ShoppingCart(customer)
    cart_items = {}

    while True:
        item_name = input("Enter item name (or 'done' to finish): ")
        if item_name.lower() == "done":
            break

        item_quantity = int(input("Enter quantity: "))
        item_price = float(input("Enter item price: "))

        item = Item(item_name, item_price)
        cart_items[item.get_item_name()] = item.get_price()
        cart.add_item(item, item_quantity)

    cart.display_cart()
    discount = cart.discount(0.1)
    print("Total after discount:", discount[0])
    print("Discount amount:", discount[1])

    # Create a session
    session = Session()

    # Add customer to the database
    customer_db = Customer_db(customer_name, customer_email, customer_phone)
    session.add(customer_db)

    # Add items to the database and create a list of item_ids
    item_ids = []
    for name, price in cart_items.items():
        item_cart = Item_db(item_name=name, price=price)
        session.add(item_cart)
        session.flush()  # Synchronize with the database and get the item_id
        item_ids.append(item_cart.item_id)

    # Add cart data to the database
    quantity_list = cart.get_quantity()
    for i, item_id in enumerate(item_ids):
        cart_data = Cart_db(customer.customer_id,item_ids[i],quantity_list[i])
        session.add(cart_data)

    # Commit the transaction
    session.commit()

except Exception as e:
    print("An error occurred:", str(e))
finally:
    session.close()  # Ensure the session is closed, even in case of an error

    
    
