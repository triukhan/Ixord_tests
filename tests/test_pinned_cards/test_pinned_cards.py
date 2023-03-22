import requests

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


# def test_activate_removed_list_pinn(auto_reg, rand):
#     requests.post(ENDPOINT_EX + "cancelExecution?executionId=" + auto_reg[2], headers=auto_reg[0])
#     sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]
#     q = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{"stepId": sid, "executed": None,
#                     "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value": {"id": "dSduC49dAr",
#                                               "type": "paragraph", "data": {"text": "qqq"}}}]}])
#     print(q.json())
#     rl = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={}).json()
#     assert len(rl["result"]["items"]) == 1


def test_drd_pinned(auto_reg, rand):
    l = requests.post(ENDPOINT_LIST, headers=auto_reg[0], json={"name": rand, "value": "{\"blocks\":[]}", "workspaceId":
                  auto_reg[1]}).json()["result"]["id"]
    requests.post(ENDPOINT_EX + "pinExecution?executionId=" + l, headers=auto_reg[0])
    rp = requests.post(ENDPOINT_EXS + "updateReorder", headers=auto_reg[0],
                       json={"sortItems": [{"id": auto_reg[2], "newSort": 1}, {"id": l, "newSort": 0}]})
    Response(rp).assert_status_code(200).validate(Post)


def test_return_by_add_cl(auto_reg, rand):
    requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json=
                  {"value": "{\"blocks\":[{\"type\":\"step\",\"data\":{\"title\":\"123\",\"done\":false}},"
                            "{\"type\":\"step\",\"data\":{\"title\":\"456\",\"done\":false}}]}"})
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"]
    requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=
                  [{"stepId": sid[0]["id"], "executed": 100, "dataPatch": [], "completed": True}])
    q = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json= [{"stepId": sid[0]["id"],
                      "executed":0, "dataPatch":[{"op": "add", "path": "/value/blocks/0", "value": {
                       "type": "checklist", " data": {"items": [{"text": "sdf", "checked": False}]}}}]}])

    Response(q).assert_status_code(200).validate(Post)
    assert q.json()["result"][0]["percentCompletion"] == 0


def test_complete_pinned(auto_reg, rand):
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]
    requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{"stepId": sid, "executed": 100,
                                                                              "dataPatch": []}])
    rf = requests.post(ENDPOINT_EXS + "getPinnedExecutionsByTagIds?workspaceId=" + str(auto_reg[1])
                       + "&skip=0&count=100&respectToAdminRole=true&type=1", headers=auto_reg[0], json={})
    ra = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={}).json()["result"]
    Response(rf).assert_status_code(200).validate(Post)
    assert len(rf.json()["result"]["items"]) == 1
    assert len(ra["items"]) == 0
