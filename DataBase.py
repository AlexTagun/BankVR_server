import sqlite3
import random


class DataBase:
    connection = None
    cursor = None

    def __init__(self):
        # self.conn = sqlite3.connect('C:\\Users\\aleks\\Documents\\BankVR_server\\DataBase\\BankVR.db')
        self.conn = sqlite3.connect('/root/BankVR_server/DataBase/BankVR.db')
        self.cursor = self.conn.cursor()

    def Close(self):
        self.conn.close()

    def ExecuteQuery(self):
        self.cursor.execute('SELECT * FROM "main"."Users"')
        result = self.cursor.fetchall()
        print(result)

    def create_user(self, login, password, language, user_platform, user_device_info):
        self.cursor.execute('SELECT user_id FROM "main"."Users"')
        result = self.cursor.fetchall()
        id = result[-1][0] + 1
        print(id)
        query = 'INSERT INTO "main"."Users"' \
                '("user_id", "user_login", "user_password", "user_language", "user_platform", "user_device_info")' \
                'VALUES (' + str(
            id) + ', \'' + login + '\', \'' + password + '\', \'' + language + '\', \'' + user_platform + '\',' \
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

    def create_card(self, login):

        card_number = str(random.randint(1000, 9999)) + " " + str(random.randint(1000, 9999)) + " " + str(
            random.randint(1000, 9999)) + " " + str(random.randint(1000, 9999))
        card_payment_system_id = str(random.randint(1, 3))
        card_balance = "0.0"
        card_currency_id = str(random.randint(1, 3))
        card_has_wireless_payment = "true"
        if random.randrange(2) == 1:
            card_has_wireless_payment = "false"

        query = 'INSERT INTO "main"."Cards"' \
                '("card_number", "card_payment_system_id", "card_balance", "card_currency_id", "card_has_wireless_payment", "card_user_login")' \
                'VALUES (\'' + card_number + '\', ' + card_payment_system_id + ', ' + card_balance + ', ' + card_currency_id + ', \'' + card_has_wireless_payment + '\', \'' + login + '\');'
        print(query)
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            return str(e)
        return "0"

    def get_cards(self, login):
        query = 'SELECT card_number, payment_system_name, payment_system_icon, card_balance, ' \
                'currency_symbol, card_has_wireless_payment ' \
                'FROM "Cards", "Payment_systems", "Currencies" where ' \
                'payment_system_id = card_payment_system_id ' \
                'and card_currency_id = currency_id ' \
                'and card_user_login = \'' + login + '\''

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            return str(e)

    def get_complexes(self):
        query = 'SELECT * ' \
                'FROM "Complexes"'

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            return str(e)

    def get_flats_ids(self, complex_id):
        query = 'SELECT flat_id ' \
                'FROM "Complex_Flats" where complex_id = ' + str(complex_id)

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            return str(e)

    def get_flat(self, flat_id):
        query = 'SELECT * ' \
                'FROM "Flats" where flat_id = ' + str(flat_id)

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            return str(e)
