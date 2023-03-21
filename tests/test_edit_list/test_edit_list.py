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
                  [{"id": tid, "workspaceId": auto_reg[1], "name": rand}])
    dt = requests.post(ENDPOINT_EX + "removeTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=
                       [{"id": tid}])
    Response(dt).assert_status_code(200).validate(Post)
    assert dt.json()["result"][0]["name"] == rand


def test_add_text_edit_list(auto_reg):
    at = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
                       "value": "{\"blocks\":[{\"type\":\"paragraph\",\"data\":{\"text\":\"some_text\"}}]}"})
    Response(at).assert_status_code(200).validate(Post)


def test_add_cl_edit_list(auto_reg):
    acl = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
     "value": "{\"blocks\":[{\"type\":\"checklist\",\"data\":{\"items\":[{\"text\":\"123\",\"checked\":false}]}}]}"})
    Response(acl).assert_status_code(200).validate(Post)


def test_add_step_edit_list(auto_reg):
    ast = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
                        "value": "{\"blocks\":[{\"type\":\"step\",\"data\":{\"title\":\"123\",\"done\":false}}]}"})
    Response(ast).assert_status_code(200).validate(Post)


def test_add_heading_edit_list(auto_reg):
    ah = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
                       "value": "{\"blocks\":[{\"type\":\"header\",\"data\":{\"text\":\"123\",\"level\":2}}]}"})
    Response(ah).assert_status_code(200).validate(Post)


def test_add_sublist_edit_list(auto_reg):
    asl = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
         "value": "{\"blocks\":[{\"type\":\"list\",\"data\":{\"style\":\"ordered\",\"items\":[\"1\",\"2\",\"3\"]}}]}"})
    Response(asl).assert_status_code(200).validate(Post)


def test_add_table_edit_list(auto_reg):
    at = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
                       "value": "{\"blocks\":[{\"type\":\"table\",\"data\":{\"withHeadings\":false,\"content\":[]}}]}"})
    Response(at).assert_status_code(200).validate(Post)


def test_add_image_edit_list(auto_reg):
    ai = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
        "value": "{\"blocks\":[{\"type\":\"image\",\"data\":{\"file\":{\"url\":\"images/ChecklistImages/64187b0e0029ba"
        "ebb1f21475/content/Pikachu-SVG-File-Free_2cca3351acf74ff99350b1017940a597.png\",\"title\":\"Pika\"}}}]}"})
    Response(ai).assert_status_code(200).validate(Post)


def test_add_file_edit_list(auto_reg):
    ai = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
        "value": "{\"blocks\":[{\"type\":\"attaches\",\"data\":{\"file\":{\"url\":\"images/ChecklistImages/64187b0e0029"
        "baebb1f21475/content/Pikachu-SVG-File-Free_0d08c7a9430b490e8f6259ccfb9311f8.png\",\"title\":\"Pika\"},"
                 "\"title\":\"Pika\"}}]}"})
    Response(ai).assert_status_code(200).validate(Post)


def test_add_all_elements_together(auto_reg):
    add_all = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0],
                            json=ALL_ELEMENTS)
    Response(add_all).assert_status_code(200).validate(Post)


def test_add_new_tag_edit_list(auto_reg, rand):
    at = requests.post(ENDPOINT_EX + "addTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=
                       [{"name": rand, "isLoading": True}])
    Response(at).assert_status_code(200).validate(Post)
    assert at.json()["result"][0]["name"] == rand


def test_add_5_existing_folders_edit_list(auto_reg):
    tg = []
    tags = ["1", "2", "3", "4", "5"]
    for tag in tags:
        tg.append(requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + tag,
                                headers=auto_reg[0]).json()["result"]["id"])
    for i in tg:
        requests.post(ENDPOINT_EX + "addTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=[{"id": i}])
    gt = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()
    assert len(gt["result"]["tags"]) == 5


def test_add_tag_with_spaces_edit_list(auto_reg):
    at = requests.post(ENDPOINT_EX + "addTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=
                       [{"name": "q q", "isLoading": True}])
    Response(at).assert_status_code(200).validate(Post)
    assert at.json()["result"][0]["name"] == "q q"


def test_complete_list_by_cl_edit_list(auto_reg):
    requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
     "value": "{\"blocks\":[{\"type\":\"checklist\",\"data\":{\"items\":[{\"text\":\"123\",\"checked\":true}]}}]}"})
    rl = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={}).json()
    assert len(rl["result"]["items"]) == 0


def test_add_29mb_file_edit_list(auto_reg):
    ai = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
        "value": "{\"blocks\":[{\"type\":\"attaches\",\"data\":{\"file\":{\"url\":\"images/ChecklistImages/64187b0e0029"
        "images/ChecklistImages/64186f053f3bf5cec5c134a9/content/1 (5)_1edc013765a84c9088957df309bc9f68.\",\"title\":"
                 "\"Pika\"},\"title\":\"Pika\"}}]}"})
    Response(ai).assert_status_code(200).validate(Post)


def test_different_image_formats(auto_reg):
    ai = requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json=IMAGES)
    Response(ai).assert_status_code(200).validate(Post)


def test_integration_edit_lists_and_card(auto_reg):
    requests.post(ENDPOINT_EXS + "updateRunOnce?executionId=" + auto_reg[2], headers=auto_reg[0], json={
         "value": "{\"blocks\":[{\"type\":\"step\",\"data\":{\"title\":\"123\",\"done\":false}},"
                  "{\"type\":\"step\",\"data\":{\"title\":\"456\",\"done\":false}}]}"})
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"]
    requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{
        "stepId": sid[0]["id"], "executed": 100, "completed": True}])
    requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{
        "stepId": sid[1]["id"], "executed": 100, "completed": True}])
    rl = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={}).json()
    assert len(rl["result"]["items"]) == 0
