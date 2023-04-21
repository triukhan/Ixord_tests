import requests
import pytest

from configuration import *
from src.baseclasses.response import Response
from src.pydantic_schemas.ix_classes import Post, Negative
from sqlalchemy import create_engine


def test_name_space(rand):
    n = requests.put(ENDPOINT_PRF + "setPersonalInfo", headers=PRF_TOKEN, json={"id": 763, "displayName": rand + "  q"})
    Response(n).assert_status_code(200).validate(Post)


def test_name_cyrillic_special():
    n = requests.put(ENDPOINT_PRF + "setPersonalInfo", headers=PRF_TOKEN, json={"id": 763, "displayName":
                                                                                "ШАЛОМ№;№;*?!%:()"})
    Response(n).assert_status_code(200).validate(Post)


def test_existing_email():
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=m4tr1x1703@gmail.com", headers=PRF_TOKEN)
    Response(e).assert_status_code(200).validate(Negative)
    assert e.json()["errorMessage"] == 'Item already exists () => value(excord.Services.UserService+<>c__' \
                                       'DisplayClass17_0).email, [() => value(excord.Services.UserService+<>c__' \
                                       'DisplayClass17_0).email=m4tr1x1703@gmail.com]'


def test_blank_email():
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=", headers=PRF_TOKEN)
    Response(e).assert_status_code(200).validate(Negative)
    assert e.json()["errorMessage"] == 'Item already exists () => value(excord.Services.UserService+<>c__' \
                                       'DisplayClass17_0).email, [() => value(excord.Services.UserService+<>c__' \
                                       'DisplayClass17_0).email=]'


def test_email_dot_tire(rand):
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=" + rand + "-da.da_da@gmail.com",
                      headers=PRF_TOKEN)
    Response(e).assert_status_code(200).validate(Post)


def test_email_special():
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=da%$#-_-da@gmail.com", headers=PRF_TOKEN)
    print(e.json())
    Response(e).assert_status_code(200).validate(Negative)
    assert e.json()["errorMessage"] == ERR_EMAIL


def test_valide_email(rand):
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=" + rand + "@gmail.com", headers=PRF_TOKEN)
    Response(e).assert_status_code(200).validate(Post)


def test_email_spaces(rand):
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=" + rand + "@GMAIL.COM", headers=PRF_TOKEN)
    Response(e).assert_status_code(200).validate(Post)


def test_email_without_dog():
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=danil$gmail.com", headers=PRF_TOKEN)
    Response(e).assert_status_code(200).validate(Negative)
    assert e.json()["errorMessage"] == ERR_EMAIL


def test_email_without_dog(rand):
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=" + rand + " gmail.com", headers=PRF_TOKEN)
    print(e.json())
    Response(e).assert_status_code(200).validate(Negative)
    assert e.json()["errorMessage"] == ERR_EMAIL


def test_email_cyrillic():
    e = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=ванек@gmail.com", headers=PRF_TOKEN)
    Response(e).assert_status_code(200).validate(Negative)
    assert e.json()["errorMessage"] == 'The client or server is only configured for E-mail addresses with ASCII ' \
                                       'local-parts: ванек@gmail.com.'


# @pytest.mark.parametrize('first_value, response',  [
#     ("ванек@gmail.com", "The client or server is only configured for E-mail addresses with ASCII "
#      "local-parts: ванек@gmail.com."), ("danil$gmail.com", "The specified string is not in the form required for "
#                                                            "an e-mail address.")
# ])
# def test_smth(first_value, response, email_request):
#     Response(email_request(first_value)).assert_status_code(200).validate(Negative)
#     assert email_request(first_value).json()["errorMessage"] == response


def test_reset_password(rand):
    p = requests.post(ENDPOINT_PRF + "resetPassword?newPassword=" + rand, headers=PRF_TOKEN)
    Response(p).assert_status_code(200).validate(Post)


def test_password_blank():
    p = requests.post(ENDPOINT_PRF + "resetPassword?newPassword=", headers=PRF_TOKEN)
    Response(p).assert_status_code(200).validate(Negative)
    assert p.json()["errorMessage"] == "Value cannot be null. (Parameter 'newPassword')"


def test_password_same(rand):
    requests.post(ENDPOINT_PRF + "resetPassword?newPassword=" + rand, headers=PRF_TOKEN)
    p = requests.post(ENDPOINT_PRF + "resetPassword?newPassword=" + rand, headers=PRF_TOKEN)
    Response(p).assert_status_code(200).validate(Post)


def test_password_numbers_special(rand):
    p = requests.post(ENDPOINT_PRF + "resetPassword?newPassword=324540$#@!%^" + rand, headers=PRF_TOKEN)
    Response(p).assert_status_code(200).validate(Post)


# def test_signup_profile_page(auto_reg, rand):
#     requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=" + rand + "@gmail.com", headers=auto_reg[0])
#     engine = create_engine("Initial Catalog=excord;Data Source=WORK02\\SQLEXPRESS;Integrated Security=SSPI;"
#                            "MultipleActiveResultSets=true;TrustServerCertificate=True")
#     connection = engine.connect()
#     result = connection.execute("SELECT * FROM ")
#     connection.close()


def test_signup_ex_email_profile_page(auto_reg):
    ex = requests.post(ENDPOINT_PRF + "sendConfirmationCodeToNewEmail?email=m4tr1x1703@gmail.com", headers=auto_reg[0])
    Response(ex).assert_status_code(200).validate(Negative)
    assert ex.json()["errorMessage"] == 'Item already exists () => value(excord.Services.UserService+<>c__DisplayClas' \
           's17_0).email, [() => value(excord.Services.UserService+<>c__DisplayClass17_0).email=m4tr1x1703@gmail.com]'


def test_name_unregistered_profile_page(auto_reg, rand):
    uid = requests.get(ENDPOINT + "app/userInfo", headers=auto_reg[0]).json()["result"]["userId"]
    an = requests.put(ENDPOINT_PRF + "setPersonalInfo", headers=auto_reg[0], json={"id": uid, "displayName": rand})
    Response(an).assert_status_code(200).validate(Post)
    uid2 = requests.get(ENDPOINT + "app/userInfo", headers=auto_reg[0]).json()["result"]["displayName"]
    assert uid2 == rand