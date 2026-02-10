import csv
import random
from datetime import datetime, timedelta

# Generate customers.csv
customers = []
for i in range(1, 1001):
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth',
                   'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen',
                   'Christopher', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra',
                   'Donald', 'Ashley', 'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
                   'Kenneth', 'Dorothy', 'Kevin', 'Carol', 'Brian', 'Amanda', 'George', 'Melissa', 'Edward', 'Deborah']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
                  'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
                  'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
                  'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts']
    
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego',
              'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco',
              'Indianapolis', 'Seattle', 'Denver', 'Boston', 'Nashville', 'Detroit', 'Portland', 'Las Vegas', 'Miami']
    
    states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA', 'TX', 'FL', 'TX', 'OH', 'NC', 'CA',
              'IN', 'WA', 'CO', 'MA', 'TN', 'MI', 'OR', 'NV', 'FL']
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    city_index = random.randint(0, len(cities) - 1)
    
    customer = {
        'customer_id': i,
        'first_name': first_name,
        'last_name': last_name,
        'email': f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@email.com",
        'phone': f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
        'address': f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple', 'Cedar', 'Elm', 'Park', 'Washington', 'Lake', 'Hill'])} {random.choice(['St', 'Ave', 'Blvd', 'Dr', 'Ln', 'Rd'])}",
        'city': cities[city_index],
        'state': states[city_index],
        'zip_code': f"{random.randint(10000, 99999)}",
        'registration_date': (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1825))).strftime('%Y-%m-%d')
    }
    customers.append(customer)

# Write customers.csv
with open('customers.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['customer_id', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'registration_date'])
    writer.writeheader()
    writer.writerows(customers)

print("customers.csv created successfully!")

# Generate orders.csv
orders = []
products = [
    ('Laptop', 'Electronics'), ('Smartphone', 'Electronics'), ('Tablet', 'Electronics'), ('Headphones', 'Electronics'),
    ('Smart Watch', 'Electronics'), ('Camera', 'Electronics'), ('TV', 'Electronics'), ('Gaming Console', 'Electronics'),
    ('Office Chair', 'Furniture'), ('Desk', 'Furniture'), ('Bookshelf', 'Furniture'), ('Sofa', 'Furniture'),
    ('Coffee Table', 'Furniture'), ('Bed Frame', 'Furniture'), ('Dining Table', 'Furniture'), ('Wardrobe', 'Furniture'),
    ('Running Shoes', 'Clothing'), ('Jeans', 'Clothing'), ('T-Shirt', 'Clothing'), ('Jacket', 'Clothing'),
    ('Dress', 'Clothing'), ('Sneakers', 'Clothing'), ('Sweater', 'Clothing'), ('Backpack', 'Clothing'),
    ('Blender', 'Home Appliances'), ('Microwave', 'Home Appliances'), ('Coffee Maker', 'Home Appliances'),
    ('Vacuum Cleaner', 'Home Appliances'), ('Air Purifier', 'Home Appliances'), ('Toaster', 'Home Appliances'),
    ('Novel', 'Books'), ('Cookbook', 'Books'), ('Biography', 'Books'), ('Textbook', 'Books'),
    ('Yoga Mat', 'Sports'), ('Dumbbells', 'Sports'), ('Tennis Racket', 'Sports'), ('Basketball', 'Sports')
]

payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay', 'Bank Transfer']
order_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Returned']

for i in range(1, 1001):
    product_name, product_category = random.choice(products)
    quantity = random.randint(1, 5)
    unit_price = round(random.uniform(10.0, 999.99), 2)
    
    order = {
        'order_id': i,
        'customer_id': random.randint(1, 1000),  # Foreign key to customers
        'order_date': (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 425))).strftime('%Y-%m-%d'),
        'product_name': product_name,
        'product_category': product_category,
        'quantity': quantity,
        'unit_price': unit_price,
        'total_amount': round(quantity * unit_price, 2),
        'payment_method': random.choice(payment_methods),
        'order_status': random.choice(order_statuses)
    }
    orders.append(order)

# Write orders.csv
with open('orders.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['order_id', 'customer_id', 'order_date', 'product_name', 'product_category', 'quantity', 'unit_price', 'total_amount', 'payment_method', 'order_status'])
    writer.writeheader()
    writer.writerows(orders)

print("orders.csv created successfully!")
print(f"\nSummary:")
print(f"- customers.csv: {len(customers)} records")
print(f"- orders.csv: {len(orders)} records")
print(f"- Customer IDs range from 1 to {len(customers)}")
print(f"- Orders reference customer IDs via foreign key relationship")