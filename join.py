from ORM import Customers, Items, Carts
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
db_url = 'mysql+mysqlconnector://root:Ahmadayham20@localhost:3306/shopping_cart'
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()
try:
    customer_name = input("Enter the customer name: ")
    query = session.query(
        Carts.id,
        Customers.customer_id,
        Customers.name,
        Items.item_id,
        Items.item_name,
        Items.price,
        Carts.quantity,
        Carts.total
    ).join(
        Customers, Carts.customer_id == Customers.customer_id
    ).join(
        Items, Carts.item_id == Items.item_id
    ).filter(
        Customers.name == customer_name
    )

    filter_results = query.all()

    if not filter_results:
        print(f"Customer with name '{customer_name}' does not exist.")
    else:
        for result in filter_results:
            print(f"Cart ID: {result.id}, Customer ID: {result.customer_id}, Customer Name: {result.name}, Item ID: {result.item_id}, Item Name: {result.item_name}, Price: {result.price}, Quantity: {result.quantity}, Total: {result.total}")

except Exception as e:
    print("An error occurred:", e)
finally:
    session.close()