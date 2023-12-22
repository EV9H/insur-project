from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pymysql
import joblib


def train_reg():
    # Connect to database
    db = pymysql.connect(
        host='insurance-database.cdcuzzna0mo5.us-east-2.rds.amazonaws.com',
        user='admin',
        password='12345678',
        port=3306,
        database="insdb"
    )

    # Query for parameters
    query = """
    SELECT Age, Gender, Income, Health_rating, Married, C.Status FROM Contract C
    INNER JOIN Account_owner ON Account_owner.AccID = C.AccID
    INNER JOIN Customer ON Customer.Ssn = Account_owner.Ssn
    """
    with db.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    # process data
    age = [row[0] for row in results]
    gender = [row[1] for row in results]
    gender = [int(x) for x in gender]
    income = [row[2] for row in results]
    health_rating = [row[3] for row in results]
    married = [row[4] for row in results]
    status = [row[5] for row in results]
    data = list(zip(age, gender, income, health_rating, married))

    # 80% training set/ 20% testing set
    data_train, data_test, type_train, type_test = train_test_split(data, status, test_size=0.2)

    # Create model
    model = LogisticRegression()
    model.fit(data_train, type_train)

    # Save model
    joblib.dump(model, 'regression.joblib')
    cursor.close()
    db.close()

# Test model
# model = joblib.load('regression.joblib')
# probabilities = model.predict_proba(data_test)[:, 1]
# rounded_probabilities = [round(prob, 3) for prob in probabilities]
# print(rounded_probabilities)


def get_reg():
    reg = joblib.load('regression.joblib')
    return reg
