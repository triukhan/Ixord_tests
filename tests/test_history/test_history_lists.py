import requests
import pytest

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


def test_appear_history(auto_reg):
    requests.post(ENDPOINT_EX + "cancelExecution?executionId=" + str(auto_reg[2]), headers=auto_reg[0])
    up_his = requests.get(ENDPOINT_EXS + "getExecutionsByWorkspace?type=1&workspaceKey=&skip=0&count=20&respectToAdmin"
                                         "Role=true&sortAcceding=false&includeEmail=", headers=auto_reg[0])
    Response(up_his).assert_status_code(200).validate(Post)
    assert len(up_his.json()["result"]["items"]) == 1