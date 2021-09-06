"""Create the database, inventory.db, used in the 
Database Manager GUI

Building Custom UIs with PyQt with Packt Publishing
Chapter 4 - Handling Data with PyQt
Created by: Joshua Willman
"""

import sys, random, string, datetime, csv, os
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def create_database_objects():
    """First, check if files exist.
    Second, create QSqlDatabase object and create a connection to the database.
    Third, create SQL tables."""
    # Check for data folder and data files
    path = "data"
    if os.path.exists(path):  
        # If it exists, check for the following files
        files = ["addresses.txt",
                 "first.txt",
                 "phones.txt",
                 "products.csv",
                 "surnames.txt"]
        file_list = os.listdir(path)
        missing = [name for name in files if name not in file_list]
        if missing != []:
            print(f"[INFO] Files missing: {missing}")
            sys.exit(1)
        else:
            print("[INFO] All files found. Proceeding to create database...")
    else:
        print(f"[INFO] Directory name '{path}' not found.")

    # Create connection to the database
    database = QSqlDatabase.addDatabase("QSQLITE") # SQLite 3
    database.setDatabaseName("data/inventory.db")

    if not database.open():
        print("Unable to open data source file.")
        print("Connection failed: ", 
              database.lastError().text())
        sys.exit(1) # Error code 1 - signifies error in opening file

    query = QSqlQuery() # Create query instance

    # Erase tables if they already exist (avoiding duplicates)
    query.exec("DROP TABLE IF EXISTS Staff")
    query.exec("DROP TABLE IF EXISTS Customers")
    query.exec("DROP TABLE IF EXISTS Orders")
    query.exec("DROP TABLE IF EXISTS Products")
    query.exec("DROP TABLE IF EXISTS Categories")

    query.exec("PRAGMA foreign_keys = ON")

    print("[INFO] Connected to database. Creating tables...")

    # Create Staff table
    query.exec("""CREATE TABLE Staff (
        staff_id VARCHAR PRIMARY KEY UNIQUE NOT NULL,
        username TEXT NOT NULL,
        password BLOB NOT NULL,
        is_admin BOOLEAN NOT NULL)""")

    # Create Customers table
    query.exec("""CREATE TABLE Customers (
        customer_id VARCHAR PRIMARY KEY UNIQUE NOT NULL,
        first_name VARCHAR (40) NOT NULL,
        last_name VARCHAR (40) NOT NULL,
        address VARCHAR (100) NOT NULL,
        phone VARCHAR (20),
        email VARCHAR (50) NOT NULL,
        staff_id VARCHAR REFERENCES Staff (staff_id) ON DELETE CASCADE ON UPDATE CASCADE)""") 

    # Create Categories table
    query.exec("""CREATE TABLE Categories (
        category_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        category_name VARCHAR (40) NOT NULL, 
        category_description VARCHAR (100))""") 

    # Create Products table
    query.exec("""CREATE TABLE Products (
        product_id VARCHAR PRIMARY KEY UNIQUE NOT NULL,
        product_name VARCHAR (100) NOT NULL,
        product_description VARCHAR (240),
        product_price REAL,
        category_id INTEGER REFERENCES Categories (category_id) ON DELETE CASCADE ON UPDATE CASCADE)""")
    
    # Create Orders table
    # NOTE: Store date_of_order as YYYY-MM-DD 
    query.exec("""CREATE TABLE Orders (
        order_id VARCHAR PRIMARY KEY UNIQUE NOT NULL,
        date_of_order DATE NOT NULL,
        order_status VARCHAR(40) NOT NULL,
        unit_price REAL, 
        quantity INT (10),
        discount REAL,
        total REAL,
        product_id VARCHAR REFERENCES Products (product_id) ON DELETE CASCADE ON UPDATE CASCADE,
        customer_id VARCHAR REFERENCES Customers (customer_id) ON DELETE CASCADE ON UPDATE CASCADE)""") 

    print("[INFO] Tables created.")

def random_dates(times):
    """Create random dates.
    Returns a list of random dates."""
    format = "%Y-%m-%d"
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date.today()
    time_between_dates = end_date - start_date
    return [(random.random() * time_between_dates + start_date).strftime(format) for i in range(times)]    

