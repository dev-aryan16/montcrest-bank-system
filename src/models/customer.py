class Customer:
    def __init__(self,customer_id,first_name,last_name,date_of_birth,email,phone_number,address):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.phone_number = phone_number
        self.address = address

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_email(self, new_email):
        self.email = new_email

    def update_phone_number(self, new_phone_number):
        self.phone_number = new_phone_number

    def update_address(self, new_address):
        self.address = new_address

    def get_customer_info(self):
        return {
            "Customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "Date_of_birth": self.date_of_birth
        }


c1=Customer(1,"John","Doe","1990-01-01","john.doe@example.com","123-456-7890","123 Main St")
print(c1.get_customer_info())