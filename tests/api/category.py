import json
import pytest
from starlette import status
from services_backend.settings import get_settings
from services_backend.models.database import Category


class TestCategory:
    _url = '/category/'
    settings = get_settings()

    def test_get_success(self, client, db_category):
        res = client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert len(res_body) == 1
        assert res_body[0]['id'] == db_category.id
        assert res_body[0]['type'] == db_category.type
        assert res_body[0]['name'] == db_category.name
        assert res_body[0]['order'] == db_category.order
        assert res_body[0]['buttons'] == []

    def test_post_success(self, client, dbsession):
        body = {"type": "string", "name": "string"}
        res = client.post(self._url, data=json.dumps(body))
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
        assert db_category_created.buttons == []

    def test_get_by_id_success(self, client, db_category):
        res = client.get(f'{self._url}{db_category.id}')
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body['id'] == db_category.id
        assert res_body['type'] == db_category.type
        assert res_body['name'] == db_category.name
        assert res_body['order'] == db_category.order
        assert res_body['buttons'] == []

    def test_delete_by_id_success(self, client, dbsession, db_category):
        res = client.delete(f'{self._url}{db_category.id}')
        assert res.status_code == status.HTTP_200_OK
        q = dbsession.query(Category).filter(Category.id == db_category.id)
        assert q.one_or_none() is None
        get_res = client.get(f'{self._url}{db_category.id}')
        assert get_res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_success(self, client, db_category, dbsession):
        body = {"type": "test", "name": "test", "order": 1}
        res = client.patch(f"{self._url}{db_category.id}", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body['type'] == body['type']
        assert res_body['name'] == body['name']
        assert res_body['order'] == body['order']

    def test_patch_unset_params(self, client, db_category, dbsession):
        body = {}
        res = client.patch(f"{self._url}{db_category.id}", data=json.dumps(body))
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        body["order"] = 1
        res = client.patch(f"{self._url}{db_category.id}", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["order"] == body["order"]
        body_ord = {
            "order": 1
        }
        res = client.patch(f"{self._url}{db_category.id}", data=json.dumps(body_ord))
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["order"] == body_ord["order"]

    def test_get_by_id_not_found(self, client, db_category):
        res = client.get(f'{self._url}/{db_category.id + 1}')
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_by_id_not_found(self, client, db_category):
        res = client.delete(f'{self._url}{db_category.id + 1}')
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, client, db_category):
        body = {"type": "string", "name": "string", "order": 1}
        res = client.patch(f"{self._url}{db_category.id + 1}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_create_first(self, client, dbsession, db_category):
        body = {
            "name": "test",
            "type": "test",
        }

        res = client.post(self._url, data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res1 = client.patch(f"{self._url}{res.json()['id']}", data=json.dumps({"order": 1}))
        assert res1.status_code == status.HTTP_200_OK
        assert res1.json()["order"] == 1

        res_old = client.get(f"{self._url}{db_category.id}")
        assert res_old.json()["order"] == 2

    def test_patch_order(self, client, db_category, dbsession):
        body = {
            "name": "new",
            "type": "test",
        }
        res1 = client.post(self._url, data=json.dumps(body))
        assert res1.status_code == status.HTTP_200_OK
        res = client.patch(f"{self._url}{res1.json()['id']}", data=json.dumps({"order": 1}))
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["order"] == 1

        res = client.get(f"{self._url}{db_category.id}")
        assert res.json()["order"] == 2

    def test_create_third_fail(self, dbsession, db_category, client):
        body = {
            "name": "new",
            "type": "test",
        }
        res1 = client.post(self._url, data=json.dumps(body))
        assert res1.status_code == status.HTTP_200_OK
        res = client.patch(f"{self._url}{res1.json()['id']}", data=json.dumps({"order": 33}))
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_negative_order_fail(self, dbsession, db_category, client):
        body = {
            "name": "new",
            "type": "test",
        }
        res1 = client.post(self._url, data=json.dumps(body))
        assert res1.status_code == status.HTTP_200_OK
        res = client.patch(f"{self._url}{res1.json()['id']}", data=json.dumps({"order": -1}))
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_order(self, db_category, client, dbsession):
        body = {
            "name": "new",
            "type": "test",
        }
        res1 = client.post(self._url, data=json.dumps(body))
        assert res1.status_code == status.HTTP_200_OK
        assert res1.json()['order'] == 2

        res = client.delete(f"{self._url}{db_category.id}")
        assert res.status_code == status.HTTP_200_OK

        res = client.get(f"{self._url}{res1.json()['id']}")
        assert res.json()['order'] == 1