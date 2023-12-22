import pymysql
import csv 
# Establish a connection to the database
db = pymysql.connect(
    host='insurance-database.cdcuzzna0mo5.us-east-2.rds.amazonaws.com',
    user='admin',
    password='12345678',
    port = 3306,
    database="insdb"
)

# Create a cursor object
cursor = db.cursor()

# CUSTOMER: 
def createTableCustomer():
    cursor.execute('''DROP TABLE IF EXISTS customer''')
    q = """CREATE TABLE customer (
    ssn VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender VARCHAR(255),
    income FLOAT,
    health_rating INT,
    nChildren INT,
    married BOOLEAN,
    purchased BOOLEAN
    );
    """
    cursor.execute(q)
    results = cursor.fetchall()
    print(results)

# createTableCustomer()

# Execute a SQL query
def InsertAll_Customer():
    f = csv.reader(open('example.csv'))
    next(f)
    q = """INSERT INTO customer(ssn,name, age, gender, income, health_rating, nChildren, married,purchased) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    for line in f:
        line = [None if cell == '' else cell for cell in line]
        cursor.execute(q, line)
       

# InsertAll_Customer()
# cursor.execute(q)
print("""FETCHING ------------- \n\n\n""")
q = '''SELECT * FROM customer'''
cursor.execute(q)
results = cursor.fetchall()
print(results)


db.commit()
cursor.close()
db.close()