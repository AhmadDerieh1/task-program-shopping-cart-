from Item import Item
from Customer import Customer

class ShoppingCart:
    def __init__(self, customer):
        self._customer = customer
        self._shopping_cart = {}
        self._cart_id = 1

    def add_item(self, item, quantity = 1):
        if item in self._shopping_cart:
            self._shopping_cart[item] += quantity
        else:
            self._shopping_cart[item] = quantity

    def remove_item(self, item):
        if item in self._shopping_cart:
            del self._shopping_cart[item]
        else:
            print("The "+item +" is not in the cart.")

    def get_quantity(self):
        if  len(self._shopping_cart) != 0:
            values_list = list(self._shopping_cart.values())
            return values_list
        else:
            return 0

    def calculate_total(self):
        total_value = 0
        for item, quantity in self._shopping_cart.items():
            total_value += item.get_price() * quantity
        return total_value
    
    def discount(self, discount_amount):
        total_discount = self.calculate_total() * discount_amount
        total = self.calculate_total() - total_discount
        return (total, total_discount)

    def display_cart(self):
        print("Customer: "+ self._customer.get_name() +" Email: "+ self._customer.get_email() + " Phone number: " + self._customer.get_phone_number())
        print("Items in your cart:")
        
        for item, quantity in self._shopping_cart.items():
            item_total = item.get_price() * quantity
            print(item.get_item_name() + "- Quantity: "+ str(quantity) + " Price: "+str(item.get_price()) + " Total: "+str(item_total) )
            
        total_value = self.calculate_total()
        print("Total: "+ str(total_value))
        
    def print_items(self):
        print("Items in the cart:")
        for item in self._shopping_cart.keys():  # Fixed typo here
            print(item.get_item_name())