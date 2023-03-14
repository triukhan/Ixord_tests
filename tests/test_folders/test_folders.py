import requests

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post
from src.enums.global_enums import *


def test_create_folder(auto_reg, rand):
    cr = requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand, headers=auto_reg[0])
    Response(cr).assert_status_code(200).validate(Post)
    asr_cf = cr.json()["result"]
    assert type(asr_cf["id"]) is int


def test_update_folder(auto_reg, rand):
    cr = requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand, headers=auto_reg[0])
    asr_cf = cr.json()["result"]

    ut = requests.post(ENDPOINT_GTAG + str(auto_reg[1]) + "&parentId=&search=", headers=auto_reg[0], json=[])
    Response(ut).assert_status_code(200).validate(Post)
    asr_ut = ut.json()["result"][0]
    assert asr_cf["id"] == asr_ut["id"], asr_cf["name"] == asr_ut["name"]


def test_search_tag(auto_reg, rand):
    tags = [rand, "test_folder", "ball"]
    for tag in tags:
        requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + tag, headers=auto_reg[0])

    st = requests.post(ENDPOINT_GTAG + str(auto_reg[1]) + "&parentId=&search=" + rand, headers=auto_reg[0], json=[])
    Response(st).assert_status_code(200).validate(Post)
    asr_st = st.json()["result"]
    assert len(asr_st) == 1, GlobalErrorMessages.WRONG_NUMBER_OF_ELEMENTS
    assert asr_st[0]["name"] == rand


def test_trim_search_tag(auto_reg, rand):
    requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand, headers=auto_reg[0])
    ut = requests.post(ENDPOINT_GTAG + str(auto_reg[1]) + "&parentId=&search=" + rand[7:], headers=auto_reg[0], json=[])

    Response(ut).assert_status_code(200).validate(Post)
    asr_up = ut.json()["result"]
    assert rand == asr_up[0]["name"]


def test_spaces_search(auto_reg, rand):
    requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand + " book", headers=auto_reg[0])
    ut = requests.post(ENDPOINT_GTAG + str(auto_reg[1]) + "&parentId=&search=" + rand + " book", headers=auto_reg[0], json=[])

    asr_up = ut.json()["result"]
    Response(ut).assert_status_code(200).validate(Post)
    assert rand + " book" == asr_up[0]["name"]


def test_special_symbols_search(auto_reg, rand):
    requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand + "%%", headers=auto_reg[0])
    ut = requests.post(ENDPOINT_GTAG + str(auto_reg[1]) + "&parentId=&search=%%", headers=auto_reg[0], json=[])

    asr_up = ut.json()["result"]
    Response(ut).assert_status_code(200).validate(Post)
    assert rand + "%%" == asr_up[0]["name"]


def test_cyrillic_symbols_search(auto_reg, random_cyrillic_data):
    requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + random_cyrillic_data, headers=auto_reg[0])
    ut = requests.post(ENDPOINT_GTAG + str(auto_reg[1]) + "&parentId=&search=" + random_cyrillic_data, headers=auto_reg[0], json=[])

    asr_up = ut.json()["result"]
    Response(ut).assert_status_code(200).validate(Post)
    assert asr_up[0]["name"] == random_cyrillic_data


def test_only_spaces_search(auto_reg, rand):
    requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand, headers=auto_reg[0])
    ut = requests.post(ENDPOINT_GTAG + str(auto_reg[1]) + "&parentId=&search=%20%20%20%20%20%20", headers=auto_reg[0], json=[])

    asr_oss = ut.json()["result"]
    Response(ut).assert_status_code(200).validate(Post)
    assert len(asr_oss) == 1


def test_rename_tag(auto_reg, rand):
    cr = requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand, headers=auto_reg[0])
    rt = requests.post(ENDPOINT + "tags/saveTag?workspaceId=" + str(auto_reg[1]), headers=auto_reg[0],
                       json={"id": cr.json()["result"]["id"], "name": "привет_дружок!"})
    Response(rt).assert_status_code(200).validate(Post)
    assert rt.json()["result"] == True


def test_add_subtag(auto_reg, rand):
    cr = requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand, headers=auto_reg[0])
    r_sg = requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=" + str(cr.json()["result"]["id"])
                         + "&name=new_name", headers=auto_reg[0])
    asr_sg = r_sg.json()["result"]
    Response(r_sg).assert_status_code(200).validate(Post)
    assert asr_sg["parentIds"] == [cr.json()["result"]["id"]]


def test_delete_tag(auto_reg, rand):
    cr = requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand, headers=auto_reg[0])
    r_dt = requests.post(ENDPOINT + "tags/deleteTag?workspaceId=" + str(auto_reg[1]) + "&tagId="
                         + str(cr.json()["result"]["id"]), headers=auto_reg[0])
    asr_sg = r_dt.json()
    Response(r_dt).assert_status_code(200).validate(Post)
    assert asr_sg["result"] == True


def test_add_tag_more_than_25(auto_reg):
    cr = requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + "%ХАХВА!.'asd", headers=auto_reg[0])
    asr_cr = cr.json()["result"]
    Response(cr).assert_status_code(200).validate(Post)
    assert asr_cr["name"] == "%ХАХВА!.'asd"


def test_go_to_tag_page(auto_reg, rand):
    cr = requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand,
                       headers=auto_reg[0])
    requests.post(ENDPOINT + "executions/runOnce", headers=auto_reg[0],
                  json={"value": "{\"blocks\":[]}", "tagIds": [cr.json()["result"]["id"]]})
    gt = requests.post(ENDPOINT + "executions/getExecutionsByTagIds?status=2&workspaceId=" + str(auto_reg[1])
                       + "&skip=0&count=100&showOnlyUsersExecutions=false&respectToAdminRole=true&type=1&sortBy" +
                       "Modif=false&respectToSort=true",
                       headers=auto_reg[0], json={"value": [cr.json()["result"]["id"]]})
    Response(gt).assert_status_code(200).validate(Post)
    assert gt.json()["result"]["totalItems"] == 1


def test_search_subtag(auto_reg, rand):
    cr = requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=&name=" + rand,
                       headers=auto_reg[0])
    requests.post(ENDPOINT_TAG + str(auto_reg[1]) + "&parentId=" + str(cr.json()["result"]["id"]) + "&name=sub"
                  + rand, headers=auto_reg[0])
    sr = requests.post(ENDPOINT_GTAG + str(auto_reg[1]) + "&parentId=&search=sub",
                       headers=auto_reg[0], json=[])
    asr_ss = sr.json()["result"]
    Response(sr).assert_status_code(200).validate(Post)
    assert len(asr_ss) == 1
