from contextlib import contextmanager
from .dbase import Database
from .server import HTTPClient

DB_FILE: str = "whitelist.db"
HEADERS: dict = {"Content-Type": "application/json"}


class Whitelist:
    def __init__(self, verification_service_url: str, database_path: str = DB_FILE) -> None:
        self.verification_service_url = verification_service_url
        self.database_path = database_path
        self._http_client = None
        self._database = None

    @property
    def http_client(self) -> HTTPClient:
        if self._http_client is None:
            self._http_client = HTTPClient()
        return self._http_client

    @property
    def database(self) -> Database:
        if self._database is None:
            self._database = Database(self.database_path)
            self._database.connect()
            self._database.create_whitelist_table()
        return self._database

    def process_user_verification(self, message, current_bot) -> bool:
        user_in_db = self.is_user_whitelisted(message.from_user.id)
        if user_in_db:
            return True
        else:
            request_data = self.build_request_data(message, current_bot.username)
            response = self.send_verification_request(request_data)
            if response.status_code == 200:
                self.add_user_to_whitelist(message, current_bot.username)
                return True
            else:
                return False

    def verify_user_and_register(self, message, current_bot) -> bool:
        if message.get_args():
            request_data = self.create_verification_data(message, current_bot.username)
            response = self.send_verification_request(request_data)
            return response.status_code == 200
        else:
            return False

    @staticmethod
    def create_verification_data(message, bot_username) -> dict:
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

    def is_user_whitelisted(self, user_id: str) -> bool:
        # Используйте контекстный менеджер для управления ресурсами
        with self.database_context() as db:
            return db.check_user_in_whitelist(user_id)

    @contextmanager
    def database_context(self):
        db = Database(self.database_path)
        db.connect()
        db.create_whitelist_table()
        yield db
        db.close()

    def send_verification_request(self, request_body: dict) -> requests.Response:
        # Обработка исключений и закрытие клиента может быть реализована здесь
        response = self.http_client.post(self.verification_service_url, request_body, HEADERS)
        return response

    def add_user_to_whitelist(self, message, bot_username) -> bool:
        # Используйте контекстный менеджер для базы данных
        with self.database_context() as db:
            db.add_to_whitelist(
                user_id=message.from_user.id,
                uuid=message.get_args(),
                bot=bot_username,
            )
        return True
