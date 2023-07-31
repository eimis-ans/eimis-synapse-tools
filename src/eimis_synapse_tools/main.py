import os

import click
from dotenv import load_dotenv

import eimis_synapse_tools.__init__ as init
from eimis_synapse_tools.cmd_discovery_room import do_discovery_room
from eimis_synapse_tools.cmd_import_users import do_import_users
from eimis_synapse_tools.cmd_simple_commands import (do_deactivate_user, do_get_user,
                                                     do_get_users)


@click.group()
def cli():
    """EIMIS scripts & tools for Matrix (Synapse)

    Make sure .env file is present and filled"""
    load_dotenv()
    # Fast fail if env var not set
    os.environ["SYNAPSE_URL"]
    os.environ["SYNAPSE_SECRET"]
    os.environ["ADMIN_USERNAME"]
    os.environ["ADMIN_PASSWORD"]


@cli.command
def version():
    """Print the application version information"""
    click.echo(init.__version__)


@cli.command
@click.option("-f",
              "--csv-file",
              type=str,
              required=True,
              help="Path to csv file containing users to be imported.")
@click.option("-d",
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
@click.option("-r",
              "--remote-url",
              type=str,
              required=False,
              help="Url of the remote homeserver")
@click.option("-d",
              "--dry-run",
              type=bool,
              is_flag=True,
              required=False,
              default=False,
              help="If set doesn't really import users.")
def setup_discoveryroom(remote_url, dry_run):
    """Setup discovery room 🪩\n
    - create a dummy user\n
    - make all HS users join the discovery room\n
    - make the dummy user join the remote discovery room"""
    do_discovery_room(remote_url, dry_run)


@cli.command
def get_users():
    """Get all users from csv file to Synapse"""
    do_get_users()


@cli.command
@click.option("-u",
              "--user-id",
              type=str,
              required=True,
              help="User id")
def get_user(user_id):
    """Get a user detail"""
    do_get_user(user_id)


@cli.command
@click.option("-u",
              "--user-id",
              type=str,
              required=True,
              help="User id")
def deactivate_user(user_id):
    """⚠️ Deactivate a user
    https://github.com/matrix-org/synapse/blob/develop/docs/admin_api/user_admin_api.md#deactivate-account"""
    if click.confirm(f"Deactivate {user_id} Do you want to continue?", abort=True):
        do_deactivate_user(user_id)


if __name__ == "__main__":
    cli()
