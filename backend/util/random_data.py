import random 
import csv
from faker import Faker

# ssn VARCHAR(255) PRIMARY KEY,
#     name VARCHAR(255),
#     age INT,
#     gender VARCHAR(255),
#     income FLOAT,
#     health_rating INT,
#     nChildren INT,
#     married BOOLEAN

# INSERT INTO customer (ssn, name, age, gender, income, health_rating, nChildren, married) VALUES ('123-45-6789', 'John Doe', 30, 'Male', 50000.0, 80, 2, True);
ssn_counter = 111111111
data = [['ssn', 'name', 'age', 'gender', 'income', 'health_rating', 'nChildren', 'married', 'purchased']]

faker = Faker()

def generateRandomData(amount = 1000):
    
    # wealthy
    wCnt = 0
    mCnt = 0
    pCnt = 0
    for i in range(0, int(amount * 0.2)): 
        pFactor = 1.2
        ssn = faker.ssn()
        name = faker.name()
        age = random.randint(20,100)
        gender = random.choice([0,1])
        income = round(random.uniform(80000, 200000), 2)
        health_rating = random.randint(1,100)
        nChildren = random.randint(0,3)
        married = random.choice([1,0])
        purchased = 1 if pFactor * (age/50) * (income/140000) * (80 / health_rating) > 1.5 else 0
        if purchased: 
            wCnt += 1
        data.append([ssn,name,age,gender,income,health_rating,nChildren,married,purchased])
    print("WEALTHY PURCHASED: ", wCnt, "probability = ", round( wCnt / (amount * 0.2),2) )
    # mid
    for i in range(0, int(amount * 0.4)): 
        pFactor = 0.8
        ssn = faker.ssn()
        name = faker.name()
        age = random.randint(20,100)
        gender = random.choice([0,1])
        income = round(random.uniform(40000, 80000), 2)
        health_rating = random.randint(1,100)
        nChildren = random.randint(0,3)
        married = random.choice([1,0])
        purchased = 1 if pFactor * (age/50) * (income/60000) * (80 / health_rating) > 1.5 else 0
        if purchased: 
            mCnt += 1
        data.append([ssn,name,age,gender,income,health_rating,nChildren,married,purchased])
    print("MID PURCHASED: ", mCnt, "probability = ", round( mCnt / (amount * 0.4),2) )
    
    # poor
    for i in range(0, int(amount * 0.4)): 
        pFactor = 0.4
        ssn = faker.ssn()
        name = faker.name()
        age = random.randint(20,100)
        gender = random.choice([0,1])
        income = round(random.uniform(20000, 40000), 2)
        health_rating = random.randint(1,100)
        nChildren = random.randint(0,3)
        married = random.choice([1,0])
        purchased = 1 if pFactor * (age/50) * (income/30000) * (80 / health_rating) > 1.5 else 0
        if purchased: 
            pCnt += 1
        data.append([ssn,name,age,gender,income,health_rating,nChildren,married,purchased])
    print("poor PURCHASED: ", pCnt, "probability = ", round( pCnt / (amount * 0.4),2) )
    
generateRandomData()

with open('example.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)