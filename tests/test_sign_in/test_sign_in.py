import pytest
import requests

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post, Negative


@pytest.mark.skip(reason="There is no way to send requests to the database")
def test_sign_in_valid_data(reg):
    login = requests.post(ENDPOINT + "auth/login", json={"UserName": reg[0], "Password": reg[1]})
    Response(login).assert_status_code(200).validate(Post)
    assert login.json()["result"]["notAuth"] is False


def test_sign_in_invalid_data(rand):
    login = requests.post(ENDPOINT + "auth/login", json={"UserName": rand + "@email.com", "Password": rand})
    Response(login).assert_status_code(200).validate(Post)
    assert login.json()["result"]["notAuth"] is True


def test_sign_in_invalid_password(reg, rand):
    login = requests.post(ENDPOINT + "auth/login", json={"UserName": reg[0], "Password": rand})
    Response(login).assert_status_code(200).validate(Post)
    assert login.json()["result"]["notAuth"] is True


@pytest.mark.skip(reason="There is no way to send requests to the database")
def test_forgot_password_valid_email(reg):
    send_forgot = requests.post(ENDPOINT + "auth/sendForgotPasswordConfirmCode?email=" + reg[0])
    Response(send_forgot).assert_status_code(200).validate(Post)
    assert send_forgot.json()["result"]["ok"] is True


@pytest.mark.skip(reason="There is no way to send requests to the database AND we need valid code")
def test_forgot_password_valid_data(reg):
    requests.post(ENDPOINT + "auth/sendForgotPasswordConfirmCode?email=" + reg[0])
    code = requests.post(ENDPOINT + "auth/checkConfirmationCode?email=" + reg[0] + "&code=")
    Response(code).assert_status_code(200).validate(Post)
    assert code.json()["result"]["ok"] is True


def test_forgot_password_invalid_email(rand):
    wrong_email = requests.post(ENDPOINT + "auth/sendForgotPasswordConfirmCode?email=" + rand + "email.com")
    Response(wrong_email).assert_status_code(200).validate(Post)
    assert wrong_email.json()["result"]["ok"] is False


@pytest.mark.skip(reason="There is no way to send requests to the database")
def test_forgot_password_invalid_code(reg, rand):
    requests.post(ENDPOINT + "auth/sendForgotPasswordConfirmCode?email=" + reg[0])
    code = requests.post(ENDPOINT + "auth/checkConfirmationCode?email=" + reg[0] + "&code=" + rand)
    Response(code).assert_status_code(200).validate(Post)
    assert code.json()["result"]["ok"] is False


@pytest.mark.skip(reason="There is no way to send requests to the database")
def test_sign_in_email_case_sensitive(reg):
    login = requests.post(ENDPOINT + "auth/login", json={"UserName": reg[0].upper(), "Password": reg})
    Response(login).assert_status_code(200).validate(Post)
    assert login.json()["result"]["notAuth"] is False


@pytest.mark.skip(reason="There is no way to send requests to the database")
def test_sign_in_password_case_sensitive(reg):
    login = requests.post(ENDPOINT + "auth/login", json={"UserName": reg[0], "Password": reg.upper})
    Response(login).assert_status_code(200).validate(Post)
    assert login.json()["result"]["notAuth"] is True


@pytest.mark.skip(reason="There is no way to send requests to the database")
def test_sign_in_blank_password(reg):
    login = requests.post(ENDPOINT + "auth/login", json={"UserName": reg[0], "Password": ""})
    print(login.json())
    Response(login).assert_status_code(200).validate(Post)
    assert login.json()["result"]["notAuth"] is True


def test_sign_in_without_dog(rand):
    login = requests.post(ENDPOINT + "auth/login", json={"UserName": "danik_danik", "Password": rand})
    Response(login).assert_status_code(200).validate(Post)
    assert login.json()["result"]["notAuth"] is True