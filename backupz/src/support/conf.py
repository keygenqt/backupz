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
from pathlib import Path

import click.exceptions
from yaml import Loader
from yaml import load

from backupz.src.support.helper import get_path_file
from backupz.src.support.output import echo_stdout
from backupz.src.support.texts import AppTexts

# Data versions
APP_NAME = 'backupz'
APP_VERSION = '2.0.0'

# Default path config
PATH_CONF = './.backupz/backupz.yaml'

CHANGELOG_CONF = r'''## Application configuration file Backupz
## Version config: 0.0.2
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
