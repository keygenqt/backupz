import asyncio
import random
import time
from dataclasses import dataclass
from pathlib import Path

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from backupz.src.support.output import echo_stdout
from backupz.src.support.progress_alive_bar import ProgressAliveBar
from backupz.src.support.texts import AppTexts


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
    def get_posts(self, channel_url: str, folder: Path) -> []:
        # asynchronous method
        async def _get_users_count() -> []:
            client = await self.__client()
            channel_name = channel_url.rsplit('/', 1)[-1]
            async with client:
                channel_connect = await client.get_entity(channel_name)

                folders = []
                limit = 20
                add_offset = 0
                bar = ProgressAliveBar(AppTexts.success_upload())

                while True:
                    # Get posts
                    channel_messages = await client(GetHistoryRequest(
                        peer=channel_connect,
                        limit=limit,
                        offset_date=None,
                        offset_id=0,
                        max_id=0,
                        min_id=0,
                        add_offset=add_offset,
                        hash=0))

                    # Get count messages
                    channel_size = channel_messages.count

                    # Add offset for next query
                    add_offset += limit
                    if add_offset > channel_size:
                        add_offset = channel_size

                    # Update progress
                    bar.update(add_offset, channel_size)

                    # Save messages
                    for post in channel_messages.messages:
                        if post.message:
                            folder_post = folder / channel_name / post.date.strftime('%Y-%m-%d_%H-%M-%S')
                            Path(folder_post).mkdir(parents=True, exist_ok=True)
                            await client.download_media(post.media, str(folder_post))
                            with open(folder_post / 'message', 'w') as file:
                                print(post.message, file=file)
                            folders.append(folder_post)

                    # Exit if end
                    if add_offset >= channel_size:
                        break

                    # Mini fix
                    time.sleep(random.randint(1, 3))

                return folders

        # Start downloads
        echo_stdout(AppTexts.info_download_start(channel_url))

        # Run asynchronous method with return
        return self.__run_blocking(_get_users_count)
