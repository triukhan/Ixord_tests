import requests

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


def test_refresh_completed(auto_reg):
    rf = requests.post(ENDPOINT_EXS + "getExecutionsByTagIds?status=9&workspaceId=" + str(auto_reg[1]) + REFRESH,
                       headers=auto_reg[0], json={"value": []})
    Response(rf).assert_status_code(200).validate(Post)
    assert len(rf.json()["result"]["items"]) == 1


def test_activate_list_add_step(auto_reg):
    requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json=
                  {"value": "{\"blocks\":[{\"type\":\"step\",\"data\":{\"title\":\"Step\",\"done\":false}}]}"})
    rf = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={"value": []})
    Response(rf).assert_status_code(200).validate(Post)
    assert len(rf.json()["result"]["items"]) == 1


def test_activate_list_add_cl(auto_reg):
    requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={"value": "{\"bl"
                  "ocks\":[{\"type\":\"checklist\",\"data\":{\"items\":[{\"text\":\"check\",\"checked\":false}]}}]}"})
    rf = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={"value": []})
    Response(rf).assert_status_code(200).validate(Post)
    assert len(rf.json()["result"]["items"]) == 1


def test_delete_teg_complete(auto_reg, rand):
    requests.post(ENDPOINT_EX + "addTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=[{"name": rand,
                                                                                                  "isLoading": True}])
    sir = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["tags"]
    assert len(sir) == 1
    requests.post(ENDPOINT + "tags/deleteTag?workspaceId=" + str(auto_reg[1]) + "&tagId=" + str(sir[0]["id"]), headers=
                  auto_reg[0])
    fir = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["tags"]
    assert len(fir) == 0
