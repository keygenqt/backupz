from dataclasses import dataclass

from telethon import TelegramClient


@dataclass
class DataTelegram:
    """Class contains data about telegram connects."""
    api_id: int
    api_hash: str

    @staticmethod
    def validate(data: dict) -> bool:
        if not isinstance(data['api_id'], int):
            return False
        if not isinstance(data['api_hash'], str):
            return False
        return True

    def __client(self) -> TelegramClient | None:
        try:
            return TelegramClient('anon', self.api_id, self.api_hash)
        except (Exception,):
            pass
        return None

    async def start(self):
        # Get client
        client = self.__client()
        async with client:
            # Getting information about yourself
            me = await client.get_me()
            # "me" is a user object. You can pretty-print
            # any Telegram object with the "stringify" method:
            print(me.stringify())
