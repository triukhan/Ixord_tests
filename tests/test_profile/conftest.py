import pytest
import requests

from configuration import *


def _email_request(a):
    if isinstance(a, str):
        return requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=" + a, headers=PRF_TOKEN)
    else:
        return None


@pytest.fixture()
def email_request():
    return _email_request


@pytest.fixture()
def auto_reg():
    r_auto_test = requests.post(ENDPOINT + "auth/autoRegister")
    r_user_info = requests.get(ENDPOINT + "app/userInfo",
                               headers={"Authorization": "Bearer " + r_auto_test.json()['result']['token']})
    return [{"Authorization": "Bearer " + r_auto_test.json()["result"]["token"]}, r_user_info.json()["result"]["roles"][0]["workspaceId"]]