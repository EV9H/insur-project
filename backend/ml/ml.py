from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pymysql

db = pymysql.connect(
    host='insurance-database.cdcuzzna0mo5.us-east-2.rds.amazonaws.com',
    user='admin',
    password='12345678',
    port = 3306,
    database="insdb"
)
query = "SELECT age, gender, income, health_rating, nChildren, married, purchased FROM customer"
with db.cursor() as cursor:
    cursor.execute(query)
    results = cursor.fetchall()

age = [row[0] for row in results]
gender = [row[1] for row in results]
income = [row[2] for row in results]
health_rating = [row[3] for row in results]
children = [row[4] for row in results]
married = [row[5] for row in results]
purchased = [row[6] for row in results]

data = list(zip(age, gender, income, health_rating, children, married))
data_train, data_test, type_train, type_test = train_test_split(data, purchased, test_size=0.2, random_state=42)
k = 10
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(data_train, type_train)
prediction = knn.predict(data_test)
print(confusion_matrix(type_test, prediction))
print(classification_report(type_test, prediction))
