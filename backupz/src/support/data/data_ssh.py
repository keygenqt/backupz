import socket
from dataclasses import dataclass
from pathlib import Path

from paramiko import ssh_exception
from paramiko.client import SSHClient, AutoAddPolicy

from backupz.src.support.output import echo_stderr, echo_line, echo_stdout
from backupz.src.support.progress_alive_bar import ProgressAliveBar
from backupz.src.support.texts import AppTexts


@dataclass
class DataSSH:
    """Class contains data about ssh connects."""
    hostname: str
    username: str
    port: int
    path: str
    auth: str | Path

    @staticmethod
    def validate(data: dict) -> bool:
        if 'hostname' not in data.keys() or not isinstance(data['hostname'], str):
            return False
        if 'username' not in data.keys() or not isinstance(data['username'], str):
            return False
        if 'port' not in data.keys() or not isinstance(data['port'], int):
            return False
        if 'path' not in data.keys() or not isinstance(data['path'], str):
            return False
        if 'auth' not in data.keys() or not isinstance(data['auth'], str):
            return False
        return True

    def __client(self) -> SSHClient | None:
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())

            if isinstance(self.auth, str):
                client.connect(
                    hostname=self.hostname,
                    username=self.username,
                    password=str(self.auth),
                    port=self.port,
                    timeout=5,
                )
            else:
                client.connect(
                    hostname=self.hostname,
                    username=self.username,
                    key_filename=str(self.auth),
                    port=self.port,
                    timeout=5,
                )
            return client
        except (Exception,):
            pass
        return None

    def upload(self, file: Path):
        try:
            # Create client
            client = self.__client()
            if not client:
                echo_stderr(AppTexts.error_connect('ssh', self.hostname))
                return

            echo_line()
            echo_stdout(AppTexts.info_upload('ssh', self.hostname))

            # Create ssh bar
            bar = ProgressAliveBar(AppTexts.success_upload())
            # Upload file
            client.open_sftp().put(file, '{upload_path}/{file_name}'.format(
                upload_path=self.path,
                file_name=file.name
            ), callback=bar.update)
            # Close connect
            client.close()
        except ssh_exception.SSHException as e:
            echo_stderr(AppTexts.error_exception(str(e)))
        except FileNotFoundError as e:
            echo_stderr(AppTexts.error_exception(str(e)))
