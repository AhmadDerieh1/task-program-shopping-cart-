import mysql.connector
from Customer import Customer
from Item import Item
from Shopping_cart import ShoppingCart

#connection 
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ahmadayham20",
    database="shopping_cart"
)
customer_name = input("Enter your name: ")
customer_email = input("Enter your email: ")
customer_phone = input("Enter your phone number: ")

customer = Customer(customer_name, customer_email, customer_phone)

cart = ShoppingCart(customer)
cart_items = []
while True:
    item_name = input("Enter item name (or 'done' to finish): ")
    if item_name.lower() == "done":
        break

    item_quantity = int(input("Enter quantity: "))
    item_price = float(input("Enter item price: "))

    item = Item(item_name, item_price)
    cart_items.append(item)
    cart.add_item(item, item_quantity)
cart.display_cart()
discount = cart.discount(0.1)
print("Total after discount:", discount[0])
print("Discount amount:", discount[1])

try:
    cursor = connection.cursor()

    # Insert data into customers table
    insert_customer_query = "INSERT INTO customers (name, email, phone_number) VALUES (%s, %s, %s)"
    customer_data = (customer.get_name(), customer.get_email(), customer.get_phone_number())
    cursor.execute(insert_customer_query, customer_data)
    connection.commit()
    customers_id = cursor.lastrowid
    
    # Insert data into items table
    item_id = []
    for item in cart_items:
        item_query = "INSERT INTO items (item_name, price) VALUES (%s, %s)"
        item_data = (item.get_item_name(), item.get_price())
        cursor.execute(item_query, item_data)
        connection.commit()
        item_id.append(cursor.lastrowid)  
    
    # Insert data into cart table
    quantity_list = cart.get_quantity()
    cart_query = "INSERT INTO cart (customer_id, item_id, quantity) VALUES (%s, %s, %s)" ##
    for i, item_id in enumerate(item_id):
        cart_data = (customers_id, item_id, quantity_list[i])
        cursor.execute(cart_query, cart_data)
        connection.commit()

except mysql.connector.Error as err:
    print("Error:", err)
    connection.rollback() 

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()