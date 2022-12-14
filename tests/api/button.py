import pytest
import json
from starlette import status
from services_backend.settings import get_settings
from services_backend.models.database import Button


class TestButton:
    _url = '/button/'
    settings = get_settings()

    def test_get_success(self, client, db_button):
        res = client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) == 1
        assert res.json()[0]['id'] == db_button.id

    def test_post_success(self, client, db_category):
        body = {
            "category_id": db_category.id,
            "icon": "string",
            "name": "string"
        }
        res = client.post(self._url, data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK

    def test_get_by_id_success(self, client, db_button):
        res = client.get(f'{self._url}{db_button.id}')
        assert res.status_code == status.HTTP_200_OK
        assert res.json()['category_id'] == db_button.category_id

    def test_delete_by_id_success(self, client, dbsession, db_category):
        _button = Button(id=666, name='strange button', category_id=db_category.id)
        dbsession.add(_button)
        dbsession.flush()
        res = client.delete(f"{self._url}{_button.id}")
        assert res.status_code == status.HTTP_200_OK
        q = dbsession.query(Button).filter(Button.id == _button.id)
        assert q.one_or_none() is None

    def test_patch_by_id_success(self, db_button, dbsession, client):
        body = {
            "category_id": db_button.category_id,
            "icon": "cool icon",
            "name": "nice name"
        }
        res = client.patch(f"{self._url}{db_button.id}", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
