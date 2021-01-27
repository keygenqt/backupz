"""
Copyright 2021 Vitaliy Zarubin

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
from pathlib import Path

import click
from yaml import Loader
from yaml import load

from backupz2.src.components.helper import get_path_conf, get_default_conf

CONF_FOLDERS = 'folders'


class Config:

    @staticmethod
    def init_conf(conf=None):
        path = Path(get_path_conf(conf))
        if not path.is_file():
            type_conf = ('default', 'custom')[conf is not None]
            click.echo(click.style("\nAdded {} config. {}\nPlease configure the application.\n".format(type_conf, path), fg="yellow"))
            with open(path, 'w') as file:
                print(get_default_conf(), file=file)
        return path

    def __init__(self, test, conf):
        self.test = test
        self.path_conf = Config.init_conf(conf)
        with open(self.path_conf, 'rb') as file:
            self.conf = load(file.read(), Loader=Loader)

    def get(self, name):
        if name == CONF_FOLDERS:
            if name in self.conf:
                return self.conf[name]
            else:
                return []
