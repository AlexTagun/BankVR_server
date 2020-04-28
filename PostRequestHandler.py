import json
import time
from DataBase import DataBase
import TelegramBot as telegram


class PostRequestHandler:
    def __init__(self, db):
        self.db = db
        self.last_bot_message = ""
        self.handler = {
            "/register": self.register,
            "/login": self.login,
            "/create/card": self.create_card,
            "/get/profile": self.get_profile,
            "/get/apartments": self.get_apartments,
            "/send/message": self.send_message,
            "/get/message": self.get_message,
            "/check/message": self.check_message
        }

    def uuid_create(self, data):
        return "{\"requestTime\": 123, \"code\": 0, \"msg\": \"message\", \"payload\": \"payload_string\"}"

    def register(self, data):
        data = json.loads(data)
        login = data["login"]
        password = data["payload"]["pass"]
        language = data["payload"]["lang"]
        user_platform = data["payload"]["platform"]
        user_device_info = data["payload"]["deviceInfo"]

        print(type(data))
        db_msg = self.db.create_user(login, password, language, user_platform, user_device_info)

        current_time = time.time()
        code = "0"
        msg = ""

        if db_msg.startswith('UNIQUE constraint failed'):
            code = "31"
            msg = db_msg

        response = "{\"requestTime\": " + str(current_time) + ", \"code\": " + code + ", \"msg\": \"" + msg + "\"}"
        print(response)

        return response

    def login(self, data):
        data = json.loads(data)
        print(data)
        login = data["login"]
        password = data["payload"]["pass"]
        print(password + '=====')

        current_time = time.time()
        db_msg = self.db.is_user_registered(login, password)
        code = "0"
        msg = ""

        if db_msg != '[(\'' + login + '\',)]':
            code = "16"
            msg = db_msg

        response = '{"requestTime": ' + str(current_time) + ', "code": ' + code + ', "msg": "' + msg + '", ' \
                                                                                                       '"payload": { "token": "token_data"}}'
        print(response)

        return response

    def create_card(self, data):
        data = json.loads(data)
        login = data["login"]

        current_time = time.time()
        db_msg = self.db.create_card(login)
        code = "0"
        msg = ""

        if db_msg != '0':
            code = "16"
            # msg = db_msg

        response = '{"requestTime": ' + str(current_time) + ', "code": ' + code + ', "msg": "' + msg + '"}'
        return response

    def get_profile(self, data):
        data = json.loads(data)
        login = data["login"]

        current_time = time.time()
        db_msg = self.db.get_cards(login)

        code = "0"
        msg = ""

        if not db_msg:
            code = "16"
            # msg = db_msg
            response = '{"requestTime": ' + str(current_time) + ', "code": ' + code + ', "msg": "' + msg + '"}'
            return response

        cards_str = '['
        for card in db_msg:
            # print(card)
            card_str = '{"Number": "' + card[0] + '", "PaumentSystemName": "' + card[1] + '", "PaumentSystemIcon": "' \
                                                                                          '' + card[
                           2] + '", "Balance": ' + str(card[3]) + ', "CurrencySymbol": "' + card[4] + '", ' \
                                                                                                      '"HasWireless": "' + \
                       card[5] + '"},'
            cards_str += card_str
        cards_str = cards_str[:-1]
        cards_str += ']'

        response = '{"UserLogin": "' + login + '", "Cards": ' + cards_str + '}'
        # print(response)
        return response

    def get_apartments(self, data):

        complexes = self.db.get_complexes()
        complexes_str = '['
        for comlex in complexes:
            print(comlex)
            flat_ids = self.db.get_flats_ids(comlex[0])
            flats_str = '['
            for flat_id in flat_ids:
                flat = self.db.get_flat(flat_id[0])
                flat = flat[0]
                print(str(flat[5]))
                flat_str = '{' \
                           '"Id": ' + str(flat[0]) + ', ' \
                           '"AddressableName": "' + flat[1] + '", ' \
                           '"Name": "' + flat[2] + '", ' \
                           '"RoomNumber": ' + str(flat[3]) + ', ' \
                           '"Space": ' + str(flat[4]) + ', ' \
                           '"Price": ' + str(flat[5]) + ' },'
                flats_str += flat_str
            flats_str = flats_str[:-1]
            flats_str += ']'

            complexes_str += '{' \
                             '"Id": ' + str(comlex[0]) + ', ' \
                             '"AddressableName": "' + comlex[1] + '", ' \
                             '"Name": "' + comlex[2] + '", ' \
                             '"Address": "' + comlex[3] + '", ' \
                             '"MetroData": "' + comlex[4] + '", ' \
                             '"CheckInDate": "' + comlex[5] + '", ' \
                             '"Flats": ' + flats_str + ' },'
        complexes_str = complexes_str[:-1]
        complexes_str += ']'

        response = '{"ComplexesData": ' + complexes_str + '}'
        print(response)
        return response

    def send_message(self, data):
        data = json.loads(data)
        text = data["payload"]["text"]
        telegram.reply_user(text)
        current_time = time.time()
        code = "0"
        msg = ""
        response = '{"requestTime": ' + str(current_time) + ', "code": ' + code + ', "msg": "' + msg + '"}'
        return response
    
    def get_message(self, data):
        # data = json.loads(data)
        text = str(data)
        print(text)
        self.last_bot_message = text
        current_time = time.time()
        code = "0"
        msg = ""
        response = '{"requestTime": ' + str(current_time) + ', "code": ' + code + ', "msg": "' + msg + '"}'
        return response
    
    def check_message(self, data):

        current_time = time.time()
        code = "0"
        msg = ""
        response = '{"requestTime": ' + str(current_time) + ', "code": ' + code + ', "msg": "' + msg + '", ' \
                                                                                                   '"payload": "' + self.last_bot_message + '"}'
        self.last_bot_message = ""
        return response
        
