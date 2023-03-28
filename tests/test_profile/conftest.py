import pytest
import requests

from configuration import *


# @pytest.fixture()
# def auto_reg():


@pytest.fixture()
def rand():
    import random
    import string

    rand = ''.join(random.choice(string.ascii_uppercase) for _ in range(25))
    return rand


