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
import ftplib
import glob
import shutil
import time

from backupz2.src.common.config import *
from backupz2.src.components.compress import Compress


@click.command()
@click.pass_context
def ftp(ctx):
    """Backup and send to ftp."""
    cftp = ctx.obj.get(CONF_FTP)
    name = ctx.obj.get(CONF_NAME)

    params = cftp.split(':')
    if '@' in params[1]:
        params += params[1].split('@')

    if len(params) != 5:
        click.echo('{} {}\n'.format(click.style('\nError FTP configuration:', fg="red"), cftp))
        exit(0)

    hostname = params[4]
    username = params[0]
    password = params[3]
    path = '{}/{}'.format(params[2], datetime.datetime.now().strftime(name))

    def get_connect():
        try:
            return ftplib.FTP(hostname)
        except ConnectionRefusedError:
            click.echo('{} {}\n'.format(click.style('\nError FTP login:', fg="red"), cftp))
            exit(0)

    session = get_connect()
    response = session.login(username, password)
    if '230' not in response:
        click.echo('{} {}\n'.format(click.style('\nError FTP login:', fg="red"), cftp))
        exit(0)

    try:
        session.mkd(path)
    except ftplib.error_perm:
        click.echo('{} {}\n'.format(click.style('\nFolder already exist:', fg="red"), path))
        exit(0)

    tmp = Compress(ctx).run()

    array = glob.glob('{}/*.tar.gz'.format(tmp))
    len_array = len(array)
    with click.progressbar(range(len_array)) as indexes:
        time.sleep(1)
        click.echo(click.style('\nStart upload to FTP\n', fg='blue'))
        for i in indexes:
            path_file = Path(array[i])
            file = open(path_file, 'rb')
            session.storbinary('STOR {}/%s'.format(path) % path_file.name, file)
            file.close()

    shutil.rmtree(tmp)
    session.quit()

    click.echo(click.style("\nDone successfully\n", fg="green"))


@click.command()
@click.pass_context
def folder(ctx):
    """Backup and save to folder."""

    save = ctx.obj.get(CONF_FOLDER)
    name = ctx.obj.get(CONF_NAME)
    path = Path('{}/{}'.format(save, datetime.datetime.now().strftime(name)))

    if path.exists():
        click.echo('{} {}\n'.format(click.style('\nFolder already exist:', fg="red"), path))
        exit(0)

    tmp = Compress(ctx).run()
    shutil.move(tmp, path)
    click.echo(click.style("\nDone successfully\n", fg="green"))
