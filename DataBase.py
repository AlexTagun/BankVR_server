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
        self.cursor.execute('SELECT * FROM "main"."Users"')
        result = self.cursor.fetchall()
        print(result)

    def create_user(self, login, password, language, user_platform, user_device_info):
        query = 'INSERT INTO "main"."Users"' \
                '("user_id", "user_login", "user_password", "user_language", "user_platform", "user_device_info")' \
                'VALUES (1, \'' + login + '\', \'' + password + '\', \'' + language + '\', \'' + user_platform + '\',' \
                ' \'' + user_device_info + '\');'
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            return str(e)
        return "0"

    def is_user_registered(self, login, password):
        print(password + '=====')
        query = 'SELECT user_login FROM "Users" where ' \
                'user_login = \'' + login + '\' and user_password = \'' + password + '\''

        print(query)

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            print(result)
            return str(result)
        except Exception as e:
            return str(e)
