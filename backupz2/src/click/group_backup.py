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
import shutil
import subprocess
import tempfile

from backupz2.src.common.config import *


@click.group(name='backup')
def cli_backup():
    """Backup."""
    pass


def __backup(ctx, path_for_backup, tmp):
    """Common backup."""
    compression = ctx.obj.get(CONF_COMPRESSION)
    processes = ctx.obj.get(CONF_PROCESSES)
    path_to_backup = '{}/{}.tar.gz'.format(tmp, path_for_backup.name.strip('.'))
    command = 'tar --absolute-names --use-compress-program="pigz {} --recursive -p {}" -cf {} {}'.format(
        ('--{}'.format('{}'.format(compression).strip('-')), '-{}'.format('{}'.format(compression).strip('-')))[isinstance(compression, int)],
        processes,
        path_to_backup,
        path_for_backup.absolute()
    )
    print(command)
    subprocess.run([command], shell=True)


@cli_backup.command()
@click.pass_context
def ftp(ctx):
    """Backup and send to ftp."""
    pass


@cli_backup.command()
@click.pass_context
def folder(ctx):
    """Backup and save to folder."""

    # tmp = tempfile.mkdtemp()
    tmp = '/home/keygenqt/test'

    # compress folders
    for item in ctx.obj.get(CONF_FOLDERS):
        path = Path(item)
        if not path.exists():
            click.echo('Not exist')
        if not path.is_dir():
            click.echo('Not dir')
        __backup(ctx, Path(item), tmp)

    # compress files
    for item in ctx.obj.get(CONF_FILES):
        path = Path(item)
        if not path.exists():
            click.echo('Not exist')
        if not path.is_file():
            click.echo('Not file')
        __backup(ctx, Path(item), tmp)

    # shutil.rmtree(tmp, ignore_errors=False, onerror=None)
