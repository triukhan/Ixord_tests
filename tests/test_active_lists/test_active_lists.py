import requests

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


def test_update_color_and_clear_color(auto_reg):
    uc = requests.post(ENDPOINT + "execution/updateColor?executionId=" + auto_reg[2], headers=auto_reg[0],
                       json={"value": "#cf08cf"})
    cc = requests.post(ENDPOINT + "execution/updateColor?executionId=" + auto_reg[2], headers=auto_reg[0],
                       json={"value": None})
    Response(uc).assert_status_code(200).validate(Post)
    assert uc.json()["result"] is True
    Response(cc).assert_status_code(200).validate(Post)
    assert cc.json()["result"] is True


def test_delete_list(auto_reg):
    dl = requests.post(ENDPOINT + "execution/cancelExecution?executionId=" + auto_reg[2], headers=auto_reg[0])
    Response(dl).assert_status_code(200).validate(Post)
    assert dl.json()["result"] is True


def test_save_template(auto_reg):
    st = requests.post(ENDPOINT + "execution/saveAsChecklist?executionId=" + auto_reg[2], headers=auto_reg[0])
    Response(st).assert_status_code(200).validate(Post)
    assert type(st.json()["result"]) is int


def test_open_edit_list(auto_reg):
    ode = requests.get(ENDPOINT + "executions/getExecutionByKey?secureKey=" + auto_reg[3], headers=auto_reg[0])
    Response(ode).assert_status_code(200).validate(Post)


def test_drag_and_drop(auto_reg):
    cre_lis = requests.post(ENDPOINT_LIST, headers=auto_reg[0], json={"name": "New Test List",
                                                                      "value": "{\"blocks\":[]}",
                                                                      "workspaceId": auto_reg[1]})
    dad = requests.post(ENDPOINT + "executions/updateReorder", headers=auto_reg[0],
                        json={"sortItems": [{"id": cre_lis.json()["result"]["id"], "newSort": 0},
                                            {"id": auto_reg[2], "newSort": 1}]})
    Response(dad).assert_status_code(200).validate(Post)
    assert dad.json()["result"] is True


def test_add_text_cl_header(auto_reg, rand):
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]
    ae = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0],
                       json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                             {"type": "paragraph", "data": {"text": rand}}}]}])

    ac = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0],
                       json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                             {"type": "checklist", "data": {"items": [{"text": rand, "checked": False}]}}}]}])

    ah = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0],
                       json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                             {"type": "header", "data": {"text": rand, "level": 2}}}]}])

    Response(ae).assert_status_code(200).validate(Post)
    Response(ac).assert_status_code(200).validate(Post)
    Response(ah).assert_status_code(200).validate(Post)


def test_add_sublist_table_image(auto_reg, rand):
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]
    asb = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0],
                        json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                              {"type": "list", "data": {"style": "ordered", "items": ["Hi, ", rand]}}}]}])

    ast = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0],
                        json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                              {"type": "table", "data": {"withHeadings": False, "content": []}}}]}])

    asi = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{"stepId": sid, "dataPatch":
                        [{"op": "add", "path": "/value/blocks/0", "value": {"type": "image", "data": {"file": {
                         "url": "images/ChecklistImages/64108fe5c93111cad1cfa7c8/content/"
                         "harry-potter-and-the-goblet-of-fire-yule-ball_f195ab05056f4c54be7b8049bf6b429c.webp",
                         "title": "hp"}}}}]}])
    Response(asb).assert_status_code(200).validate(Post)
    Response(ast).assert_status_code(200).validate(Post)
    Response(asi).assert_status_code(200).validate(Post)


def test_add_file(auto_reg, rand):
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]
    url = "images/ChecklistImages/6411ba11ce2108919ea8480c/content/0-6600_034e101a32fe4eae8a6eaca7f6e1b90e.pdf"
    af = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0],
                       json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                           {"type": "attaches", "data": {"file": {"url": url}}}}]}])
    Response(af).assert_status_code(200).validate(Post)


