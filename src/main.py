import os
import sys

import click
from dotenv import load_dotenv

import __init__ as init
from runner import do_import_users

@click.group()
def cli():
    """EIMIS scripts for batch matrix enrollment.
    
    Make sure .env file is present and filled"""
    pass


@cli.command
def version():
    """Print the application version information"""
    click.echo(init.__version__)

@cli.command
@click.option( "-f",
    "--csv-file",
    type=str,
    required=True,
    default="default",
    help="Path to csv file containing users to be imported.")

def import_users(csv_file):
    do_import_users(csv_file)


if __name__ == "__main__":
    load_dotenv()

    # Fast fail if env var not set
    synapse_url = os.environ["SYNAPSE_URL"]
    synapse_secret = os.environ["SYNAPSE_SECRET"]
    admin_username = os.environ["ADMIN_USERNAME"]
    admin_password = os.environ["ADMIN_PASSWORD"]

    cli()
