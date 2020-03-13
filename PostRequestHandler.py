import json
import time
from DataBase import DataBase


class PostRequestHandler:
    def __init__(self, db):
        self.db = db
        self.handler = {
            "/uuid/create": self.uuid_create,
            "/register": self.register,
            "/login": self.login
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
        return "{\"requestTime\": 123, \"code\": 0, \"msg\": \"message\", \"payload\": {\"token\": \"token_data\"}}"
