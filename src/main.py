import os
import sys

import click
from dotenv import load_dotenv

import __init__ as init
from runner import do_get_user, do_get_users, do_import_users

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
    help="Path to csv file containing users to be imported.")

def import_users(csv_file):
    """Import users from csv file to Synapse"""
    do_import_users(csv_file)

@cli.command
def get_users():
    """Get all users from csv file to Synapse"""
    do_get_users()

@cli.command
@click.option( "-u",
    "--user-id",
    type=str,
    required=True,
    help="User id")
def get_user(user_id):
    """Get a user detail"""
    do_get_user(user_id)

if __name__ == "__main__":
    load_dotenv()

    # Fast fail if env var not set
    synapse_url = os.environ["SYNAPSE_URL"]
    synapse_secret = os.environ["SYNAPSE_SECRET"]
    admin_username = os.environ["ADMIN_USERNAME"]
    admin_password = os.environ["ADMIN_PASSWORD"]

    cli()
