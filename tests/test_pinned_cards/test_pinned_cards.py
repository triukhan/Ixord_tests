import requests

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


# def test_activate_removed_list_pinn(auto_reg, rand):
#     requests.post(ENDPOINT_EX + "cancelExecution?executionId=" + auto_reg[2], headers=auto_reg[0])
#     sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]
#     q = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{"stepId": sid, "dataPatch":
#                   [{"op": "add", "path": "/value/blocks/0", "value": {"type": "checklist", "data":
#                     {"items": [{"text": rand, "checked": False}]}}}]}])
#     print(q.json())
#     rl = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={}).json()
#     assert len(rl["result"]["items"]) == 1