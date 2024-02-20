from contextlib import contextmanager
from .dbase import Database
from .server import HTTPClient

DB_FILE: str = "whitelist.db"
HEADERS: dict = {"Content-Type": "application/json"}


class Whitelist:
    def __init__(self, url: str, db_file: str = DB_FILE) -> None:
        self.url = url
        self.db_file = db_file
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
            self._database = Database(self.db_file)
            self._database.connect()
            self._database.create_whitelist_table()
        return self._database

    def get_result(self, message, current_bot) -> bool:
        user_in_db = self.check_conversion(message.from_user.id)
        if user_in_db:
            return True
        else:
            request_data = self.build_request_data(message, current_bot.username)
            response = self.send_request(request_data)
            if response.status_code == 200:
                self.register_conversion(message, current_bot.username)
                return True
            else:
                return False

    @staticmethod
    def build_request_data(message, bot_username) -> dict:
        # Тело метода остаётся неизменным
        ...

    def check_conversion(self, user_id: str) -> bool:
        # Используйте контекстный менеджер для управления ресурсами
        with self.manage_database() as db:
            return db.check_user_in_whitelist(user_id)

    @contextmanager
    def manage_database(self):
        db = Database(self.db_file)
        db.connect()
        db.create_whitelist_table()
        yield db
        db.close()

    def send_request(self, request_body: dict) -> int:
        # Обработка исключений и закрытие клиента может быть реализована здесь
        response = self.http_client.post(self.url, request_body, HEADERS)
        return response

    def register_conversion(self, message, bot_username) -> bool:
        # Используйте контекстный менеджер для базы данных
        with self.manage_database() as db:
            db.add_to_whitelist(
                user_id=message.from_user.id,
                uuid=message.get_args(),
                bot=bot_username,
            )
        return True
