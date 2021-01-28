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
import datetime
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

    error_not_is_folder = []
    error_not_is_file = []
    error_not_exist = []

    tmp = tempfile.mkdtemp()
    name = ctx.obj.get(CONF_NAME)
    save = Path('{}/{}'.format(ctx.obj.get(CONF_SAVE), datetime.datetime.now().strftime(name)))

    len_folders = len(ctx.obj.get(CONF_FOLDERS))
    with click.progressbar(range(len_folders)) as bar:

        click.echo(click.style("\nStart compress folders: {}\n".format(len_folders), fg="blue"))

        # compress folders
        for i in bar:
            item = ctx.obj.get(CONF_FOLDERS)[i]
            path = Path(item)
            if not path.exists():
                error_not_exist.append(click.style('{}'.format(path.absolute()), fg="red"))
            elif not path.is_dir():
                error_not_is_folder.append(click.style('{}'.format(path.absolute()), fg="red"))
            else:
                __backup(ctx, Path(item), tmp)

    len_files = len(ctx.obj.get(CONF_FILES))
    with click.progressbar(range(len_files)) as bar2:

        click.echo(click.style("\nStart compress files: {}\n".format(len_files), fg="blue"))

        # compress files
        for i in bar2:
            item = ctx.obj.get(CONF_FILES)[i]
            path = Path(item)
            if not path.exists():
                error_not_exist.append(click.style('{}'.format(path.absolute()), fg="red"))
            elif not path.is_file():
                error_not_is_file.append(click.style('{}'.format(path.absolute()), fg="red"))
            else:
                __backup(ctx, Path(item), tmp)

    if error_not_exist:
        click.echo(click.style("\nNot exist:", fg="red"))
        for e in error_not_exist:
            click.echo(e)

    if error_not_is_folder:
        click.echo(click.style("\nNot is folder:", fg="red"))
        for e in error_not_is_folder:
            click.echo(e)

    if error_not_is_file:
        click.echo(click.style("\nNot is file:", fg="red"))
        for e in error_not_is_file:
            click.echo(e)

    if save.exists():
        shutil.rmtree(save)

    shutil.move(tmp, save)
