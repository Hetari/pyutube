import click
import uTube.cli as app
from click_aliases import ClickAliasedGroup


@click.group(cls=ClickAliasedGroup)
def cli():
    pass


cli.add_command(app.info)
cli.add_command(app.welcome)
