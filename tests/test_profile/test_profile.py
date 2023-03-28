import requests

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post


def test_name_space(rand):
    n = requests.put(ENDPOINT_PRF + "setPersonalInfo", headers=PRF_TOKEN, json={"id": 763, "displayName": rand + "  q"})
    Response(n).assert_status_code(200).validate(Post)


def test_name_cyrillic_special():
    n = requests.put(ENDPOINT_PRF + "setPersonalInfo", headers=PRF_TOKEN, json={"id": 763, "displayName":
                                                                                "ШАЛОМ№;№;*?!%:()"})
    Response(n).assert_status_code(200).validate(Post)


def test_existing_email():
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=m4tr1x1703@gmail.com", headers=PRF_TOKEN)
    assert e.json()["errorMessage"] == 'Item already exists () => value(excord.Services.UserService+<>c__' \
                                       'DisplayClass17_0).email, [() => value(excord.Services.UserService+<>c__' \
                                       'DisplayClass17_0).email=m4tr1x1703@gmail.com]'
    assert e.json()["hasError"] is True


def test_blank_email():
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=", headers=PRF_TOKEN)
    assert e.json()["errorMessage"] == 'Item already exists () => value(excord.Services.UserService+<>c__' \
                                       'DisplayClass17_0).email, [() => value(excord.Services.UserService+<>c__' \
                                       'DisplayClass17_0).email=]'
    assert e.json()["hasError"] is True


def test_valide_email(rand):
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=" + rand + "@gmail.com", headers=PRF_TOKEN)
    Response(e).assert_status_code(200).validate(Post)


def test_email_spaces(rand):
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=" + rand + "@GMAIL.COM", headers=PRF_TOKEN)
    Response(e).assert_status_code(200).validate(Post)


def test_email_without_dog():
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=danil$gmail.com", headers=PRF_TOKEN)
    assert e.json()["hasError"] is True
    assert e.json()["errorMessage"] == "The specified string is not in the form required for an e-mail address."


def test_email_cyrillic():
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=ванек@gmail.com", headers=PRF_TOKEN)
    assert e.json()["hasError"] is True
    assert e.json()["errorMessage"] == 'The client or server is only configured for E-mail addresses with ASCII ' \
                                       'local-parts: ванек@gmail.com.'