def insert_data_into_tables():
    """Create the mock data items and populate the tables."""
    # Set the number of users and orders in the database
    number_of_users = 2500
    number_of_orders = 10000

    print("[INFO] Getting ready to insert data into the tables...")

    ################################### Staff #####################################
    # Create the users and admin accounts that are able to access the database

    # users[i][4] values represent boolean values, True = 1, False = 0
    users = [[None, "admin", "paSSw0rd!", 1], 
             [None, "employee01", "Godz!lla0", 0],
             [None, "employee02", "C0d3r4L!fe", 0]]

    # Create random staff_id
    for user in users:
        id = random.randint(0, 9999)
        user[0] = int(f"{id:04d}")

    ################################# Customers ###################################
    # Create a table of customer information 
    print("[INFO] Creating customer data...")

    # Create customer_id 
    customer_ids = []
    while len(customer_ids) < number_of_users:
        id = random.randint(0, 999999)
        if id not in customer_ids:
            customer_ids.append(int(f"{id:06d}"))

    # Create first_name and last_name data
    with open("data/first.txt", "r") as f:
        first_names = random.choices(list(f), k=number_of_users)
    for i, first in enumerate(first_names):
        new_first = first.strip("\n")
        first_names[i] = new_first

    with open("data/surnames.txt", "r") as f:
        surnames = random.choices(list(f), k=number_of_users)
    for i, sur in enumerate(surnames):
        new_sur = sur.strip("\n")
        surnames[i] = new_sur    

    # Create Address data
    addresses, address = [], ""
    with open("data/addresses.txt") as f:
        for count, line in enumerate(f, start=1):
            if count % 2 == 1:
                address = line.strip(" \n")
            elif count % 2 == 0:
                address = address + ", " + line.strip("\n")
                addresses.append(address)

    # Create Phone data
    phones = []
    with open("data/phones.txt", "r") as f:
        for i, phone in enumerate(f):
            new_phone = phone.strip("\n")
            phones.append(new_phone)

    customer_items = zip(customer_ids, first_names, surnames, addresses, phones) # List of tuples
    customers = []
    # Turn list of tuples into list of lists
    for item in customer_items:
        customers.append(list(item))

    ################################### Orders ####################################
    # Create order items for Orders table
    print("[INFO] Creating orders data...")

    # Create orders_id
    order_ids = []
    while len(order_ids) < number_of_orders:
        id = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if id not in order_ids:
            order_ids.append(id)

    # Create random dates 
    dates = random_dates(number_of_orders)

    # Create status for each order
    status_values = ["Delivered", "Refunded", "Pending", "En Route", "Unfulfillable"]
    statuses = random.choices(population=status_values, 
                                 weights=[0.45, 0.05, 0.10, 0.35, 0.05], 
                                 k=number_of_orders)

    order_items = zip(order_ids, dates, statuses)
    orders = []
    # Turn list of tuples into list of lists
    for item in order_items:
        orders.append(list(item))

    ############################## Products & Categories ###############################
    # Create a table for product and category information
    print("[INFO] Creating addtional data...")

    categories = []
    # Read in all information for the products table
    # NOTE: The products.csv file contains both product and category info
    with open("data/products.csv", "r", newline="") as csv_f:
        reader = csv.reader(csv_f)
        header_labels = next(reader) # Skip headers in csv file
        products = list(reader)

        csv_f.seek(0) # Reset pointer to beginning of file
        csv_f.readline() # Skip the header
        for lines in reader:
            categories.append([lines[2], lines[3]])

    print("[INFO] Data samples created. Populating tables...")

    query = QSqlQuery() # Create new QSqlQuery object

    # Positional binding to insert records into the Staff table
    query.prepare("""INSERT INTO Staff (
                  staff_id, 
                  username, 
                  password, 
                  is_admin) VALUES (?, ?, ?, ?)""")
    # Add values to the query to be inserted into the Staff table
    for i in range(len(users)):
        id = users[i][0]
        username = users[i][1]
        password = users[i][2]
        admin_or_not = users[i][3]
        query.addBindValue(id)
        query.addBindValue(username)
        query.addBindValue(password)
        query.addBindValue(admin_or_not)
        query.exec()

    # Add values to the query to be inserted into the Customers table
    # Collect user_id values
    user_ids = []
    for user in users:
        user_ids.append(user[0]) 

    # Positional binding to insert records into the Customers table
    query.prepare("""INSERT INTO Customers (
                  customer_id, 
                  first_name, 
                  last_name, 
                  address, 
                  phone, 
                  email, 
                  staff_id) VALUES (?, ?, ?, ?, ?, ?, ?)""")
    for i in range(len(customers)):
        id = customers[i][0]
        first = customers[i][1]
        last = customers[i][2]
        address = customers[i][3]
        phone = customers[i][4]
        # Create company Email addresses
        email = last.replace(" ", "") + first.replace(" ", "") + "." + "@company.com" 
        staff = random.choice(user_ids)
        query.addBindValue(id)
        query.addBindValue(first)
        query.addBindValue(last)
        query.addBindValue(address)
        query.addBindValue(phone)
        query.addBindValue(email)
        query.addBindValue(staff)
        query.exec()

    print("[INFO] Staff and Customers tables finished.")

    # Create a set (actually a list in order to keep track of the order) 
    # of all possible categories
    categories_set = []
    for sublist in categories:
        if sublist not in categories_set:
            categories_set.append(sublist)  

    # Positional binding to insert records into the Categories table
    query.prepare("""INSERT INTO Categories (
                  category_name, 
                  category_description) VALUES (?, ?)""")
    # Add values to the query to be inserted into the Categories table
    for category in categories_set:
        name = category[0] 
        description = category[1]
        query.addBindValue(name)
        query.addBindValue(description)
        query.exec()

    # Positional binding to insert records into the Products table
    query.prepare("""INSERT INTO Products (
                  product_id, 
                  product_name, 
                  product_description, 
                  product_price, 
                  category_id) VALUES (?, ?, ?, ?, ?)""")
    # Add values to the query to be inserted into the Products table
    for i in range(len(products)):
        id = products[i][0]
        name = products[i][1]
        description = products[i][5]
        price = float(products[i][4])
        category_id = categories_set.index(categories[i]) + 1
        query.addBindValue(id)
        query.addBindValue(name)
        query.addBindValue(description)
        query.addBindValue(price)
        query.addBindValue(category_id)
        query.exec()     

    # Create a list of all product ids
    product_ids = []
    for product in products:
        product_ids.append(product[0]) 

    print("[INFO] Categories and Products tables finished.")

    # Positional binding to insert records into the Orders table
    query.prepare("""INSERT INTO Orders (
                  order_id, 
                  date_of_order, 
                  order_status, 
                  unit_price, 
                  quantity, 
                  discount, 
                  total,
                  product_id, 
                  customer_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""")
    # Add values to the query to be inserted into the Orders table 
    for i in range(number_of_orders):
        id = orders[i][0]
        order_date = orders[i][1]
        status = orders[i][2]
        price = None # Placeholder value
        quantity = random.randint(1, 4)
        discount = random.choices([0, 10, 25, 50], 
                                 weights=[0.70, 0.15, 0.10, 0.05], 
                                 k=1)
        total = None # Placeholder value
        prod_id = random.choices(product_ids, k=1)
        customer = random.choices(customer_ids, k=1)
        query.addBindValue(id)
        query.addBindValue(order_date)
        query.addBindValue(status)
        query.addBindValue(price)
        query.addBindValue(quantity)
        query.addBindValue(discount[0])
        query.addBindValue(total)
        query.addBindValue(prod_id[0])
        query.addBindValue(customer[0])
        query.exec()

    # Update the Orders.unit_price values using the prices in Products.product_price 
    query.exec("""UPDATE Orders 
                  SET unit_price = (SELECT product_price
                                    FROM Products
                                    WHERE Products.product_id = Orders.product_id)""")

    # Update the total value in Orders
    query.exec("""UPDATE Orders 
                  SET total = (unit_price - (discount / 100) * unit_price) * quantity""")
    query.exec("""UPDATE Orders 
                  SET total = ROUND(total, 2)""")

    print("[INFO] Orders table finished.")
    print("[INFO] Database succeessfully created.")
    sys.exit(0)

if __name__ == "__main__":   
    create_database_objects()
    insert_data_into_tables()
