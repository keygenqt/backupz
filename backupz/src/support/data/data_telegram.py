from dataclasses import dataclass
from pathlib import Path

from telethon import TelegramClient


@dataclass
class DataTelegram:
    """Class contains data about telegram connects."""
    api_id: int
    api_hash: str
    path_session: Path

    @staticmethod
    def validate(data: dict) -> bool:
        if not isinstance(data['api_id'], int):
            return False
        if not isinstance(data['api_hash'], str):
            return False
        return True

    def __client(self) -> TelegramClient | None:
        try:
            return TelegramClient(str(self.path_session / 'telegram.session'), self.api_id, self.api_hash)
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
            # send message
            await client.send_message('+79889498250', "It's console app - backupz")
