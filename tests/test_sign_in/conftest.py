import pytest
import requests

from configuration import *


@pytest.fixture()
def reg(rand):
    requests.post(ENDPOINT + "auth/exists", json={"Value": rand + "@gmail.com"})
    code = requests.post(ENDPOINT + "auth/checkConfirmationCode?email=" + rand + "@gmail.com" + "&code=")
    return [code[]]



