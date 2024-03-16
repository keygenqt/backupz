"""
Copyright 2021-2024 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
from datetime import datetime
from pathlib import Path

import click.exceptions
from yaml import Loader
from yaml import load

from backupz.src.support.helper import get_path_file, get_path_folder
from backupz.src.support.output import echo_stdout, echo_stderr
from backupz.src.support.texts import AppTexts

# Data versions
APP_NAME = 'backupz'
APP_VERSION = '2.0.0'

# Default path config
PATH_CONF = '~/.backupz/configuration.yaml'

CHANGELOG_CONF = r'''## Application configuration file Backupz
## Version config: 0.0.2

# Folders and files for backup
backup:
  - ~/.backupz

# https://linux.die.net/man/1/tar
# Exclude by regex (tar --exclude)
exclude: []

# https://linux.die.net/man/1/pigz
# Regulate the speed of compression using the specified digit #, where -1 or --fast indicates the
# fastest compression method (less compression) and -9 or --best indicates the slowest compression
# method. Level 0 is no compression.
# 1 to 9 or fast/best
compression: best

# Name folder for save backup in format 'datetime.strftime'
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
name: 'backupz_%d_%m_%Y'

# Folder for save
folder: ~/backupz
'''


# Loader configuration yaml
class Conf:

    @staticmethod
    def get_app_name() -> str:
        return APP_NAME

    @staticmethod
    def get_app_version() -> str:
        return APP_VERSION

    @staticmethod
    def _get_path_conf(path, default):
        path = get_path_file(path)

        default = get_path_file(default, none=False)

        if path and str(path).lower().endswith('.yaml'):
            return path
        else:
            if not default.is_file():
                Conf._create_default_config(default)
            return Path(default)

    @staticmethod
    def _create_default_config(path: Path):
        if not click.confirm(AppTexts.confirm_init()):
            exit(0)

        path_dir = os.path.dirname(path)

        # Create dir if not exist
        if not os.path.isdir(path_dir):
            Path(path_dir).mkdir()

        # Write default configuration file
        with open(path, 'w') as file:
            print(CHANGELOG_CONF, file=file)

        echo_stdout(AppTexts.success_init(str(path)), 2)

    def __init__(self, path):
        # Get path config
        self.conf_path = Conf._get_path_conf(path, default=PATH_CONF)

        # Load config
        with open(self.conf_path, 'rb') as file:
            self.conf = load(file.read(), Loader=Loader)

    # Get path for save tar.gz archive
    def get_path_to_save(self) -> Path:
        return self.get_folder_for_save() / '{name}.tar.gz'.format(
            name=datetime.now().strftime(self.get_name())
        )

    # Get paths folder and files for backup
    def get_backup_paths(self) -> [str]:
        if 'backup' not in self.conf.keys():
            echo_stderr(AppTexts.error_load_key('backup'))
            exit(1)
        else:
            if not isinstance(self.conf['backup'], list):
                echo_stderr(AppTexts.error_load_key('backup'))
                exit(1)
            return self.conf['backup']

    # Get exclude regex exclude files
    # https://linux.die.net/man/1/tar
    # Exclude by regex (tar --exclude)
    def get_exclude(self) -> [str]:
        if 'exclude' not in self.conf.keys():
            echo_stderr(AppTexts.error_load_key('exclude'))
            exit(1)
        else:
            if not isinstance(self.conf['exclude'], list):
                echo_stderr(AppTexts.error_load_key('exclude'))
                exit(1)
            return self.conf['exclude']

    # Get level compression.
    # 1 to 9 or fast/best
    def get_compression(self) -> str:
        if 'compression' not in self.conf.keys():
            echo_stderr(AppTexts.error_load_key('compression'))
            exit(1)
        else:
            # Check int 0-9
            if isinstance(self.conf['compression'], int) and 0 <= self.conf['compression'] < 10:
                return '-{}'.format(self.conf['compression'])
            # Check str best/fast
            if (isinstance(self.conf['compression'], str)
                    and (self.conf['compression'] == 'best' or self.conf['compression'] == 'fast')):
                return '--{}'.format(self.conf['compression'])
            # Error
            echo_stderr(AppTexts.error_load_key('compression'))
            exit(1)

    # Get name format archive
    def get_name(self) -> str:
        if 'name' not in self.conf.keys():
            echo_stderr(AppTexts.error_load_key('name'))
            exit(1)
        else:
            if not isinstance(self.conf['name'], str):
                echo_stderr(AppTexts.error_load_key('name'))
                exit(1)
            return self.conf['name']

    # Get path to folder for save archive
    def get_folder_for_save(self) -> Path:
        if 'folder' not in self.conf.keys():
            echo_stderr(AppTexts.error_load_key('folder'))
            exit(1)
        else:
            if not isinstance(self.conf['folder'], str):
                echo_stderr(AppTexts.error_load_key('folder'))
                exit(1)
            path = get_path_folder(self.conf['folder'])
            if not path:
                echo_stderr(AppTexts.error_found_folder_for_save(self.conf['folder']))
                exit(1)
            return path