def test_complete_by_done(auto_reg):
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]
    cl = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0],
                       json=[{"stepId": sid, "executed": 100, "dataPatch": [], "completed": True}])
    Response(cl).assert_status_code(200).validate(Post)


def test_drd__list_elements(auto_reg, rand):
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]

    requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0],
                  json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                             {"type": "checklist", "data": {"items": [{"text": "checklist", "checked": False}]}}}]}])
    requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0],
                  json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/1", "value":
                             {"type": "paragraph", "data": {"text": "text"}}}]}])

    drd = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[
                {"stepId": sid, "dataPatch": [{"op": "remove", "path": "/value/blocks/1/data/text"},
                    {"op": "add", "path": "/value/blocks/1/data/items", "value":
                        [{"text": "checklist", "checked": False}]},
                    {"op": "replace", "path": "/value/blocks/1/type", "value": "checklist"},
                    {"op": "remove", "path": "/value/blocks/0/data/items"},
                    {"op": "replace", "path": "/value/blocks/0/type", "value": "paragraph"},
                    {"op": "add", "path": "/value/blocks/0/data/text", "value": "text"}]}])
    Response(drd).assert_status_code(200).validate(Post)


def test_delete_element(auto_reg, rand):
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]

    requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{"stepId": sid, "dataPatch":
                  [{"op": "add", "path": "/value/blocks/0", "value": {"type": "paragraph", "data": {"text": "text"}}}]}])
    de = requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{"stepId": sid, "dataPatch":
                       [{"op": "remove", "path": "/value/blocks/0"}]}])
    Response(de).assert_status_code(200).validate(Post)


def test_delete_tag_check_card(auto_reg, rand):
    ct = str(requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand,
                           headers=auto_reg[0]).json()["result"]["id"])
    requests.post(ENDPOINT + "execution/addTags?executionId=" + auto_reg[2], headers=auto_reg[0], json=[{"id": ct}])
    t = requests.post(ENDPOINT + "tags/deleteTag?workspaceId=" + str(auto_reg[1]) + "&tagId=" + ct, headers=auto_reg[0])
    Response(t).assert_status_code(200).validate(Post)


def test_refresh_cards(auto_reg):
    rc = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={})
    Response(rc).assert_status_code(200).validate(Post)
    assert auto_reg[2] == rc.json()["result"]["items"][0]["id"]


def test_done_cards(auto_reg):
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]
    requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{"stepId": sid, "executed": 100,
                                                                              "completed": True}])
    rc = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={})
    Response(rc).assert_status_code(200).validate(Post)
    assert len(rc.json()["result"]["items"]) == 0


def test_complete_checkboxes(auto_reg, rand):
    sid = requests.get(ENDPOINT_SID + auto_reg[3], headers=auto_reg[0]).json()["result"]["steps"][0]["id"]
    requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{"stepId": sid, "dataPatch":
                  [{"op": "add", "path": "/value/blocks/0", "value": {"type": "checklist", "data":
                    {"items": [{"text": rand, "checked": True}]}}}]}])
    requests.post(ENDPOINT_EXECUTE + auto_reg[2], headers=auto_reg[0], json=[{"stepId": sid, "executed": 100,
                  "dataPatch": [{"op": "replace", "path": "/value/blocks/0/data/items/0/checked", "value": True}]}])
    rc = requests.post(ENDPOINT_REFRESH + str(auto_reg[1]) + REFRESH, headers=auto_reg[0], json={})
    Response(rc).assert_status_code(200).validate(Post)
    assert len(rc.json()["result"]["items"]) == 0


def test_pin_card(auto_reg):
    requests.post(ENDPOINT + "execution/pinExecution?executionId=" + auto_reg[2], headers=auto_reg[0])
    rp = requests.post(ENDPOINT + "executions/getPinnedExecutionsByTagIds?workspaceId=" + str(auto_reg[1]) +
                       "&skip=0&count=100&respectToAdminRole=true&type=1", headers=auto_reg[0], json={})
    Response(rp).assert_status_code(200).validate(Post)
    assert len(rp.json()["result"]["items"]) == 1
