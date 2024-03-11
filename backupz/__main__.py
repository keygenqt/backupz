import click

from backupz.src.support.conf import Conf
from backupz.src.support.dependency import check_dependency_init

check_dependency_init()


@click.group(invoke_without_command=True)
@click.version_option(version=Conf.get_app_version(), prog_name=Conf.get_app_name())
@click.option(
    '--conf',
    default=None,
    help='Specify config path.',
    type=click.STRING,
    required=False)
@click.pass_context
def main(ctx: {}, conf: str):
    ctx.obj = Conf(conf)


if __name__ == '__main__':
    main(obj={})
