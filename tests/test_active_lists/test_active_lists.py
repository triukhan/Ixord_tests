import requests

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


def test_update_color(auto_reg):
    uc = requests.post(ENDPOINT + "execution/updateColor?executionId=" + auto_reg[2], headers=auto_reg[0],
                       json={"value": "#cf08cf"})
    Response(uc).assert_status_code(200).validate(Post)
    assert uc.json()["result"] is True


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
    assert ode.json()["hasError"] is False


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
    gs = requests.get(ENDPOINT + "executions/getExecutionByKey?secureKey=" + auto_reg[3], headers=auto_reg[0])
    sid = gs.json()["result"]["steps"][0]["id"]
    ae = requests.post(ENDPOINT + "defaultExecuteExecution/executeSteps?executionId=" + auto_reg[2],
                       headers=auto_reg[0],
                       json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                           {"type": "paragraph", "data": {"text": rand}}}]}])

    ac = requests.post(ENDPOINT + "defaultExecuteExecution/executeSteps?executionId=" + auto_reg[2],
                       headers=auto_reg[0],
                       json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                           {"type": "checklist", "data": {"items": [{"text": rand, "checked": False}]}}}]}])

    ah = requests.post(ENDPOINT + "defaultExecuteExecution/executeSteps?executionId=" + auto_reg[2],
                       headers=auto_reg[0],
                       json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                           {"type": "header", "data": {"text": rand, "level": 2}}}]}])

    Response(ae).assert_status_code(200).validate(Post)
    assert ae.json()["hasError"] is False
    Response(ac).assert_status_code(200).validate(Post)
    assert ac.json()["hasError"] is False
    Response(ah).assert_status_code(200).validate(Post)
    assert ah.json()["hasError"] is False


def test_add_sublist_table_image(auto_reg, rand):
    gs = requests.get(ENDPOINT + "executions/getExecutionByKey?secureKey=" + auto_reg[3], headers=auto_reg[0])
    sid = gs.json()["result"]["steps"][0]["id"]
    asb = requests.post(ENDPOINT + "defaultExecuteExecution/executeSteps?executionId=" + auto_reg[2],
                        headers=auto_reg[0],
                        json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                            {"type": "list", "data": {"style": "ordered", "items": ["Hi, ", rand]}}}]}])

    ast = requests.post(ENDPOINT + "defaultExecuteExecution/executeSteps?executionId=" + auto_reg[2],
                        headers=auto_reg[0],
                        json=[{"stepId": sid, "dataPatch": [{"op": "add", "path": "/value/blocks/0", "value":
                            {"type": "table", "data": {"withHeadings": False, "content": []}}}]}])

    asi = requests.post(ENDPOINT + "defaultExecuteExecution/executeSteps?executionId=" + auto_reg[2],
                        headers=auto_reg[0],
                        json=[{"stepId": sid, "dataPatch":
                              [{"op": "add", "path": "/value/blocks/0", "value": {"type": "image", "data": {"file": {
                               "url": "images/ChecklistImages/64108fe5c93111cad1cfa7c8/content/"
                                "harry-potter-and-the-goblet-of-fire-yule-ball_f195ab05056f4c54be7b8049bf6b429c.webp",
                                "title": "hp"}}}}]}])
    Response(asb).assert_status_code(200).validate(Post)
    assert asb.json()["hasError"] is False
    Response(ast).assert_status_code(200).validate(Post)
    assert ast.json()["hasError"] is False
    Response(asi).assert_status_code(200).validate(Post)
    assert asi.json()["hasError"] is False
