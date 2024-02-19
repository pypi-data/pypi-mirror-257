import base64
import binascii
import re

import yaml

from mitmproxy import http


class AWSCredential:
    def __init__(self, access_key_id: str, date: str, region: str, service: str):
        self.access_key_id = access_key_id
        self.date = date
        self.region = region
        self.service = service
        try:
            self.account_id = self.get_account_id(self.access_key_id)
        except:
            self.account_id = "000000000000"

    def get_account_id(self) -> str:
        mask = 140737488355200
        id_type = self.access_key_id[4:]  # remove KeyID prefix
        id_bytes = base64.b32decode(id_type)  # base32 decode
        be_start = id_bytes[0:6]
        z = int.from_bytes(y, byteorder="big", signed=False)
        return (z & mask) >> 7


class Clotho:
    def __init__(self):
        with open("config.yaml.example") as f:
            self.config = yaml.load(f, Loader=yaml.CLoader)
        self.auth_re = re.compile(r"Credential=(A.*?)/(20.*?)/(.*?)/(.*?)/")

    def is_request_allowed(self, cred) -> bool:
        allowed_account = self.config.get(cred.account_id, self.config["accounts"].get("*", None))
        if not allowed_account:
            return False
        allowed_region = allowed_account["regions"].get(cred.region, allowed_account["regions"].get("*", None))
        if not allowed_region:
            return False
        if cred.service in allowed_region["services"] or "*" in allowed_region["services"]:
            return True
        return False

    async def request(self, flow):
        headers = dict(flow.request.headers)
        if "Authorization" not in headers:
            flow.response = http.Response.make(
                403,
                '{"Error":"Missing Authorization Token"}',
                {"content-type": "text/json"},
            )
            return
        try:
            parts = self.auth_re.findall(headers["Authorization"])[0]
            cred = AWSCredential(access_key_id=parts[0], date=parts[1], region=parts[2], service=parts[3])
        except Exception as e:
            flow.response = http.Response.make(
                400,
                '{"Error":"Malformed AWS SigV4 Request"}',
                {"content-type": "text/json"},
            )
            return
        else:
            try:
                if self.is_request_allowed(cred):
                    return
                else:
                    flow.response = http.Response.make(
                        403,
                        '{"Error":"Unauthorized"}',
                        {"content-type": "text/json"},
                    )
            except:
                flow.response = http.Response.make(400, '{"Error":"No account found"}', {"content-type": "text/json"})


addons = [Clotho()]
