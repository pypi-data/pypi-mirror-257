from dataclasses import asdict, dataclass


@dataclass
class RequestBodyClass:
    user_uuid: str
    telegram_bot_username: str
    telegram_user_id: str
    telegram_user_username: str
    telegram_user_fullname: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class WhitelistBodyClass:
    user_id: str
    uuid: str
    bot: str
