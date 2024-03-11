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

import subprocess
import tempfile
import time

from backupz2.src.common.config import *


class Compress:
    def __init__(self, ctx):
        self.files = ctx.obj.get(CONF_FILES)
        self.folders = ctx.obj.get(CONF_FOLDERS)
        self.processes = ctx.obj.get(CONF_PROCESSES)
        self.compression = ctx.obj.get(CONF_COMPRESSION)
        self.exclude = ctx.obj.get(CONF_EXCLUDE)
        self.names = []

    def run(self):
        tmp = tempfile.mkdtemp()

        errors = self.__check_data(self.files, True)
        if errors:
            click.echo(click.style('\nErrors files:', fg="red"))
            for item in errors:
                click.echo(click.style('{}'.format(item), fg="yellow"))
                self.files.remove(item)

        errors = self.__check_data(self.folders, False)
        if errors:
            click.echo(click.style('\nErrors folders:', fg="red"))
            for item in errors:
                click.echo(click.style('{}'.format(item), fg="yellow"))
                self.folders.remove(item)

        self.__compress_list(tmp, self.files, True)
        self.__compress_list(tmp, self.folders, False)

        return tmp

    def __get_exclude(self):
        result = []
        for e in self.exclude:
            result.append('--exclude="{}"'.format(e))
        return ' '.join(result)

    def __compress_list(self, tmp, array, is_file):
        """Compress list files, folders"""
        len_array = len(array)
        with click.progressbar(range(len_array)) as bar:
            time.sleep(1)
            click.echo(click.style("\nStart compress {}: {}\n".format(('folders', 'files')[is_file], len_array), fg="blue"))
            for i in bar:
                self.__backup(Path(array[i]), tmp)

    @staticmethod
    def __check_data(array, is_file=False):
        """Check is folder of file."""
        error = []
        if array:
            for item in array:
                path = Path(item)
                if not path.exists():
                    error.append(item)
                if not is_file and path.is_file():
                    error.append(item)
                elif is_file and path.is_dir():
                    error.append(item)
        return error

    def __get_name(self, name, index=1):
        """Add index to double names."""
        if name not in self.names:
            self.names.append(name)
            return name
        else:
            return self.__get_name('{}_{}'.format(name, index), index + 1)

    def __backup(self, path_for_backup, tmp):
        """Create backup."""
        exclude = self.__get_exclude()
        path_to_backup = '{}/{}.tar.gz'.format(tmp, self.__get_name(path_for_backup.name.strip('.')))
        command = 'tar --absolute-names --use-compress-program="pigz {} --recursive -p {}" {} -cf {} {}'.format(
            ('--{}'.format('{}'.format(self.compression).strip('-')), '-{}'.format('{}'.format(self.compression).strip('-')))[
                isinstance(self.compression, int)],
            self.processes,
            exclude,
            path_to_backup,
            path_for_backup.absolute()
        )
        subprocess.run([command], shell=True)
