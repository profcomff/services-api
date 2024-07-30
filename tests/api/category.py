import json

from pytest_mock import MockerFixture
from starlette import status

from services_backend.models.database import Category
from services_backend.settings import get_settings


settings = get_settings()


def test_get_success(client, db_category):
    res = client.get('/category')
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert len(res_body) == 1
    assert res_body[0]['id'] == db_category.id
    assert res_body[0]['type'] == db_category.type
    assert res_body[0]['name'] == db_category.name
    assert res_body[0]['order'] == db_category.order


def test_post_success(client, dbsession):
    body = {"type": "string", "name": "string"}
    res = client.post('/category', data=json.dumps(body))
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body["type"] == body["type"]
    assert res_body["name"] == body["name"]
    assert res_body["order"] == 1
    db_category_created: Category = dbsession.query(Category).filter(Category.name == body["name"]).one_or_none()
    assert db_category_created
    assert db_category_created.name == body["name"]
    assert db_category_created.type == body["type"]
    assert db_category_created.order == 1
    assert not db_category_created.buttons
    client.delete(f'/category/{db_category_created.id}')


def test_get_by_id_success(client, db_category, mocker: MockerFixture):
    res = client.get(f'/category/{db_category.id}')
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body['id'] == db_category.id
    assert res_body['type'] == db_category.type
    assert res_body['name'] == db_category.name
    assert res_body['order'] == db_category.order

    user_mock = mocker.patch('auth_lib.fastapi.UnionAuth.__call__')
    user_mock.return_value = {
        "session_scopes": [
            {"id": 0, "name": "string", "comment": "string"},
            {"id": 1, "name": "test", "comment": "string"},
        ],
        "user_scopes": [{"id": 0, "name": "string", "comment": "string"}],
        "indirect_groups": [{"id": 0, "name": "string", "parent_id": 0}],
        "groups": [{"id": 0, "name": "string", "parent_id": 0}],
        "id": 0,
        "email": "string",
    }

    res = client.get(f'/category/{db_category.id}')
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body['id'] == db_category.id
    assert res_body['type'] == db_category.type
    assert res_body['name'] == db_category.name
    assert res_body['order'] == db_category.order


def test_delete_by_id_success(client, dbsession, db_category):
    res = client.delete(f'/category/{db_category.id}')
    assert res.status_code == status.HTTP_200_OK
    q = dbsession.query(Category).filter(Category.id == db_category.id)
    assert q.one_or_none() is None
    get_res = client.get(f'/category/{db_category.id}')
    assert get_res.status_code == status.HTTP_404_NOT_FOUND


def test_patch_by_id_success(client, db_category):
    body = {"type": "test", "name": "test", "order": 1}
    res = client.patch(f"/category/{db_category.id}", data=json.dumps(body))
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body['type'] == body['type']
    assert res_body['name'] == body['name']
    assert res_body['order'] == body['order']


def test_patch_unset_params(client, db_category):
    body = {}
    body["order"] = 1
    res = client.patch(f"/category/{db_category.id}", data=json.dumps(body))
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["order"] == body["order"]
    body_ord = {"order": 1}
    res = client.patch(f"/category/{db_category.id}", data=json.dumps(body_ord))
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["order"] == body_ord["order"]


def test_get_by_id_not_found(client, db_category):
    res = client.get(f'/category/{db_category.id + 1}')
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_by_id_not_found(client, db_category):
    res = client.delete(f'/category/{db_category.id + 1}')
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_patch_by_id_not_found(client, db_category):
    body = {"type": "string", "name": "string", "order": 1}
    res = client.patch(f"/category/{db_category.id + 1}", data=json.dumps(body))
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_create_first(client, db_category):
    body = {
        "name": "test",
        "type": "test",
    }

    res = client.post('/category', data=json.dumps(body))
    assert res.status_code == status.HTTP_200_OK
    res1 = client.patch(f"/category/{res.json()['id']}", data=json.dumps({"order": 1}))
    assert res1.status_code == status.HTTP_200_OK
    assert res1.json()["order"] == 1

    res_old = client.get(f"/category/{db_category.id}")
    assert res_old.json()["order"] == 2
    client.delete(f"/category/{res.json()['id']}")


