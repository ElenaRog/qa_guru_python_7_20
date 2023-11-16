import json
import allure
import jsonschema

from allure_commons.types import AttachmentType
from requests import sessions
from curlify import to_curl

from utils import load_schema


def reqres_api(method, url, **kwargs):
    args = kwargs
    base_url = "https://reqres.in"
    new_url = base_url + url
    method = method.upper()
    with allure.step(f'Отправляем {method} запрос на reqres.in{url}. Параметры: {args if len(args) != 0 else "отсутствуют"}'):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)
            allure.attach(
                body=message.encode("utf8"),
                name="Curl",
                attachment_type=AttachmentType.TEXT,
                extension='txt')
            try:
                allure.attach(
                    body=json.dumps(
                        response.json(),
                        indent=4
                    ).encode("utf8"),
                    name="Json",
                    attachment_type=AttachmentType.JSON, extension='json')
            except:
                pass
    return response


def test_get_status_code_is_ok():
    response = reqres_api('get', '/api/users')

    assert response.status_code == 200


def test_get_user_is_found():
    schema = load_schema('get_user.json')

    user_id = 2
    response = reqres_api(
        'get',
        f'/api/users/{user_id}'
    )

    assert response.json()["data"]["id"] == user_id
    jsonschema.validate(response.json(), schema)


def test_get_user_is_not_found():
    response = reqres_api(
        'get',
        '/api/users/23'
    )

    assert response.status_code == 404


def test_post_create_user():
    schema = load_schema('post_user.json')

    response = reqres_api(
        'post',
        '/api/users',
        json={
            "name": "elena",
            "job": "QA"
        }
    )

    assert response.status_code == 201
    assert response.json()['name'] == "elena"
    jsonschema.validate(response.json(), schema)


def test_put_update_user():
    schema = load_schema('put_user.json')

    response = reqres_api(
        'put',
        '/api/users/2',
        json={
            "name": "morpheus",
            "job": "actor"
        }
    )

    assert response.status_code == 200
    assert response.json()['job'] == "actor"
    jsonschema.validate(response.json(), schema)


def test_get_delete_user():
    user_id = 2

    response = reqres_api(
        'delete',
        f'/api/users/{user_id}'
    )

    assert response.status_code == 204


def test_post_successful_registration():
    schema = load_schema('post_register.json')

    response = reqres_api(
        'post',
        '/api/register',
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )

    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_post_unsuccessful_registration():
    response = reqres_api(
        'post',
        '/api/register',
        json={
            "email": "sydney@fife"
        }
    )

    assert response.status_code == 400
    assert response.json()['error'] == "Missing password"


def test_post_successful_login():
    schema = load_schema('post_login.json')

    response = reqres_api(
        'post',
        '/api/login',
        json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
    )

    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_post_unsuccessful_login():
    response = reqres_api(
        'post',
        '/api/login',
        json={
            "email": "peter@klaven"
        }
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'
