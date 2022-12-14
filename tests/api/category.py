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
        assert len(res.json()) == 1
        assert res.json()[0]['id'] == db_category.id

    def test_post_success(self, client, dbsession):
        body = {
            "type": "string",
            "name": "string"
        }
        res = client.post(self._url, data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK

    def test_get_by_id_success(self, client, db_category):
        res = client.get(f'{self._url}{db_category.id}')
        assert res.status_code == status.HTTP_200_OK
        assert res.json()['id'] == db_category.id

    def test_delete_by_id_success(self, client, dbsession):
        _category = Category(id=33, name='deleted', type='typee')
        dbsession.add(_category)
        dbsession.flush()
        res = client.delete(f'{self._url}{_category.id}')
        assert res.status_code == status.HTTP_200_OK
        q = dbsession.query(Category).filter(Category.id == _category.id)
        assert q.one_or_none() is None

    def test_patch_by_id_success(self, client, db_category):
        body = {
            "type": "string",
            "name": "string"
        }
        res = client.patch(f"{self._url}{db_category.id}", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK

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
