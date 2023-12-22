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
    
    def excute(self,query, show_result = False, auto_close = True):
        self.cursor.excute(query)
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


