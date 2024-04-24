import asyncio
from dataclasses import dataclass
from pathlib import Path

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest


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

    async def __client(self) -> TelegramClient | None:
        try:
            client = TelegramClient(
                str(self.path_session / '.backupz_telegram.session'),
                self.api_id,
                self.api_hash
            )
            await client.connect()
            return client
        except (Exception,):
            pass
        return None

    # Run asynchronous method with return
    @staticmethod
    def __run_blocking(function):
        loop = asyncio.get_event_loop()
        task = loop.create_task(function())
        loop.run_until_complete(task)
        return task.result()

    # Get count user channel
    def get_posts(self, channel_url: str) -> []:
        # asynchronous method
        async def _get_users_count() -> []:
            client = await self.__client()
            channel_name = channel_url.rsplit('/', 1)[-1]
            async with client:
                channel_connect = await client.get_entity(channel_name)
                posts = await client(GetHistoryRequest(
                    peer=channel_connect,
                    limit=1,  # 100 - max
                    offset_date=None,
                    offset_id=0,
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0))

                print(posts.messages[0].message)

                return [None]

        # Run asynchronous method with return
        return self.__run_blocking(_get_users_count)
