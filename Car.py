from datetime import datetime

class Car:
    def __init__(self, car_id,  make, model, year, rental_price, available = True):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.rental_price = rental_price
        self.available = available
        

    def is_available(self):
        return self.available
            
            

    def rent_car(self):
        if self.available:
            self.available = False
            return True
        else:
            print("Car is not available")

    def return_car(self):
        self.available = True  

class Customer:
    def __init__(self, name, dob, phone):
        self.name = name
        self.dob = dob
        self.phone = phone
        self.rented_cars = []
        self.rental_records = []
    
    def rent_car(self, car, start_date, end_date):
        if car.rent_car():
            self.rented_cars.append(car)
            rental_record = RentalRecord(car, self, start_date, end_date)
            self.rental_records.append(rental_record)
            print(f"Car {car.car_id} rented successfully by {self.name}")
        else:
            print(f"Failed to rent car {car.car_id}, \n sorry {self.name} the car you selected is not available")

    def return_car(self, car, return_date):
        if car in self.rented_cars:
            car.return_car()
            self.rented_cars.remove(car)
            for record in self.rental_records:
                if record.car == car:
                    record.return_record(return_date)
                    print(f"Car {car.car_id} returned successfully by {self.name}")
                    rental_cost = record.calculate_rental_cost()
                    print(f"Rental cost for Car {car.car_id}: ${rental_cost}")
        else:
            print(f"Car {car.car_id} was not rented by {self.name}")

class RentalRecord:
    def __init__(self, car, customer, start_date, end_date):
        self.car = car
        self.customer = customer
        self.start_date = start_date
        self.end_date = end_date
        self.returned = False

    def return_record(self, return_date):
        self.returned = True
        self.return_date = return_date

    def calculate_rental_cost(self):
        if not self.returned:
            raise ValueError(f"Car must be returned by {self.name} to calculate rental cost.")
    
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d")
        return_date = datetime.strptime(self.return_date, "%Y-%m-%d")
        
        rental_duration = (return_date - start_date).days

        total_rental_cost = rental_duration * self.car.rental_price
        return total_rental_cost
              
    
class CarRentalSystem:
    def __init__(self):
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def display_available_cars(self):
        for index, car in enumerate(self.cars, start=1):
            if car.is_available():
                print(f"Car {index} - Car ID: {car.car_id}, Make: {car.make}, Model: {car.model}, Year: {car.year}, Rental Price: ${car.rental_price} per day \n")

car1 = Car("C001", "Toyota", "Camry", 2019, 150)
car2 = Car("C002", "Honda", "Civic", 2020, 150)
car3 = Car("C003", "Ford", "Mustang", 2022, 350)
car4 = Car("C004", "Chevrolet", "Camaro", 2021, 220)

car_rental_system = CarRentalSystem()
car_rental_system.add_car(car1)
car_rental_system.add_car(car2)
car_rental_system.add_car(car3)
car_rental_system.add_car(car4)



def create_customer():
    name = input("Enter your name: ")
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    phone = input("Enter your phone number: ")
    return Customer(name, dob, phone)

def display_Menu():
    print("Car Rental System Menu: ")
    print()
    print("1: Display available cars")
    print()
    print("2: Rent a car")
    print()
    print("3: Return a car")
    print()
    print("4: Exit")
    


while True:
    display_Menu()
    print()
    choice = input("Enter your choice: \n")
    print()

    if choice == '1':
        print("Available Cars: ")
        print()
        car_rental_system.display_available_cars()
    elif choice == '2':
        if 'customer' not in locals():
            print("Please Enter your Details:")
            customer = create_customer()
        else:
            use_existing_customer = input("Do you want to use your existing details? (yes/no) ").lower()
            if use_existing_customer == 'yes':
                print(f"Welcome back, {customer.name}")
                print(f"DOB: {customer.dob} \n Phone Number: {customer.phone} ")
            else: 
                customer = create_customer()

        print(f"Welcome, {customer.name}")
        car_id = input("Enter the Car Id you want to rent ").strip().capitalize()
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        car_to_rent = next((car for car in car_rental_system.cars if car.car_id == car_id), None)
        if car_to_rent: 
            customer.rent_car(car_to_rent, start_date, end_date)
        else:
            print( "Car not found, enter a valid car_id. \n Press 1 to see available cars ")
    elif choice == '3':
        if 'customer' not in locals():
            print("Please create a customer first ")
        else:
            car_id = input("Enter the Car Id you want to rent ")
            return_date = input("Enter the return date (YYYY-MM-DD): ")
            car_to_return =next((car for car in car_rental_system.cars if car.car_id == car_id), None)
            if car_to_return:
                customer.return_car(car_to_return, return_date)
            else:
                print("Car Not Found ")
    elif choice == '4':
        print("Exiting the system. Thank you!")
        break
    else:
        print("Invalid choice. Please try again")