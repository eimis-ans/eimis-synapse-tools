import os

import click
from dotenv import load_dotenv

import __init__ as init
from cmd_import_users import do_import_users
from cmd_simple_commands import do_deactivate_user, do_get_user, do_get_users


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

@click.option( "-d",
    "--dry-run",
    type=bool,
    is_flag=True,
    required=False,
    default=False,
    help="If set doesn't really import users.")

def import_users(csv_file, dry_run):
    """Import users from csv file to Synapse"""
    do_import_users(csv_file, dry_run)

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

@cli.command
@click.option( "-u",
    "--user-id",
    type=str,
    required=True,
    help="User id")
def deactivate_user(user_id):
    """⚠️ Deactivate a user - https://github.com/matrix-org/synapse/blob/develop/docs/admin_api/user_admin_api.md#deactivate-account"""
    if click.confirm(f"Deactivate {user_id} Do you want to continue?", abort=True):
        do_deactivate_user(user_id)

if __name__ == "__main__":
    load_dotenv()

    # Fast fail if env var not set
    synapse_url = os.environ["SYNAPSE_URL"]
    synapse_secret = os.environ["SYNAPSE_SECRET"]
    admin_username = os.environ["ADMIN_USERNAME"]
    admin_password = os.environ["ADMIN_PASSWORD"]

    cli()
