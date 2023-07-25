import logging
import secrets

from synapse_client import SynapseClient

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


def do_discovery_room(remote_domain, dry_run):
    client = SynapseClient()

    dummy_password = secrets.token_urlsafe(32)
    dummy_user = "dummy_user"
    if not dry_run:
        client.create_user(dummy_user, "Dummy User", "dummy-mail@nowhere.fr", dummy_password)

    discovery_room_id = client.get_discovery_room_id()
    if not discovery_room_id and not dry_run:
        logging.info("Create discovery room...")
        discovery_room_id = client.create_discovery_room()

    # get all users in home server (can be up to 100k)
    all_users_by_name = client.get_users()

    all_user_ids = parse_get_users(all_users_by_name)

    logging.info("Users in homeserver : %s" % len(all_user_ids))

    # get all users in discovery room
    users_in_room = client.get_users_in_room(discovery_room_id)

    logging.info("Users in room (with dummy users): %s" % len(users_in_room))

    # list all users missing the room
    users_missing_in_room = set(
        all_user_ids).difference(set(users_in_room))
    logging.info("Users missing in room : %s" % len(users_missing_in_room))

    # add user one by one
    for index, user_id in enumerate(users_missing_in_room):
        logging.info(
            f"{len(users_missing_in_room)}/{index + 1} Adding user {user_id} in room : {discovery_room_id}"
        )
        if not dry_run:
            client.add_user_in_room(
                room_id=discovery_room_id, user_id=user_id
            )

    dummy_client = SynapseClient( dummy_user, dummy_password)
    dummy_client.join_discoveryroom(remote_domain, dry_run)


def parse_get_users(raw_user_name):
    return list(map(lambda x: x["name"], raw_user_name))
