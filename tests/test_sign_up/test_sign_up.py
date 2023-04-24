import pytest
import requests

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post, Negative


def test_sign_up(rand):
    sign_up = requests.post(ENDPOINT + "auth/exists", json={"Value": rand + "@gmail.com"})
    Response(sign_up).assert_status_code(200).validate(Post)


def test_sign_up_with_invalid_code(rand):
    requests.post(ENDPOINT + "auth/exists", json={"Value": rand + "@gmail.com"})
    code = requests.post(ENDPOINT + "auth/checkConfirmationCode?email=" + rand + "@gmail.com" + "&code=11111")
    Response(code).assert_status_code(200).validate(Post)
    assert code.json()["result"]["ok"] is False
    assert code.json()["result"]["token"] is None


@pytest.mark.skip(reason="There is no way to send requests to the date base")
def test_sign_up_with_valid_code(rand):
    requests.post(ENDPOINT + "auth/exists", json={"Value": rand + "@gmail.com"})
    code = requests.post(ENDPOINT + "auth/checkConfirmationCode?email=" + rand + "@gmail.com" + "&code=")
    Response(code).assert_status_code(200).validate(Post)
    assert code.json()["result"]["ok"] is True
    assert code.json()["result"]["token"] is not None


def test_sign_up_blank_email():
    sign_up = requests.post(ENDPOINT + "auth/exists", json={"Value": ""})
    Response(sign_up).assert_status_code(200).validate(Negative)
    assert sign_up.json()["errorMessage"] == "The value cannot be an empty string. (Parameter 'address')"


def test_sign_up_without_dog(rand):
    sign_up = requests.post(ENDPOINT + "auth/exists", json={"Value": rand})
    Response(sign_up).assert_status_code(200).validate(Negative)
    assert sign_up.json()["errorMessage"] == 'The specified string is not in the form required for an e-mail address.'


def test_sign_up_cyrillic():
    sign_up = requests.post(ENDPOINT + "auth/exists", json={"Value": "даник@gmail.com"})
    Response(sign_up).assert_status_code(200).validate(Negative)
    assert sign_up.json()["errorMessage"] == 'The client or server is only configured for E-mail addresses with ' \
                                             'ASCII local-parts: даник@gmail.com.'


def test_sign_up_two_dogs():
    sign_up = requests.post(ENDPOINT + "auth/exists", json={"Value": "da@da@gmail.com"})
    print(sign_up.json())
    Response(sign_up).assert_status_code(200).validate(Negative)
    assert sign_up.json()["errorMessage"] == "An invalid character was found in the mail header: '@'."


def test_sign_up_spaces(rand):
    sign_up = requests.post(ENDPOINT + "auth/exists", json={"Value": rand + "@gma il.com"})
    Response(sign_up).assert_status_code(200).validate(Negative)
    assert sign_up.json()["errorMessage"] == "The specified string is not in the form required for an e-mail address."


def test_sign_up_two_dogs():
    sign_up = requests.post(ENDPOINT + "auth/exists", json={"Value": "da@da@gmail.com"})
    print(sign_up.json())
    Response(sign_up).assert_status_code(200).validate(Negative)
    assert sign_up.json()["errorMessage"] == "An invalid character was found in the mail header: '@'."


def test_sign_up_upper_valid(rand):
    sign_up = requests.post(ENDPOINT + "auth/exists", json={"Value": rand.upper() + "@GMAIL.COM"})
    Response(sign_up).assert_status_code(200).validate(Post)


def test_sign_up_registered_email():
    sign_up = requests.post(ENDPOINT + "auth/exists", json={"Value": "m4tr1x1703@gmail.com"})
    Response(sign_up).assert_status_code(200).validate(Post)
    assert sign_up.json()["result"]["exists"] is True


def test_sign_up_upper_registered_email():
    sign_up = requests.post(ENDPOINT + "auth/exists", json={"Value": "M4TR1X1703@GMAIL.COM"})
    Response(sign_up).assert_status_code(200).validate(Post)
    assert sign_up.json()["result"]["exists"] is True

