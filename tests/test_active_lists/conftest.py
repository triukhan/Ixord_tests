import pytest
import requests

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


@pytest.fixture()
def auto_reg():
    r_auto_test = requests.post(ENDPOINT + "auth/autoRegister")

    r_user_info = requests.get(ENDPOINT + "app/userInfo",
                               headers={"Authorization": "Bearer " + r_auto_test.json()['result']['token']})

    cre_lis = requests.post(ENDPOINT_LIST, headers={"Authorization": "Bearer " + r_auto_test.json()["result"]["token"]},
                            json={"name": "New Test List", "value": "{\"blocks\":[]}",
                                  "workspaceId": r_user_info.json()["result"]["roles"][0]["workspaceId"]})
    return [{"Authorization": "Bearer " + r_auto_test.json()["result"]["token"]},
            r_user_info.json()["result"]["roles"][0]["workspaceId"],
            cre_lis.json()["result"]["id"], cre_lis.json()["result"]["secureKey"]]


@pytest.fixture()
def rand():
    import random
    import string

    rand = ''.join(random.choice(string.ascii_uppercase) for _ in range(20))
    return rand