def test_patch_order(client, db_category):
    body = {
        "name": "new",
        "type": "test",
    }
    res1 = client.post('/category', data=json.dumps(body))
    assert res1.status_code == status.HTTP_200_OK
    res = client.patch(f"/category/{res1.json()['id']}", data=json.dumps({"order": 1}))
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["order"] == 1

    res = client.get(f"/category/{db_category.id}")
    assert res.json()["order"] == 2
    client.delete(f"/category/{res1.json()['id']}")


def test_create_third_fail(db_category, client):
    body = {
        "name": "new",
        "type": "test",
    }
    res1 = client.post('/category', data=json.dumps(body))
    assert res1.status_code == status.HTTP_200_OK
    res = client.patch(f"/category/{res1.json()['id']}", data=json.dumps({"order": 33}))
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    client.delete(f"/category/{res1.json()['id']}")


def test_create_negative_order_fail(db_category, client):
    body = {
        "name": "new",
        "type": "test",
    }
    res1 = client.post('/category', data=json.dumps(body))
    assert res1.status_code == status.HTTP_200_OK
    res = client.patch(f"/category/{res1.json()['id']}", data=json.dumps({"order": -1}))
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    client.delete(f"/category/{res1.json()['id']}")


def test_delete_order(db_category, client):
    body = {
        "name": "new",
        "type": "test",
    }
    res1 = client.post('/category', data=json.dumps(body))
    assert res1.status_code == status.HTTP_200_OK
    assert res1.json()['order'] == 2

    res = client.delete(f"/category/{db_category.id}")
    assert res.status_code == status.HTTP_200_OK

    res = client.get(f"/category/{res1.json()['id']}")
    assert res.json()['order'] == 1
    client.delete(f"/category/{res1.json()['id']}")


def test_scopes(client, dbsession, mocker: MockerFixture):
    user_mock = mocker.patch('auth_lib.fastapi.UnionAuth.__call__')
    user_mock.return_value = {
        "session_scopes": [{"id": 0, "name": "string", "comment": "string"}],
        "user_scopes": [{"id": 0, "name": "string", "comment": "string"}],
        "indirect_groups": [{"id": 0, "name": "string", "parent_id": 0}],
        "groups": [{"id": 0, "name": "string", "parent_id": 0}],
        "id": 0,
        "email": "string",
    }

    # Create value
    body = {"name": "new", "type": "grid3", "scopes": ["string"]}
    res1 = client.post('/category', data=json.dumps(body))
    assert res1.status_code == status.HTTP_200_OK
    id_ = res1.json()['id']
    assert res1.json()['scopes'] == ["string"]

    res2 = client.get(f'/category/{id_}')
    assert res2.status_code == status.HTTP_200_OK
    assert res2.json()['scopes'] == ["string"]

    # Patch value to value
    body = {"scopes": ["string2"]}
    res3 = client.patch(f'/category/{id_}', data=json.dumps(body))
    assert res3.status_code == status.HTTP_200_OK
    assert res3.json()['scopes'] == ["string2"]

    res4 = client.get(f'/category/{id_}')
    assert res4.status_code == status.HTTP_404_NOT_FOUND

    # Patch value to null
    body = {"scopes": []}
    res5 = client.patch(f'/category/{id_}', data=json.dumps(body))
    assert res5.status_code == status.HTTP_200_OK
    assert res5.json()['scopes'] == []

    res6 = client.get(f'/category/{id_}')
    assert res6.status_code == status.HTTP_200_OK
    assert res6.json()['scopes'] == []

    # Patch null to value
    body = {"scopes": ["string3"]}
    res7 = client.patch(f'/category/{id_}', data=json.dumps(body))
    assert res7.status_code == status.HTTP_200_OK
    assert res7.json()['scopes'] == ["string3"]

    res8 = client.get(f'/category/{id_}')
    assert res8.status_code == status.HTTP_404_NOT_FOUND

    category = dbsession.query(Category).filter(Category.id == id_).one_or_none()
    dbsession.delete(category)
    dbsession.commit()


def test_get_hidden_button_success(client, dbsession, db_button):
    db_button.is_hidden = True
    dbsession.commit()
    res = client.get('/category', params={"info": "buttons"})
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert len(res_body) == 1
    assert len(res_body[0]["buttons"]) == 1
    assert res_body[0]["buttons"][0]["id"] == db_button.id
    assert res_body[0]["buttons"][0]["view"] == "hidden"
    assert "link" not in res_body[0]["buttons"][0]
