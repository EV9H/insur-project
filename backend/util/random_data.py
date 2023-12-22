import random 
import csv, os
from faker import Faker
# from db_query import QuerySender

os.chdir('../backend/util/csv')
faker = Faker()

# def generateRandomData(amount = 1000):
#     data = [['ssn', 'name', 'age', 'gender', 'income', 'health_rating', 'nChildren', 'married', 'purchased']]
#     ssn_counter = 111111111

#     # wealthy
#     wCnt = 0
#     mCnt = 0
#     pCnt = 0
#     for i in range(0, int(amount * 0.2)): 
#         pFactor = 1.2
#         ssn = faker.ssn()
#         name = faker.name()
#         age = random.randint(20,100)
#         gender = random.choice([0,1])
#         income = round(random.uniform(80000, 200000), 2)
#         health_rating = random.randint(1,100)
#         nChildren = random.randint(0,3)
#         married = random.choice([1,0])
#         purchased = 1 if pFactor * (age/50) * (income/140000) * (80 / health_rating) > 1.5 else 0
#         if purchased: 
#             wCnt += 1
#         data.append([ssn,name,age,gender,income,health_rating,nChildren,married,purchased])
#     print("WEALTHY PURCHASED: ", wCnt, "probability = ", round( wCnt / (amount * 0.2),2) )
#     # mid
#     for i in range(0, int(amount * 0.4)): 
#         pFactor = 0.8
#         ssn = faker.ssn()
#         name = faker.name()
#         age = random.randint(20,100)
#         gender = random.choice([0,1])
#         income = round(random.uniform(40000, 80000), 2)
#         health_rating = random.randint(1,100)
#         nChildren = random.randint(0,3)
#         married = random.choice([1,0])
#         purchased = 1 if pFactor * (age/50) * (income/60000) * (80 / health_rating) > 1.5 else 0
#         if purchased: 
#             mCnt += 1
#         data.append([ssn,name,age,gender,income,health_rating,nChildren,married,purchased])
#     print("MID PURCHASED: ", mCnt, "probability = ", round( mCnt / (amount * 0.4),2) )
    
#     # poor
#     for i in range(0, int(amount * 0.4)): 
#         pFactor = 0.4
#         ssn = faker.ssn()
#         name = faker.name()
#         age = random.randint(20,100)
#         gender = random.choice([0,1])
#         income = round(random.uniform(20000, 40000), 2)
#         health_rating = random.randint(1,100)
#         nChildren = random.randint(0,3)
#         married = random.choice([1,0])
#         purchased = 1 if pFactor * (age/50) * (income/30000) * (80 / health_rating) > 1.5 else 0
#         if purchased: 
#             pCnt += 1
#         data.append([ssn,name,age,gender,income,health_rating,nChildren,married,purchased])
#     print("poor PURCHASED: ", pCnt, "probability = ", round( pCnt / (amount * 0.4),2) )
    


    
        

def w(filename,data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
        
def fill_customer():
    data = [['Fname', 'Lname', 'Mname', 'Age', 'Ssn', 'Gender', 'Active', 'Suffix', 'Income', 'Health_rating', 'Married', 'Purchased']]
    
    amount = 100
    
    # wealthy
    wCnt = 0
    mCnt = 0
    pCnt = 0
    pFactor = 1.2
    for i in range(0, int(amount * 0.2)): 
        name = faker.name().split(' ')
        
        fname = name[0]
        lname = name[1]
        mname = ''
        age = random.randint(20,100)
        ssn = faker.ssn()
        gender = random.choice([0,1])
        active = random.choice([0,1])
        suffix = ''
        income = round(random.uniform(80000, 200000), 2)
        
        health_rating = random.randint(1,100)
        married = random.choice([1,0])
        purchased = 1 if pFactor * (age/50) * (income/140000) * (80 / health_rating) > 1.5 else 0
        if purchased: 
            wCnt += 1
        data.append([fname, lname, mname, age, ssn, gender, active, suffix, income, health_rating, married,purchased])
    print("WEALTHY PURCHASED: ", wCnt, "probability = ", round( wCnt / (amount * 0.2),2) )
    # mid
    for i in range(0, int(amount * 0.4)): 
        pFactor = 0.8
        name = faker.name().split(' ')
        
        fname = name[0]
        lname = name[1]
        mname = ''
        age = random.randint(20,100)
        ssn = faker.ssn()
        gender = random.choice([0,1])
        active = random.choice([0,1])
        suffix = ''
        income = round(random.uniform(40000, 80000), 2)
        health_rating = random.randint(1,100)
        married = random.choice([1,0])
        purchased = 1 if pFactor * (age/50) * (income/60000) * (80 / health_rating) > 1.5 else 0
        if purchased: 
            mCnt += 1
        data.append([fname, lname, mname, age, ssn, gender, active, suffix, income, health_rating, married,purchased])
    print("MID PURCHASED: ", mCnt, "probability = ", round( mCnt / (amount * 0.4),2) )
    
    # poor
    for i in range(0, int(amount * 0.4)): 
        pFactor = 0.4
        name = faker.name().split(' ')
        
        fname = name[0]
        lname = name[1]
        mname = ''
        age = random.randint(20,100)
        ssn = faker.ssn()
        gender = random.choice([0,1])
        active = random.choice([0,1])
        suffix = ''
        income = round(random.uniform(20000, 40000), 2)
        health_rating = random.randint(1,100)
        married = random.choice([1,0])
        purchased = 1 if pFactor * (age/50) * (income/30000) * (80 / health_rating) > 1.5 else 0
        if purchased: 
            pCnt += 1
        data.append([fname, lname, mname, age, ssn, gender, active, suffix, income, health_rating, married,purchased])
    print("poor PURCHASED: ", pCnt, "probability = ", round( pCnt / (amount * 0.4),2) )
    

    w("Customer.csv", data)
    

def fill_account():
    faker2 = Faker()
    data = [['AccID', 'Password', 'Email', 'TaxID', 'GroupNum', 'AccCity', 'Active', 'AccCompany', 'AccName']]
    
    amount = 100
    
    for _ in range(amount):
        accid = str(faker2.unique.random_int(min=111111, max=999999))
        password = str('12345')
        email = faker2.email()
        taxid = ''
        groupnum = ''
        acccity = faker.city()
        active = 1
        acccompany = ''
        accname = ''
        data.append([accid, password,email,taxid,groupnum,acccity,active,acccompany,accname])
    w("Account.csv", data)
    
    
    
    
    
    
    
    
    
    
    
######## CALL AREA #############

# fill_customer()
fill_account()
