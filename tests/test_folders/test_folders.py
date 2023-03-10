import requests

from configuration import ENDPOINT
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post
from src.enums.global_enums import *


def test_create_folder(auto_reg):
    req_create_folder = requests.post(ENDPOINT + "tags/addTag?workspaceId=" +
                                      str(auto_reg[1]) + "&parentId=&name=test_folder",
                                      headers={"Authorization": "Bearer " + auto_reg[0]})
    r = Response(req_create_folder)
    r.assert_status_code(200).validate(Post)
    asr_cf = req_create_folder.json()["result"]
    assert asr_cf["parents"] is None
    assert asr_cf["hasChildren"] == False
    assert type(asr_cf["id"]) is int


def test_update_folder(auto_reg):
    req_create_folder = requests.post(ENDPOINT + "tags/addTag?workspaceId=" +
                                      str(auto_reg[1]) + "&parentId=&name=test_folder",
                                      headers={"Authorization": "Bearer " + auto_reg[0]})
    asr_cf = req_create_folder.json()["result"]

    req_update_tags = requests.post(ENDPOINT + "tags/getTags?workspaceId=" + str(auto_reg[1]) + "&parentId=&search=",
                                    headers={"Authorization": "Bearer " + auto_reg[0]}, json=[])
    r = Response(req_update_tags)
    r.assert_status_code(200).validate(Post)
    asr_ut = req_update_tags.json()["result"][0]
    assert asr_cf["id"] == asr_ut["id"], asr_cf["name"] == asr_ut["name"]


def test_search_tag(auto_reg, random_data):
    requests.post(ENDPOINT + "tags/addTag?workspaceId=" + str(auto_reg[1]) + "&parentId=&name=" + random_data,
                  headers={"Authorization": "Bearer " + auto_reg[0]})
    requests.post(ENDPOINT + "tags/addTag?workspaceId=" + str(auto_reg[1]) + "&parentId=&name=test_folder",
                  headers={"Authorization": "Bearer " + auto_reg[0]})
    requests.post(ENDPOINT + "tags/addTag?workspaceId=" + str(auto_reg[1]) + "&parentId=&name=ball",
                  headers={"Authorization": "Bearer " + auto_reg[0]})
    req_search_tags = requests.post(ENDPOINT + "tags/getTags?workspaceId=" + str(auto_reg[1]) + "&parentId=&search="
                                    + random_data, headers={"Authorization": "Bearer " + auto_reg[0]}, json=[])
    Response(req_search_tags).assert_status_code(200).validate(Post)
    asr_st = req_search_tags.json()["result"]
    assert len(asr_st) == 1, GlobalErrorMessages.WRONG_NUMBER_OF_ELEMENTS
    assert asr_st[0]["name"] == random_data


def test_trim_search_tag(auto_reg, random_data):
    requests.post(ENDPOINT + "tags/addTag?workspaceId=" + str(auto_reg[1]) + "&parentId=&name=" + random_data,
                  headers={"Authorization": "Bearer " + auto_reg[0]})
    req_update_tags = requests.post(ENDPOINT + "tags/getTags?workspaceId=" + str(auto_reg[1])
                                    + "&parentId=&search=" + random_data[7:],
                                    headers={"Authorization": "Bearer " + auto_reg[0]}, json=[])
    Response(req_update_tags).assert_status_code(200).validate(Post)
    asr_up = req_update_tags.json()["result"]
    assert random_data == asr_up[0]["name"]


def test_spaces_search(auto_reg, random_data):
    requests.post(ENDPOINT + "tags/addTag?workspaceId=" + str(auto_reg[1]) + "&parentId=&name=" + random_data + " book",
                  headers={"Authorization": "Bearer " + auto_reg[0]})
    req_update_tags = requests.post(ENDPOINT + "tags/getTags?workspaceId=" + str(auto_reg[1])
                                    + "&parentId=&search=" + random_data + " book",
                                    headers={"Authorization": "Bearer " + auto_reg[0]}, json=[])
    asr_up = req_update_tags.json()["result"]
    Response(req_update_tags).assert_status_code(200).validate(Post)
    assert random_data + " book" == asr_up[0]["name"]


def test_special_symbols_search(auto_reg, random_data):
    requests.post(ENDPOINT + "tags/addTag?workspaceId=" + str(auto_reg[1]) + "&parentId=&name=" + random_data + "%%",
                  headers={"Authorization": "Bearer " + auto_reg[0]})
    req_update_tags = requests.post(ENDPOINT + "tags/getTags?workspaceId=" + str(auto_reg[1]) + "&parentId=&search=%%",
                                    headers={"Authorization": "Bearer " + auto_reg[0]}, json=[])
    asr_up = req_update_tags.json()["result"]
    Response(req_update_tags).assert_status_code(200).validate(Post)
    assert random_data + "%%" == asr_up[0]["name"]


def test_cyrillic_symbols_search(auto_reg, random_cyrillic_data):
    requests.post(ENDPOINT + "tags/addTag?workspaceId=" + str(auto_reg[1]) + "&parentId=&name=" + random_cyrillic_data,
                  headers={"Authorization": "Bearer " + auto_reg[0]})
    req_update_tags = requests.post(ENDPOINT + "tags/getTags?workspaceId=" + str(auto_reg[1]) + "&parentId=&search="
                                    + random_cyrillic_data, headers={"Authorization": "Bearer " + auto_reg[0]}, json=[])
    asr_up = req_update_tags.json()["result"]
    Response(req_update_tags).assert_status_code(200).validate(Post)
    assert asr_up[0]["name"] == random_cyrillic_data


def test_only_spaces_search(auto_reg, random_data):
    requests.post(ENDPOINT + "tags/addTag?workspaceId=" + str(auto_reg[1]) + "&parentId=&name=" + random_data,
                  headers={"Authorization": "Bearer " + auto_reg[0]})
    req_update_tags = requests.post(ENDPOINT + "tags/getTags?workspaceId=" + str(auto_reg[1]) + "&parentId=&search="
                                    + "%20%20%20%20%20%20", headers={"Authorization": "Bearer " + auto_reg[0]}, json=[])
    asr_up = req_update_tags.json()["result"]
    Response(req_update_tags).assert_status_code(200).validate(Post)
    assert len(asr_up) == 1
