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

import click

from backupz.src.features.group_make import group_make
from backupz.src.support.conf import Conf
from backupz.src.support.dependency import check_dependency_init

# @todo check all dependency?
check_dependency_init()

# Path for save archive
config: Conf | None = None


@click.group(invoke_without_command=True)
@click.version_option(version=Conf.get_app_version(), prog_name=Conf.get_app_name())
@click.option(
    '--conf',
    default=None,
    help='Specify config path.',
    type=click.STRING,
    required=False)
def main(conf: str):
    global config
    config = Conf(conf)
    group_make(config)


if __name__ == '__main__':
    try:
        main(obj={}, standalone_mode=False)
    except click.exceptions.Abort:
        path_to_save = config.get_path_to_save()
        # Remove file archive if abort
        if path_to_save:
            path_to_save.unlink()
