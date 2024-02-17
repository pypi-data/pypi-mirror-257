"""Entrypoint for the OpenDAPI CLI."""
import click

from opendapi.cli.init import cli as init_cli
from opendapi.cli.generate import cli as generate_cli
from opendapi.cli.enrich.main import cli as enrich_cli
from opendapi.cli.run import cli as run_cli


@click.group()
def cli():
    """
    OpenDAPI CLI is a command-line interface to initialize and run OpenDAPI projects.\n\n

    This tool helps autogenerate DAPI files and associated configuration files,
    and interacts with DAPI servers to bring the power of AI to your data documentation.\n\n

    Use `opendapi [COMMAND] --help` for more information about a command.
    """


# Add commands to the CLI
cli.add_command(init_cli, name="init")
cli.add_command(generate_cli, name="generate")
cli.add_command(enrich_cli, name="enrich")
cli.add_command(run_cli, name="run")
