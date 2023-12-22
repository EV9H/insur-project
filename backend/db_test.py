import pymysql
import csv, os
import random

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
    f = csv.reader(open('C:/Users/EvanH/OneDrive/Documents/GitHub/insur-project/backend/util/csv/Customer.csv'))
    next(f)
    q = """INSERT INTO Customer(fname, lname, mname, age, ssn, gender, active, suffix, income, health_rating, married,purchased) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    for line in f:
        line = [None if cell == '' else cell for cell in line]
        cursor.execute(q, line)
       
def InsertAll_Account():
    f = csv.reader(open('C:/Users/EvanH/OneDrive/Documents/GitHub/insur-project/backend/util/csv/Account.csv'))
    next(f)
    q = """INSERT INTO Account(AccID, Password, Email, TaxID, GroupNum, AccCity, Active, AccCompany, AccName) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    for line in f:
        line = [None if cell == '' else cell for cell in line]
        cursor.execute(q, line)
        
def insert_Account():
    q = """
        INSERT INTO Account(AccID, Password, AccName) VALUES(test, 12345,testUser) 
    
    """
    cursor.execute(q)
    
def connect_account_customer():
    amount = 100
    cursor.execute('''SELECT * FROM Customer''' )
    customers = cursor.fetchall()
    
    cursor.execute('''SELECT * FROM Account''' )
    accounts = cursor.fetchall()
    
    for i in range(amount):
        ssn = customers[i][4]
        accid = accounts[i][0]
        custfname = customers[i][0]
        custlname = customers[i][1]
        
        cursor.execute(""" INSERT INTO Account_owner(Ssn, AccID, CustFname, CustLname) VALUES(%s,%s, %s, %s)""", [ssn,accid,custfname,custlname])
    
# InsertAll_Customer()
# InsertAll_Account()

# connect_account_customer()
def addBenefitType():
    benefitType = "A"
    benefitPercentage = "100%"
    DurationOfPayment = '1y' 
    
    cursor.execute('''INSERT INTO BenefitType(BenefitType,BenefitPercentage,DurationOfPayment) VALUES(%s,%s,%s)''', [benefitType,benefitPercentage,DurationOfPayment] )

    benefitType = "B"
    benefitPercentage = "150%"
    DurationOfPayment = '2y' 
    
    cursor.execute('''INSERT INTO BenefitType(BenefitType,BenefitPercentage,DurationOfPayment) VALUES(%s,%s,%s)''', [benefitType,benefitPercentage,DurationOfPayment] )

    benefitType = "C"
    benefitPercentage = "200%"
    DurationOfPayment = '3y' 
    
    cursor.execute('''INSERT INTO BenefitType(BenefitType,BenefitPercentage,DurationOfPayment) VALUES(%s,%s,%s)''', [benefitType,benefitPercentage,DurationOfPayment] )

def addPremiumType():
    ptype = "A"
    pinterval = "1m"
    price = '100' 
    
    cursor.execute('''INSERT INTO PremiumType(PremiumType,PaymentInterval, Price) VALUES(%s,%s,%s)''', [ptype,pinterval,price] )

    ptype = "B"
    pinterval = "1m"
    price = '150' 
    
    cursor.execute('''INSERT INTO PremiumType(PremiumType,PaymentInterval, Price) VALUES(%s,%s,%s)''', [ptype,pinterval,price] )

    ptype = "C"
    pinterval = "1m"
    price = '300' 
    
    cursor.execute('''INSERT INTO PremiumType(PremiumType,PaymentInterval, Price) VALUES(%s,%s,%s)''', [ptype,pinterval,price] )

def addPlan():
    chars = ['A','B','C']
    for ch in chars:
        Plan_Name = "Plan "+ch
        PremiumType = ch
        BenefitType = ch
        cursor.execute('''INSERT INTO Plan(Plan_Name, PremiumType,BenefitType) VALUES(%s,%s,%s)''', [Plan_Name,PremiumType,BenefitType])
