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

from backupz2.src.common.config import *
from backupz2.src.components.compress import Compress


@click.command()
@click.pass_context
def ftp(ctx):
    """Backup and send to ftp."""
    pass


@click.command()
@click.pass_context
def folder(ctx):
    """Backup and save to folder."""

    save = ctx.obj.get(CONF_FOLDER)
    name = ctx.obj.get(CONF_NAME)
    path = Path('{}/{}'.format(save, datetime.datetime.now().strftime(name)))

    tmp = Compress(ctx).run()

    if path.exists():
        shutil.rmtree(path)

    shutil.move(tmp, path)

    click.echo(click.style("\nDone successfully\n", fg="green"))
