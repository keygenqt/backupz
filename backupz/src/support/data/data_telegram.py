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
            # send message
            await client.send_message(
                'username',
                'Я приложение Backupz, что бы мне такое забэкапить... =)'
            )
