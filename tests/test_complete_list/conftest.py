import pytest
import requests

from configuration import *


@pytest.fixture()
def auto_reg():
    r_auto_test = requests.post(ENDPOINT + "auth/autoRegister")

    r_user_info = requests.get(ENDPOINT + "app/userInfo",
                               headers={"Authorization": "Bearer " + r_auto_test.json()['result']['token']})

    cre_lis = requests.post(ENDPOINT_LIST, headers={"Authorization": "Bearer " + r_auto_test.json()["result"]["token"]},
                            json={"name": "New Test List", "value": "{\"blocks\":[]}",
                                  "workspaceId": r_user_info.json()["result"]["roles"][0]["workspaceId"]})
    sid = requests.get(ENDPOINT_SID + cre_lis.json()["result"]["secureKey"], headers={"Authorization": "Bearer " +
                       r_auto_test.json()["result"]["token"]}).json()["result"]["steps"][0]["id"]
    requests.post(ENDPOINT_EXECUTE + cre_lis.json()["result"]["id"], headers={"Authorization": "Bearer " +
                  r_auto_test.json()["result"]["token"]}, json=[{"stepId": sid, "executed": 100, "dataPatch": [],
                                                                 "completed": True}])
    return [{"Authorization": "Bearer " + r_auto_test.json()["result"]["token"]},
            r_user_info.json()["result"]["roles"][0]["workspaceId"],
            cre_lis.json()["result"]["id"], cre_lis.json()["result"]["secureKey"]]
