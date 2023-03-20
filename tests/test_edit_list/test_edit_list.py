import requests

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


def test_add_and_delete_smile_title(auto_reg):
    sl = requests.post(ENDPOINT_EX + "updateEmoji?executionId=" + auto_reg[2], headers=auto_reg[0],
                       json={"native": "😚", "colons": ":kissing_closed_eyes:", "id": "kissing_closed_eyes"})
    ds = requests.post(ENDPOINT_EX + "updateEmoji?executionId=" + auto_reg[2], headers=auto_reg[0], json={})
    Response(ds).assert_status_code(200).validate(Post)
    Response(sl).assert_status_code(200).validate(Post)


def test_change_title(auto_reg, rand):
    ct = requests.post(ENDPOINT_EX + "changeExecutionName?executionId=" + auto_reg[2] + "&newName=" + rand,
                       headers=auto_reg[0])
    Response(ct).assert_status_code(200).validate(Post)


def test_change_empty_title(auto_reg, rand):
    ct = requests.post(ENDPOINT_EX + "changeExecutionName?executionId=" + auto_reg[2] + "&newName=",
                       headers=auto_reg[0])
    assert ct.json()["hasError"] is True
    assert ct.json()["errorMessage"] == "name can not be null or empty"


def test_title_special_symbols(auto_reg):
    ct = requests.post(ENDPOINT_EX + "changeExecutionName?executionId=" + auto_reg[2] + "&newName=4$-bъъ_!!@#$''DF",
                       headers=auto_reg[0])
    Response(ct).assert_status_code(200).validate(Post)


def test_add_existing_tag_edit_list(auto_reg, rand):
    tid = requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand,
                        headers=auto_reg[0]).json()["result"]["id"]
    at = requests.post(ENDPOINT_EX + "addTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=
                       [{"id": tid}])
    Response(at).assert_status_code(200).validate(Post)
    assert at.json()["result"][0]["name"] == rand


def test_remove_tag_edit_list(auto_reg, rand):
    tid = requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand,
                        headers=auto_reg[0]).json()["result"]["id"]
    requests.post(ENDPOINT_EX + "addTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=
                       [{"id": tid, "workspaceId": auto_reg[1], "name": rand, "count":0}])
    dt = requests.post(ENDPOINT_EX + "removeTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=
                       [{"id": tid}])
    Response(dt).assert_status_code(200).validate(Post)
    assert dt.json()["result"][0]["name"] == rand

