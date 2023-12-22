import pymysql

class QuerySender:
    def __init__(self): 
        self.db = pymysql.connect(
            host='insurance-database.cdcuzzna0mo5.us-east-2.rds.amazonaws.com',
            user='admin',
            password='12345678',
            port = 3306,
            database="insdb"
        )
        
        self.cursor = self.db.cursor()
    
    def execute(self, query, params=None, show_result=True, auto_close=True):
        self.cursor.execute(query, params)
        if show_result:
            return self.cursor.fetchall()
        
        if auto_close: 
            self.db.commit()
            self.cursor.close()
            self.db.close()  
    
    def close(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()  


