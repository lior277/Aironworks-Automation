import io
import json
from google.oauth2 import service_account
import google.auth.transport.requests


def generate_jwt(sa_keyfile, audience, expiry_length=1000):
    """Generates a signed JSON Web Token using a Google API Service Account."""
    with io.open(sa_keyfile, 'r', encoding='utf-8') as json_file:
        data = json.loads(json_file.read())
        sa_info = service_account.IDTokenCredentials.from_service_account_info(
            data, target_audience=audience
        )

    auth_req = google.auth.transport.requests.Request()
    sa_info.refresh(auth_req)

    return sa_info.token
