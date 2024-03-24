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
from click import Context

from backupz.src.features.group_make import group_make
from backupz.src.support.conf import Conf
from backupz.src.support.dependency import check_dependency_init

check_dependency_init()

# Global config
_config: Conf | None = None

# Global context
_ctx: Context | None = None


@click.group(invoke_without_command=True)
@click.version_option(version=Conf.get_app_version(), prog_name=Conf.get_app_name())
@click.option(
    '--conf',
    default=None,
    help='Specify config path.',
    type=click.STRING,
    required=False)
@click.option(
    '--delete',
    is_flag=True,
    default=False,
    required=True, help="Delete download folder")
def main(conf: str, delete: bool):
    global _config
    _config = Conf(conf)
    group_make(_config, delete)


if __name__ == '__main__':
    try:
        main(standalone_mode=False)
    except click.exceptions.UsageError:
        main()
    except click.exceptions.Abort:
        path_to_save = _config.get_path_to_save()
        # Remove file archive if abort
        if path_to_save:
            path_to_save.unlink()
