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

import click

from backupz2.src.common.config import Config
from backupz2.src.components.helper import get_app_version, get_app_name

Config.init_conf()


@click.group()
@click.pass_context
@click.version_option(version=get_app_version(), prog_name=get_app_name())
@click.option('--test', help='For test.', hidden=True, is_flag=True, default=False, is_eager=True)
@click.option('--conf', '-c', default=None, help='Specify config path.', type=click.STRING, required=False)
def cli(ctx, test, conf):
    """Create backup tar.gz archive in multiple processes and send to ftp or save to folder."""
    if not test:
        ctx.obj = Config(test, conf)


if __name__ == '__main__':
    cli(obj={})
