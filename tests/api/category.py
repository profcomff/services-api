import pytest
import json
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
        assert res_body[0]['buttons'] == []

    def test_post_success(self, client, dbsession):
        body = {
            "type": "string",
            "name": "string"
        }
        res = client.post(self._url, data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["type"] == body["type"]
        assert res_body["name"] == body["name"]
        db_category_created: Category = dbsession.query(Category).filter(Category.name == body["name"]).one_or_none()
        assert db_category_created
        assert db_category_created.name == body["name"]
        assert db_category_created.type == body["type"]
        assert db_category_created.buttons == []

    def test_get_by_id_success(self, client, db_category):
        res = client.get(f'{self._url}{db_category.id}')
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body['id'] == db_category.id
        assert res_body['type'] == db_category.type
        assert res_body['name'] == db_category.name
        assert res_body['buttons'] == []

    def test_delete_by_id_success(self, client, dbsession, db_category):
        res = client.delete(f'{self._url}{db_category.id}')
        assert res.status_code == status.HTTP_200_OK
        q = dbsession.query(Category).filter(Category.id == db_category.id)
        assert q.one_or_none() is None
        get_res = client.get(f'{self._url}{db_category.id}')
        assert get_res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_success(self, client, db_category, dbsession):
        body = {
            "type": "string",
            "name": "string"
        }
        res = client.patch(f"{self._url}{db_category.id}", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body['type'] == body['type']
        assert res_body['name'] == body['name']
        db_category_patched: Category = dbsession.query(Category).filter(Category.id == db_category.id).one_or_none()
        assert db_category_patched
        assert db_category_patched.id == db_category.id
        assert db_category_patched.name == body["name"]
        assert db_category_patched.type == body["type"]


    def test_get_by_id_not_found(self, client, db_category):
        res = client.get(f'{self._url}{db_category.id + 1}')
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_by_id_not_found(self, client, db_category):
        res = client.delete(f'{self._url}{db_category.id + 1}')
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, client, db_category):
        body = {
            "type": "string",
            "name": "string"
        }
        res = client.patch(f"{self._url}{db_category.id + 1}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND
