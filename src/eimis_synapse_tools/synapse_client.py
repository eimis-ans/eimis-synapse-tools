import hashlib
import hmac
import logging
import os
import re
import secrets

import requests
from matrix_client.client import MatrixClient
from matrix_client.room import Room


class SynapseClient:
    client_path = "_matrix/client/v3"
    discovery_room_alias = "discoveryroom"

    def __init__(self, login=None, password=None):
        if not login:
            login = os.environ["ADMIN_USERNAME"]
        if not password:
            password = os.environ["ADMIN_PASSWORD"] 
        self.base_url = os.environ["SYNAPSE_URL"]
        self.domain = self.base_url.replace(
            "https://", "").replace("http://", "")
        self.login = login
        self.password = password
        self.token = self._get_auth_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _get_auth_token(self):
        auth_url = f"{self.base_url}/_matrix/client/v3/login"
        credentials = {
            "identifier": {"type": "m.id.user", "user": self.login},
            "initial_device_display_name": "✒️ Script",
            "password": self.password,
            "type": "m.login.password",
        }
        response = requests.post(auth_url, json=credentials)
        response.raise_for_status()
        auth_data = response.json()
        return auth_data["access_token"]

    def create_user(self, username, display_name, email, password=None):
        """Create a user; If no password is provided, generated one and display it"""
        logging.info("Creating user " + username)
        url = f"{self.base_url}/_synapse/admin/v2/users/%40{username}%3A{self.domain}"
        nonce = requests.get(
            f"{self.base_url}/_synapse/admin/v1/register").json()["nonce"]
        if not password:
            password = secrets.token_urlsafe(32)
        mac = generate_mac(
            nonce, username, password
        )

        registration_res = requests.put(
            url,
            json={
                "nonce": nonce,
                "username": username,
                "displayname": display_name,
                "threepids": [
                    {
                        "medium": "email",
                        "address": email
                    }
                ],
                "password": password,
                "admin": False,
                "mac": mac,
            },
            headers=self.headers
        ).json()

        if (
            "name" in registration_res and
            registration_res["name"] == f"@{username}:{self.domain}"
        ):
            logging.info("User created with password : " + password)
        elif "errcode" in registration_res and registration_res["errcode"] == "M_USER_IN_USE":
            logging.warn("User was already created")
        else:
            raise Exception("Error creating user", registration_res)

        return

    def get_users(self):
        url = f"{self.base_url}/_synapse/admin/v2/users?from=0&limit=10000&guests=false"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["users"]

    def get_user(self, user_id):
        url = f"{self.base_url}/_synapse/admin/v2/users/{user_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def deactivate_users(self, user_id):
        url = f"{self.base_url}/_synapse/admin/v1/deactivate/{user_id}"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        logging.info("User deactivated")

    def create_discovery_room(self):
        """Create a room with preset public_chat and visibility private
        and return the room_id"""
        request_url = f"{self.base_url}/_matrix/client/v3/createRoom"
        body = {
            "name": "Discovery Room",
            "power_level_content_override": {
                "events_default": 50,
                "invite": 50,
                "kick": 50,
                "state_default": 100,
                "users_default": 0,
            },
            "preset": "public_chat",
            "room_alias_name": f"{self.discovery_room_alias}",
            "room_version": "9",
            "visibility": "private",
            "join_rules": "public",
        }
        res = requests.post(url=request_url, json=body, headers=self.headers)
        return res.json()["room_id"]

    def get_users_in_room(self, room_id):
        """
        https://matrix-org.github.io/matrix-python-sdk/matrix_client.html#matrix_client.room.Room.get_joined_members
        """
        client = MatrixClient(self.base_url)
        client.login(username=self.login, password=self.password)

        room = Room(client, room_id)

        if not room:
            raise Exception("didn't find discovery room")
        return list(map(lambda user: user.user_id, room.get_joined_members()))

    def get_discovery_room_id(self, room_domain=None):
        if not room_domain:
            room_domain = self.domain
        room_url = f"{self.base_url}/{self.client_path}/directory/room/%23{self.discovery_room_alias}%3A{room_domain}"
        response = requests.get(room_url, headers=self.headers)
        response.raise_for_status()
        return response.json()["room_id"]

    def add_user_in_room(self, room_id, user_id):
        url = f"{self.base_url}/_synapse/admin/v1/join/%s" % room_id

        res = requests.post(
            url=url,
            json={
                "user_id": user_id,
            },
            headers=self.headers,
        )
        if res.status_code != 200:
            print(res)
            print(res.content)
            raise Exception(
                f"Error when joining the discovery room for user {user_id}", res
            )

    def join_discoveryroom(self, remote_domain, dry_run=False):
        room_id = self.get_discovery_room_id(remote_domain)
        url = f"{self.base_url}/_matrix/client/r0/join/{room_id}?server_name={remote_domain}"

        if dry_run:
            logging.info("Join remote discovery room : dry-run")
            return
        res = requests.post(
            url,
            headers=self.headers,
            json={"reason": "dummy user joins discovery room"},
        )
        res.raise_for_status()
        logging.info("Join remote discovery room : ok")


def generate_mac(nonce, user, password, admin=False, user_type=None):
    mac = hmac.new(
        key=bytearray(os.environ["SYNAPSE_SECRET"].encode("utf8")),
        digestmod=hashlib.sha1,
    )

    mac.update(nonce.encode("utf8"))
    mac.update(b"\x00")
    mac.update(user.encode("utf8"))
    mac.update(b"\x00")
    mac.update(password.encode("utf8"))
    mac.update(b"\x00")
    mac.update(b"admin" if admin else b"notadmin")
    if user_type:
        mac.update(b"\x00")
        mac.update(user_type.encode("utf8"))

    return mac.hexdigest()


def domain_not_port(url):
    return remove_after_last_colon(url).replace("https://", "").replace("http://", "")


def remove_after_last_colon(url):
    if url.count(':') < 2:
        return url
    pattern = r"(.*):[^:]*$"
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    else:
        return url
