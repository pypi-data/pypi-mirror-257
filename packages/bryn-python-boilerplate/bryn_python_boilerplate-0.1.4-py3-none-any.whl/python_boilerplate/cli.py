"""Console script for python_boilerplate."""

import click


@click.version_option(package_name="bryn_python_boilerplate")
@click.command()
def cli(args=None):
    """Console script for python_boilerplate."""
    click.echo("Replace this message by putting your code into python_boilerplate.cli.cli")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0
