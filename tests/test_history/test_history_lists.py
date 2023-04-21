import requests
import pytest

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


def test_appear_history_remove(auto_reg):
    requests.post(ENDPOINT_EX + "cancelExecution?executionId=" + auto_reg[2], headers=auto_reg[0])
    up_his = requests.get(ENDPOINT_EXS + "getExecutionsByWorkspace?type=1&workspaceKey=&skip=0&count=20&respectToAdmin"
                                         "Role=true&sortAcceding=false&includeEmail=", headers=auto_reg[0])
    Response(up_his).assert_status_code(200).validate(Post)
    assert len(up_his.json()["result"]["items"]) == 1


def test_appear_history_complete(auto_reg):
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]
    requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{"stepId": sid, "executed": 100}])
    up_his = requests.get(ENDPOINT_EXS + "getExecutionsByWorkspace?type=1&workspaceKey=&skip=0&count=20&respectToAdmin"
                                         "Role=true&sortAcceding=false&includeEmail=", headers=auto_reg[0])
    Response(up_his).assert_status_code(200).validate(Post)
    assert len(up_his.json()["result"]["items"]) == 1


def test_repeat_history(auto_reg):
    requests.post(ENDPOINT_EX + "cancelExecution?executionId=" + auto_reg[2], headers=auto_reg[0])
    repeat = requests.post(ENDPOINT_EX + "repeatExecution?executionId=" + auto_reg[2], headers=auto_reg[0])
    refresh = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={})
    Response(repeat).assert_status_code(200).validate(Post)
    assert len(refresh.json()["result"]["items"]) == 1


def test_repeat_history_by_changes(auto_reg):
    requests.post(ENDPOINT_EX + "cancelExecution?executionId=" + auto_reg[2], headers=auto_reg[0])
    add_text = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
                 "value": "{\"blocks\":[{\"type\":\"paragraph\",\"data\":{\"text\":\"some_text\"}}]}"})
    refresh = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={})
    Response(add_text).assert_status_code(200).validate(Post)
    assert len(refresh.json()["result"]["items"]) == 1


def test_history_save_tags(auto_reg, rand):
    requests.post(ENDPOINT_EX + "addTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=[{"name": rand}])
    requests.post(ENDPOINT_EX + "cancelExecution?executionId=" + auto_reg[2], headers=auto_reg[0])
    repeat = requests.post(ENDPOINT_EX + "repeatExecution?executionId=" + auto_reg[2], headers=auto_reg[0])
    refresh = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={})
    Response(repeat).assert_status_code(200).validate(Post)
    assert len(refresh.json()["result"]["items"][0]["tags"]) == 1


def test_tag_disappear_history(auto_reg, rand):
    cr = requests.post(ENDPOINT_EX + "addTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=[{"name": rand}])
    requests.post(ENDPOINT_EX + "cancelExecution?executionId=" + auto_reg[2], headers=auto_reg[0])
    requests.post(ENDPOINT + "tags/deleteTag?workspaceId=" + str(auto_reg[1]) + "&tagId="
                  + str(cr.json()["result"][0]["id"]), headers=auto_reg[0])
    upd = requests.get(ENDPOINT_EXS + "getExecutionsByWorkspace?type=1&workspaceKey=&skip=0&count=20&"
                       "respectToAdminRole=true&sortAcceding=false&includeEmail=", headers=auto_reg[0])
    Response(upd).assert_status_code(200).validate(Post)
    assert len(upd.json()["result"]["items"][0]["tags"]) == 0
