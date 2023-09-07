from ORM import Customers, Items, Carts
from Customer import Customer
from Item import Item
from Shopping_cart import ShoppingCart
from sqlalchemy import create_engine, Column, CHAR, Integer, ForeignKey, Float ,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError  

try:
    customer_name = input("Enter your name: ")
    customer_email = input("Enter your email: ")
    customer_phone = input("Enter your phone number: ")
    customer = Customer(customer_name, customer_email, customer_phone)
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
    total = discount[0]

    Base = declarative_base()
    db_url = 'mysql+mysqlconnector://root:Ahmadayham20@localhost:3306/shopping_cart'
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        
       customer = Customers(customer_name, customer_email, customer_phone)
       session.add(customer)
       session.commit()
    except SQLAlchemyError as e:
       print("An error occurred while interacting with the calss Customers:", e)

    try:
       item_ids = []

       for name, price in cart_items.items():
          item_cart = Items(name, price)
          session.add(item_cart)
          session.flush()  
          item_ids.append(item_cart.item_id)  
       session.commit()
    except SQLAlchemyError as e:
       print("An error occurred while interacting with the calss Items:", e)

    try:
      quantity_list = cart.get_quantity()
      for i, item_id in enumerate(item_ids):
          cart_data = Carts(customer.customer_id, item_ids[i], quantity_list[i], customer.customer_id, total)
          session.add(cart_data)
      session.commit()
    except SQLAlchemyError as e:
       print("An error occurred while interacting with the calss Carts:", e)

except SQLAlchemyError as e:
    print("An error occurred while interacting with the database:", e)
finally:
    session.close()  