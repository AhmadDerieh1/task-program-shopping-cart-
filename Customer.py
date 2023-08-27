class Customer:   
    def __init__(self, name="Default Name", email="default@example.com", phone_number="000-000-0000"):
        self._name = name
        self._email = email
        self._phone_number = phone_number
        self._customer_id = 1  
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
    
    def get_email(self):
        return self._email
    
    def set_email(self, email):
        self._email = email
        
    def set_phone_number(self, phone_number):
        self._phone_number = phone_number
   
    def get_phone_number(self):
        return self._phone_number
    
    def get_customer_id(self):
        return self._customer_id