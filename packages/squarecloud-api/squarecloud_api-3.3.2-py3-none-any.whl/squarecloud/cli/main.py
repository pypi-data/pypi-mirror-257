from typing import Literal

import click
from click import prompt
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from squarecloud.client import Client, create_config_file
from squarecloud.data import StatisticsData

from ..errors import RequestError, SquareException
from . import cli, run_async
from .app import app_list, upload_app
from .files import app_group

load_dotenv()


@cli.command(
    name='statistics', help='Get statistics information about the host'
)
@click.option(
    '--token',
    '-t',
    help='your api token',
    envvar='SQUARECLOUD_KEY',
    required=True,
    type=click.STRING,
    prompt='API KEY',
    hide_input=True,
)
@run_async
async def get_squarecloud_statistics(token: str):
    client = Client(api_key=token, debug=False)

    with Console().status('loading'):
        statistics_data: StatisticsData = await client.statistics()
    table = Table(title='Statistics', header_style='purple')

    table.add_column('Apps', justify='center')
    table.add_column('Websites', justify='center')
    table.add_column('Time', justify='center')
    table.add_column('Ping', justify='center')
    table.add_column('Users', justify='center')

    table.add_row(
        str(statistics_data.apps),
        str(statistics_data.websites),
        str(statistics_data.ping),
        str(statistics_data.users),
        style='green',
    )
    print(table)


@click.command(
    name='create-config-file',
    help='Create a config file to upload an application',
)
@click.argument(
    'output_file',
    type=click.Path(),
    required=False,
)
@click.option(
    '--display-name',
    help='Set the display name of your app',
    prompt='Enter display name',
)
@click.option(
    '--main',
    help='Set the display name of your app',
    prompt='Enter main',
)
@click.option(
    '--memory',
    help='Set the memory of the app',
    prompt='Enter memory',
    type=click.IntRange(100),
)
@click.option(
    '--version',
    help='Ensure that the version is either "recommended" or "latest"',
    type=click.Choice(['recommended', 'latest']),
    default='recommended',
    prompt='Enter version',
    required=False,
)
@click.option(
    '--description',
    help='Specify a description for the app',
    type=click.STRING,
    prompt='Enter description (optional)',
    default='',
    required=False,
)
@click.option(
    '--subdomain',
    help='Specify the subdomain of your app',
    prompt='Enter subdomain (optional)',
    default='',
    type=click.STRING,
)
@click.option(
    '--start',
    prompt='Enter start (optional)',
    default='',
    required=False,
    help='Specify the command that should be run when the application starts',
)
@click.option(
    '--auto_restart',
    help='Determine if the app should restart automatically after a crash',
    prompt='Enter auto restart (optional)',
    type=click.BOOL,
    default=False,
    required=False,
)
def create_config(
    output_file: str,
    display_name: str,
    main: str,
    memory: int,
    version: Literal['recommended', 'latest'] = 'recommended',
    description: str | None = None,
    subdomain: str | None = None,
    start: str | None = None,
    auto_restart: bool | None = None,
):

    content = create_config_file(
        path='/',
        display_name=display_name,
        main=main,
        memory=memory,
        version=version,
        description=description,
        subdomain=subdomain,
        start=start,
        auto_restart=auto_restart,
        save=False,
    )
    if output_file:
        with open(output_file, 'w') as f:
            f.write(content)
        print(
            Panel(
                f'\u2728  file saved successfully at {output_file}',
                border_style='green',
                style='green',
            )
        )
        return
    else:
        print(
            Panel(
                content,
                title='squarecloud.app',
                border_style='purple',
                style='green',
            )
        )
        r = prompt(
            'would you like to save the file? [y/N]',
            type=click.BOOL,
            default='Y',
        )
    if r:
        path = prompt(
            'where do you want to save the file', default='squarecloud.app'
        )
        with open(path, 'w') as f:
            f.write(content)
        print(
            Panel(
                f'\u2728  file saved successfully at {path}',
                border_style='green',
                style='green',
            )
        )


cli.add_command(app_group)
cli.add_command(app_list)
cli.add_command(create_config)
cli.add_command(upload_app)


def safe_entry_point():
    try:
        cli()
    except RequestError as e:
        title = e.__class__.__name__
        print(Panel(e.message, title=title, title_align='left', style='red'))
    except SquareException as e:
        print(
            Panel(
                e.message,
                title_align='left',
                style='red',
            ),
        )
    except Exception as e:
        print(
            Panel(
                str(e),
                title_align='left',
                style='red',
            ),
        )
