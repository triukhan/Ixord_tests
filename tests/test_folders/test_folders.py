import requests

from configuration import ENDPOINT
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


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
    print(auto_reg[1])
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

