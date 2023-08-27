class Item:

    def __init__(self, item_name="Default Item", price=0):
        self._item_name = item_name
        self._price = price
        self._item_id = 1  

    
    def get_item_name(self):
        return self._item_name
    
    def set_item_name(self, item_name):
        self._item_name = item_name
    
    def get_price(self):
        return self._price
    
    def set_price(self, price):
        self._price = price
    
    def get_item_id(self):
        return self._item_id