def add_region_manager_assoc_lic():
    regionID = [1,2,3]
    regions = ['New York', 'California', 'Shanghai']
    for _ in range(3):
        cursor.execute('''INSERT INTO Region(Region_Id, Region_Name) VALUES(%s,%s)''', [regionID[_], regions[_]])
    cursor.execute(""" SELECT * FROM Region""")
    
    
    license = [ i for i in range(0,10)]
    for _ in range(len(license)):
        cursor.execute("""INSERT INTO License(Lic_id) VALUES(%s)""", [license[_]])
    
    manager = ['987-65-4321']
    cursor.execute("""INSERT INTO Manager(Manager_Ssn, Region_Id) VALUES(%s,%s)""", [manager[0],1])
    print(cursor.fetchall())
    assoc_ssn = [ str(i) * 3 + '-' + str(i)*2 + '-' + str(i)*4 for i in range(10) ]
    for _ in range(len(assoc_ssn)):
        cursor.execute('''INSERT INTO Associate(Assc_Ssn, Manager_Ssn, Lic_id, Region_Id) VALUES(%s,%s,%s,%s)''', [assoc_ssn[_], manager[0], license[_], regionID[_%3]])
        
    cursor.execute("""SELECT * FROM Associate""")
    print(cursor.fetchall())
def add_contract():
    cursor.execute(""" SELECT Account.AccID, Age, Health_rating, Income, Married, Purchased FROM Account
                        INNER JOIN Account_owner ao ON ao.AccID = Account.AccID
                        INNER JOIN Customer c ON c.Ssn = ao.Ssn
    """)
    
    
    table = cursor.fetchall()
    # print(table)
    
    accid  = [_[0] for _ in table]
    age = [_[1] for _ in table]
    hr = [_[2] for _ in table]
    income = [_[3] for _ in table]
    married = [_[4] for _ in table]
    purchased = [_[5] for _ in table]
    cnt = 0
    for i in range(len(accid)):
        _age = age[i] / 50 
        _hr = 50 / hr[i] 
        _income = 80000 / income[i]
        _married = 0.8 if married[i] == '1' else 0.4
        _purchased = 0.8 if purchased[i] == '1' else 0.4
        
        coefficient = _age * _hr * _income * _married * _purchased 
        # print(_age, _hr, _income,_married, _purchased, "=", _age * _hr * _income * _married * _purchased)
        
        for j in range(random.randint(1,3)):
            amount = random.randint(100,1000)
            cid = cnt 
            assoc = f'{str(i%10)*3}-{str(i%10)*2}-{str(i%10)*4}' 
            planname = random.choice(['Plan A', 'Plan B', 'Plan C'])
            acc = accid[i]
            
            status = '1' if coefficient * float(random.choice(['1','0.75', '1.25'])) > 0.5 else '0' 
            cursor.execute("""INSERT INTO Contract(Amount, CID, AccID, Plan_Name, Assc_Ssn,Status) VALUES(%s,%s,%s,%s,%s,%s)""", [amount, cid, acc,planname,assoc,status])    
            cnt += 1
        
        
        
    
    


    
    
# addPlan()
# addBenefitType()
# addPremiumType()
# add_region_manager_assoc_lic()````
# add_contract()
# ------------------------
# add_contract()
# cursor.execute("""DELETE FROM Contract""")
# cursor.execute("""SELECT CID, Status FROM Contract WHERE Status = 1 """)

# q = """
#     SELECT age, gender, income, health_rating, married, C.Status FROM Contract C
#     INNER JOIN Account_owner ON Account_owner.AccID = C.AccID
#     INNER JOIN Customer ON Customer.Ssn = Account_owner.Ssn 
# """
# cursor.execute(q)
# print(cursor.fetchall())


# cursor.execute("SELECT * FROM Plan")
# print(cursor.fetchall())
# q = '''SELECT * FROM Account_owner ao

#         INNER JOIN Account a ON ao.AccID = a.AccID
#         INNER JOIN Customer c ON c.Ssn = ao.Ssn
#     '''
# cursor.execute(q)
# results = cursor.fetchall()
# print(results)

q = '''
    SELECT AccID FROM Contract
'''

q = '''SELECT CID, Plan_Name, Status, Amount, Assc_Ssn FROM Contract 
            INNER JOIN Account ON Account.AccID = Contract.AccID
            WHERE Contract.AccID = 132059
        '''
        
        
q =  '''SELECT * FROM Customer C
        INNER JOIN Account_owner AO ON AO.Ssn = C.Ssn
        WHERE AO.AccID = %s
'''

# q = """
#     UPDATE Customer 
#     SET Age = 123
#     WHERE Customer.Ssn = (
#         SELECT Account_owner.Ssn FROM Account_owner
#         WHERE Account_owner.AccID = %s
#     )

# """


q =  '''SELECT * FROM Contract
        WHERE AccID = %s
'''

# q = """SELECT MAX(CAST(CID AS UNSIGNED))  FROM Contract"""
cursor.execute(q, 'test12345')
print(cursor.fetchall())

db.commit()
cursor.close()
db.close()