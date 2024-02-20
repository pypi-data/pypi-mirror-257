from .dbase import Database
from .server import HTTPClient

DB_FILE: str = "whitelist.db"
URL: str = "some_url"
HEADERS: dict = {"Content-Type": "application/json"}


class Whitelist:
    def __init__(self, db_file: str = DB_FILE) -> None:
        self.db_file = db_file
        self.http_client = None
        self.database = None

    def initialize(self):
        self.http_client = HTTPClient()
        self.database = Database(self.db_file)
        self.database.connect()
        self.database.create_whitelist_table()

    def get_result(self, message, current_bot) -> bool:
        user_in_db = self.check_conversion(message.from_user.id)
        if user_in_db:
            return True
        else:
            request_data = self.build_request_data(message, current_bot.username)
            response = self.send_request(request_data)
            if response.status_code == 200:
                self.register_conversion(message, current_bot.username)
                self.close_database()
                return True
            else:
                return False

    @staticmethod
    def build_request_data(message, bot_username) -> dict:
        data = {
            "user_uuid": message.get_args(),
            "telegram_bot_username": bot_username,
            "telegram_user_id": message.from_user.id,
            "telegram_user_username": message.from_user.username,
            "telegram_user_fullname": (
                f"{message.from_user.first_name} {message.from_user.last_name}"
                if message.from_user.last_name
                else message.from_user.first_name
            ),
        }
        return data

    def check_conversion(self, user_id: str) -> bool:
        res = self.database.check_user_in_whitelist(user_id)
        return res

    def close_database(self):
        self.database.close()

    def send_request(self, request_body: dict) -> int:
        response = self.http_client.post(URL, request_body, HEADERS)
        self.http_client.close()
        return response

    def register_conversion(self, message, bot_username) -> bool:
        self.database.add_to_whitelist(
            user_id=message.from_user.id,
            uuid=message.get_args(),
            bot=bot_username,
        )
        self.database.close()
        return True
