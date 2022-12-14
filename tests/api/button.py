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

    def test_post_success(self, client, db_category, dbsession):
        body = {
            "category_id": db_category.id,
            "icon": "https://lh3.googleusercontent.com/yURn6ISxDySTdXZAW2PUcADMnU3y9YX0M1RyXOH8a3sa1Tr0pHhPLGw5BKuiLiXa3Eh0fyHm7Dfsd9FodK3fxJge6g=w640-h400-e365-rj-sc0x00ffffff",
            "name": "string",
        }
        res = client.post(self._url, data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["category_id"] == body["category_id"]
        assert res_body["icon"] == body["icon"]
        assert res_body["name"] == body["name"]
        db_button_created: Button = (
            dbsession.query(Button).filter(Button.category_id == body["category_id"]).one_or_none()
        )
        assert db_button_created
        assert db_button_created.icon == body["icon"]
        assert db_button_created.category_id == body["category_id"]
        assert db_button_created.name == body["name"]
        assert db_button_created.category == db_category

    def test_get_by_id_success(self, client, db_button):
        res = client.get(f'{self._url}{db_button.id}')
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body['category_id'] == db_button.category_id
        assert res_body['icon'] == db_button.icon
        assert res_body['name'] == db_button.name

    def test_delete_by_id_success(self, client, dbsession, db_button):
        res = client.delete(f"{self._url}{db_button.id}")
        assert res.status_code == status.HTTP_200_OK
        q = dbsession.query(Button).filter(Button.id == db_button.id)
        assert q.one_or_none() is None
        get_res = client.get(f"{self._url}{db_button.id}")
        assert get_res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_success(self, db_button, dbsession, client):
        body = {"category_id": db_button.category_id, "icon": "cool icon", "name": "nice name"}
        res = client.patch(f"{self._url}{db_button.id}", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["category_id"] == body["category_id"]
        assert res_body["icon"] == body["icon"]
        assert res_body["name"] == body["name"]

    def test_get_by_id_not_found(self, client, db_button):
        res = client.get(f'{self._url}{db_button.id + 1}')
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_by_id_not_found(self, client, db_button):
        res = client.delete(f"{self._url}{db_button.id + 1}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, client, db_button):
        body = {"category_id": db_button.category_id, "icon": "cool icon", "name": "nice name"}
        res = client.patch(f"{self._url}{db_button.id + 1}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND
