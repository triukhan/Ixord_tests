import pytest
import requests

from configuration import ENDPOINT
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


@pytest.fixture()
def auto_reg():
    r_auto_test = requests.post(ENDPOINT + "auth/autoRegister")
    resp_ar = Response(r_auto_test)
    resp_ar.assert_status_code(200).validate(Post)

    r_user_info = requests.get(ENDPOINT + "app/userInfo",
                               headers={"Authorization": "Bearer " + r_auto_test.json()['result']['token']})
    resp_ui = Response(r_user_info)
    resp_ui.assert_status_code(200).validate(Post)
    return [r_auto_test.json()["result"]["token"], r_user_info.json()["result"]["roles"][0]["workspaceId"]]


@pytest.fixture()
def random_data():
    import random
    import string

    random_data = ''.join(random.choice(string.ascii_uppercase) for _ in range(20))
    return random_data

@pytest.fixture()
def random_cyrillic_data():
    import random

    cyrillic_chars = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    random_data = ''.join(random.choice(cyrillic_chars) for _ in range(10))
    return random_data
