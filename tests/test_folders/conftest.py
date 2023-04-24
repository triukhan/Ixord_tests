import pytest
import requests

from configuration import *


@pytest.fixture()
def auto_reg():
    r_auto_test = requests.post(ENDPOINT + "auth/autoRegister")
    r_user_info = requests.get(ENDPOINT + "app/userInfo",
                               headers={"Authorization": "Bearer " + r_auto_test.json()['result']['token']})
    return [{"Authorization": "Bearer " + r_auto_test.json()["result"]["token"]},
            r_user_info.json()["result"]["roles"][0]["workspaceId"]]


@pytest.fixture()
def random_cyrillic_data():
    import random

    cyrillic_chars = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    random_data = ''.join(random.choice(cyrillic_chars) for _ in range(10))
    return random_data
