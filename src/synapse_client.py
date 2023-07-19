import hashlib
import hmac
import logging
import os
import secrets

import requests

class SynapseClient:
    def __init__(self):
        self.base_url = os.environ["SYNAPSE_URL"]
        self.domain = self.base_url.replace("https://", "").replace("http://", "")
        self.login = os.environ["ADMIN_USERNAME"]
        self.password = os.environ["ADMIN_PASSWORD"]
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

    def create_user(self, username, display_name, email):
        logging.info("Creating user " + username)
        url = f"{self.base_url}/_synapse/admin/v1/register"
        nonce = requests.get(url).json()["nonce"]
        password = secrets.token_urlsafe(32)
        mac = generate_mac(
            nonce, username,password
        )

        registration_res = requests.post(
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
        ).json()

        if (
            "user_id" in registration_res and 
            registration_res["user_id"] == f"@{username}:{self.domain}"
        ):
             logging.info("User created " + password)
        elif "errcode" in registration_res and registration_res["errcode"] == "M_USER_IN_USE":
             logging.warn("User was already created")
        else:
            raise Exception("Error creating user", registration_res)

        return
    
    def get_users(self):
        url = f"{self.base_url}/_synapse/admin/v2/users"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_user(self, user_id):
        url = f"{self.base_url}/_synapse/admin/v2/users/{user_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
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
