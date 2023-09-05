
from sqlalchemy import create_engine, Column, CHAR, Integer, ForeignKey, Float ,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

class Customer_db(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50) ,nullable= False)
    email = Column(String(100) ,nullable= False)
    phone_number = Column(String(10))
    
    def __init__(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.customer_id
    
    def get_customer_id(self):
        return self.customer_id 

    def __repr__(self):
        return f"({self.customer_id}) {self.name} {self.email} {self.phone_number}"


class Item_db(Base):
    __tablename__ = "items"
    
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String(100),nullable= False)
    price = Column(Float,nullable= False)

    def __init__(self, item_name, price):
        self.item_name = item_name
        self.price = price
    
    def get_item_id(self):
        return self.item_id 
    
    def __repr__(self):
        return f"({self.item_id}) {self.item_name} {self.price}"


class Cart_db(Base):
    __tablename__ = "cart"

    cart_item_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    item_id = Column(Integer, ForeignKey('items.item_id'))
    quantity = Column(Integer)

    def __init__(self, customer_id, item_id, quantity):
        self.customer_id = customer_id
        self.item_id = item_id
        self.quantity = quantity

    customer = relationship("Customer_db")
    item = relationship("Item_db")

    def __repr__(self):
        return f"({self.cart_item_id}) {self.customer} {self.item} {self.quantity})"
