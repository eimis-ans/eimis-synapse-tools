import json
from eimis_synapse_tools.synapse_client import SynapseClient


def do_get_users():
    client = SynapseClient()
    users = client.get_users()
    print(json.dumps(users, indent=2, sort_keys=True))


def do_deactivate_user(userId):
    client = SynapseClient()
    client.deactivate_users(userId)


def do_get_user(userId):
    client = SynapseClient()
    user = client.get_user(userId)
    print(json.dumps(user, indent=2, sort_keys=True))
