import sqlite3


class DataBase:
    connection = None
    cursor = None

    def __init__(self):
        self.conn = sqlite3.connect('C:\\Users\\aleks\\Documents\\BankVR_server\\DataBase\\BankVR.db')
        self.cursor = self.conn.cursor()

    def Close(self):
        self.conn.close()
        
    def ExecuteQuery(self):
        self.cursor.execute("SELECT * FROM Client")
        result = self.cursor.fetchall()
        print(result)
