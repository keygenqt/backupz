from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataSSH:
    """Class contains data about ssh connects."""
    ip: str
    port: int
    path: str
    auth: str | Path

    def get_connect(self) -> None:
        pass

    @staticmethod
    def validate(data: dict) -> bool:
        if 'ip' not in data.keys() or not isinstance(data['ip'], str):
            return False
        if 'port' not in data.keys() or not isinstance(data['port'], int):
            return False
        if 'path' not in data.keys() or not isinstance(data['path'], str):
            return False
        if 'auth' not in data.keys() or not isinstance(data['auth'], str):
            return False
        return True
