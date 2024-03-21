import ftplib
import os
from dataclasses import dataclass
from pathlib import Path

from backupz.src.support.output import echo_stderr, echo_line, echo_stdout
from backupz.src.support.progress_alive_bar import ProgressAliveBar
from backupz.src.support.texts import AppTexts


@dataclass
class DataFTP:
    """Class contains data about ftp connects."""
    hostname: str
    username: str
    password: str
    port: int
    path: str

    @staticmethod
    def validate(data: dict) -> bool:
        if 'hostname' not in data.keys() or not isinstance(data['hostname'], str):
            return False
        if 'username' not in data.keys() or not isinstance(data['username'], str):
            return False
        if 'password' not in data.keys() or not isinstance(data['password'], str):
            return False
        if 'port' not in data.keys() or not isinstance(data['port'], int):
            return False
        if 'path' not in data.keys() or not isinstance(data['path'], str):
            return False
        return True

    def __client(self) -> ftplib.FTP | None:
        try:
            client = ftplib.FTP()
            client.connect(host=self.hostname, port=self.port, timeout=5)
            client.login(user=self.username, passwd=self.password)
            return client
        except (Exception,):
            pass
        return None

    def upload(self, file: Path):
        try:
            # Create client
            client = self.__client()
            if not client:
                echo_stderr(AppTexts.error_connect('ftp', self.hostname))
                return

            echo_line()
            echo_stdout(AppTexts.info_upload('ftp', self.hostname))

            # Create ftp bar
            bar = ProgressAliveBar(AppTexts.success_upload())

            # Load binary file
            file_binary = open(file, "rb")

            # Get file size
            total = os.path.getsize(file)

            # Upload file
            client.storbinary('STOR {upload_path}/{file_name}'.format(
                upload_path=self.path,
                file_name=file.name
            ), file_binary, 8192, lambda _: bar.up(
                total=total,
                transferred=8192
            ))
            # Close open file
            file_binary.close()
            # Close connect
            client.close()
        except ftplib.all_errors as e:
            echo_stderr(AppTexts.error_exception(str(e)))
        except FileNotFoundError as e:
            echo_stderr(AppTexts.error_exception(str(e)))
