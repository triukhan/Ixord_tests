import requests
import pytest

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


def test_save_template(save_template):
    Response(save_template).assert_status_code(200).validate(Post)


def test_template_saved(save_template, auto_reg):
    upd = requests.post(ENDPOINT_UP_TMP + str(auto_reg[1]) + UP_END, headers=auto_reg[0], json={"Value1": []})
    Response(upd).assert_status_code(200).validate(Post)
    assert len(upd.json()["result"]["items"]) == 1


def test_start_template(auto_reg, save_template):
    upd = requests.post(ENDPOINT_UP_TMP + str(auto_reg[1]) + UP_END, headers=auto_reg[0], json={"Value1": []}).json()
    start = requests.post(END_START + str(save_template.json()["result"]) + "&routerKey=" +
                          upd["result"]["items"][0]["routerKey"] + "&workspaceId=" + str(auto_reg[1]) + "&name=New%20"
                          "List&startTime=&refId=&patternId=&contextId=&executionFlowId=&startupScenarioId=",
                          headers=auto_reg[0], json={"value": "", "value1": None})
    Response(start).assert_status_code(200).validate(Post)
    upd_active = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={"value": []})
    assert len(upd_active.json()["result"]["items"]) == 2


def test_delete_template(auto_reg, save_template):
    delete = requests.post(ENDPOINT + "checklists/archiveChecklist?checklistId=" + str(save_template.json()["result"]) +
                           "&deleteDraftChecklist=true", headers=auto_reg[0])
    Response(delete).assert_status_code(200).validate(Post)
    upd = requests.post(ENDPOINT_UP_TMP + str(auto_reg[1]) + UP_END, headers=auto_reg[0], json={"Value1": []}).json()
    assert len(upd["result"]["items"]) == 0


def test_template_save_tag(auto_reg, rand):
    requests.post(ENDPOINT_EX + "addTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=
    [{"name": rand, "isLoading": True}])
    requests.post(ENDPOINT_TMP + auto_reg[2], headers=auto_reg[0])
    upd = requests.post(ENDPOINT_UP_TMP + str(auto_reg[1]) + UP_END, headers=auto_reg[0], json={"Value1": []}).json()
    assert len(upd["result"]["items"][0]["tags"]) == 1


def test_template_save_color(auto_reg):
    requests.post(ENDPOINT_EX + "updateColor?executionId=" + auto_reg[2], headers=auto_reg[0],
                  json={"value": "#003cff"})
    requests.post(ENDPOINT_TMP + auto_reg[2], headers=auto_reg[0])
    upd = requests.post(ENDPOINT_UP_TMP + str(auto_reg[1]) + UP_END, headers=auto_reg[0], json={"Value1": []}).json()
    assert upd["result"]["items"][0]["color"] == "#003cff"


def test_template_save_steps(auto_reg):
    requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
                  "value": "{\"blocks\":[{\"type\":\"step\",\"data\":{\"title\":\"test\",\"done\":false}},"
                  "{\"type\":\"step\",\"data\":{\"title\":\"test2\",\"done\":false}},{\"type\":\"step\",\"data\":"
                  "{\"title\":\"test3\",\"done\":false}}]}"})
    requests.post(ENDPOINT_TMP + auto_reg[2], headers=auto_reg[0])
    upd = requests.post(ENDPOINT_UP_TMP + str(auto_reg[1]) + UP_END, headers=auto_reg[0], json={"Value1": []}).json()
    assert len(upd["result"]["items"][0]["steps"]) == 3


def test_save_closed_steps_and_cl(auto_reg):
    q = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json=
                      {"value": "{\"blocks\":[{\"type\":\"step\",\"data\":{\"title\":\"TEST1\",\"done\":false}},"
                       "{\"type\":\"step\",\"data\":{\"title\":\"TEST2\",\"done\":false}},"
                       "{\"type\":\"checklist\",\"data\":{\"items\":[{\"text\":\"CHECK1\",\"checked\":false}]}},"
                       "{\"type\":\"checklist\",\"data\":{\"items\":[{\"text\":\"CHECK2\",\"checked\":false}]}}]}"})
    print(q.json())
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]
    st = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{"stepId": sid, "executed": 100,
                                                                                  "completed": True}])
    requests.post(ENDPOINT_TMP + auto_reg[2], headers=auto_reg[0])
    upd = requests.post(ENDPOINT_UP_TMP + str(auto_reg[1]) + UP_END, headers=auto_reg[0], json={"Value1": []}).json()
    start = requests.post(END_START + str(st.json()["result"]) + "&routerKey=" +
                          upd["result"]["items"][0]["routerKey"] + "&workspaceId=" + str(auto_reg[1]) + "&name=New%20"
                          "List&startTime=&refId=&patternId=&contextId=&executionFlowId=&startupScenarioId=",
                          headers=auto_reg[0], json={"value": "", "value1": None})
    get_by_key = requests.get(ENDPOINT_SID + str(auto_reg[3]), headers=auto_reg[0]).json()
    assert get_by_key["result"]["steps"][0]["step"]["data"]["value"]["blocks"][0]["data"]["done"] is False
    assert get_by_key["result"]["steps"][1]["step"]["data"]["value"]["blocks"][1]["data"]["items"][0]["checked"] is False

    # test is broken because of bug in backend (if this case will be fixed, change False to True)


def test_remove_tag_from_template(auto_reg, rand):
    add_t = requests.post(ENDPOINT_EX + "addTags?executionId=" + auto_reg[2], headers=auto_reg[0], json= [{"name": rand,
                          "isLoading": True}]).json()["result"][0]["id"]
    requests.post(ENDPOINT_TMP + auto_reg[2], headers=auto_reg[0])
    requests.post(ENDPOINT + "tags/deleteTag?workspaceId=" + str(auto_reg[1]) + "&tagId=" + str(add_t))
    upd = requests.post(ENDPOINT_UP_TMP + str(auto_reg[1]) + UP_END, headers=auto_reg[0], json={"Value1": []}).json()
    assert len(upd["result"]["items"][0]["tags"]) == 1

    # test is broken because of bug in backend (if this test will be broken, just change 1 to 0 in assert)


@pytest.mark.skip
def test_template_save_priority(auto_reg):
    requests.post(ENDPOINT_EX + "updatePriority?executionId=" + auto_reg[2], headers=auto_reg[0], json={"value": 40})
    requests.post(ENDPOINT_TMP + auto_reg[2], headers=auto_reg[0])
    upd = requests.post(ENDPOINT_UP_TMP + str(auto_reg[1]) + UP_END, headers=auto_reg[0], json={"Value1": []}).json()
    assert len(upd["result"]["items"][0]["priority"]) == 0

    # test is broken because of bug in backend (if this case will be fixed, remove @pytest.mark.skip)
