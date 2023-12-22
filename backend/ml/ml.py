from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pymysql
import joblib


def train_knn():
    # Connect to database
    db = pymysql.connect(
        host='insurance-database.cdcuzzna0mo5.us-east-2.rds.amazonaws.com',
        user='admin',
        password='12345678',
        port=3306,
        database="insdb"
    )

    # Query for parameters
    query = "SELECT Age, Gender, Income, Health_rating, Married, Purchased FROM Customer"
    with db.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    age = [row[0] for row in results]
    gender = [row[1] for row in results]
    gender = [int(x) for x in gender]
    income = [row[2] for row in results]
    health_rating = [row[3] for row in results]
    married = [row[4] for row in results]
    purchased = [row[5] for row in results]
    data = list(zip(age, gender, income, health_rating, married))

    # 80% training set/ 20% testing set
    data_train, data_test, type_train, type_test = train_test_split(data, purchased, test_size=0.2)
    k = 10

    # Create model
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(data_train, type_train)

    # Save model
    joblib.dump(knn, 'knn.joblib')
    cursor.close()
    db.close()

# Test model
# knn = joblib.load('knn.joblib')
# prediction = knn.predict(data_test)
# print(confusion_matrix(type_test, prediction))
# print(classification_report(type_test, prediction))


def get_knn():
    knn1 = joblib.load('knn.joblib')
    return knn1
