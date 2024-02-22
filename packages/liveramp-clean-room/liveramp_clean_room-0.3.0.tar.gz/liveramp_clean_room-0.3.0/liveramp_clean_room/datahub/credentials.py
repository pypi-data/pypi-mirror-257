import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Credentials:
    """Service account credentials."""

    account_id: str
    client_id: str
    secret_key: str
    token_uri: str

    @staticmethod
    def from_json(raw_credentials: str) -> "Credentials":
        json_credentials = json.loads(raw_credentials)

        return Credentials(
            client_id=json_credentials["client_id"],
            account_id=json_credentials["account_id"],
            secret_key=json_credentials["secret_key"],
            token_uri=json_credentials["token_uri"],
        )

    @staticmethod
    def from_file(raw_credentials: str) -> "Credentials":
        with open(raw_credentials, "r", encoding="UTF-8") as cred_file:
            json_credentials = json.load(cred_file)

        return Credentials(
            client_id=json_credentials["client_id"],
            account_id=json_credentials["account_id"],
            secret_key=json_credentials["secret_key"],
            token_uri=json_credentials["token_uri"],
        )
