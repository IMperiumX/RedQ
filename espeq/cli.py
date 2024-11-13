"""Console script for redq."""
import json
import sys

import click

from redq.utils import import_app
from redq.worker import Worker

from . import utils
from .scheduler import Scheduler


@click.command()
def main(args=None):
    """Console script for redq."""
    click.echo("Replace this message by putting your code into " "redq.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


@click.command()
@click.option("--app", required=True, help="Import path of the redq instance.")
def worker(**options):
    """Run worker(s) to process tasks from queue(s) defined in your app."""
    redq = import_app(options.pop("app"))
    worker = Worker(redq=redq)
    worker.start()


@click.command()
@click.option("--app", required=True, help="Import path of the redq instance.")
def info(**options):
    """Inspect and print info about your queues."""
    redq = import_app(options.pop("app"))
    _info = utils.inspect(redq)
    json_formatted_str = json.dumps(_info, indent=2, sort_keys=True)
    click.echo(json_formatted_str)


@click.command()
@click.option("--app", required=True, help="Import path of the redq instance.")
@click.option(
    "--foreground",
    is_flag=True,
    help="Run in foreground; Default is to run as daemon in background.",
)
def scheduler(**options):
    """Run a scheduler to enqueue periodic tasks based on a schedule defined in your app."""
    redq = import_app(options.pop("app"))
    result = Scheduler(redq=redq, **options)
    if result:
        click.fail(result)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
