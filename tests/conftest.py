import pytest
import requests

from configuration import ENDPOINT
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


@pytest.fixture()
def auto_reg():
    r = requests.post(ENDPOINT + "auth/autoRegister")
    response = Response(r)
    response.assert_status_code(200).validate(Post)
    return r.json()['result']['token']
