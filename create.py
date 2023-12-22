import pymysql

db = pymysql.connect(
    host='insurance-database.cdcuzzna0mo5.us-east-2.rds.amazonaws.com',
    user='admin',
    password='12345678',
    port = 3306,
    database="insdb"
)
cur = db.cursor()
create_order = """
CREATE TABLE Customer_Relation
( 
    Fname              varchar(18),
    Lname              varchar(18),
    Mname              varchar(18),
    Age                int,
    Gender             TINYINT(1),
    CRelation          varchar(18),
    CSsn               varchar(18)  NOT NULL,
    PRIMARY KEY (CSsn),
    FOREIGN KEY (CSsn) REFERENCES Customer(Ssn)
);
"""
cur.execute(create_order)
results = cur.fetchall()
print(results)
db.commit()
cur.close()
db.close()
