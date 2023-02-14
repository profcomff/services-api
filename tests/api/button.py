import json
from starlette import status
from services_backend.settings import get_settings
from services_backend.models.database import Button


class TestButton:
    settings = get_settings()

    def test_get_success(self, client, db_button, db_category):
        res = client.get(f"/category/{db_category.id}/button/{db_button.id}")
        assert res.status_code == status.HTTP_200_OK
        assert res.json()['id'] == db_button.id

    def test_post_success(self, client, db_category, dbsession):
        body = {
            "icon": "https://lh3.googleusercontent.com/yURn6ISxDySTdXZAW2PUcADMnU3y9YX0M1RyXOH8a3sa1Tr0pHhPLGw5BKuiLiXa3Eh0fyHm7Dfsd9FodK3fxJge6g=w640-h400-e365-rj-sc0x00ffffff",
            "name": "string",
            "link": "google.com",
            "type": "test",
        }
        res = client.post(f"/category/{db_category.id}/button/", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["icon"] == body["icon"]
        assert res_body["order"] == 1
        assert res_body["name"] == body["name"]
        assert res_body["link"] == body["link"]
        assert res_body["type"] == body["type"]
        db_button_created: Button = dbsession.query(Button).filter(Button.id == res_body["id"]).one_or_none()
        assert db_button_created
        assert db_button_created.icon == body["icon"]
        assert db_button_created.name == body["name"]
        assert db_button_created.category == db_category
        assert db_button_created.link == body["link"]
        assert db_button_created.type == body["type"]
        assert db_button_created.order == 1

    def test_get_by_id_success(self, client, db_button, db_category):
        res = client.get(f"/category/{db_category.id}/button/{db_button.id}")
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body['icon'] == db_button.icon
        assert res_body['name'] == db_button.name
        assert res_body['order'] == db_button.order
        assert res_body['link'] == db_button.link
        assert res_body['type'] == db_button.type

    def test_delete_by_id_success(self, client, dbsession, db_button, db_category):
        res = client.delete(f"/category/{db_category.id}/button/{db_button.id}")
        assert res.status_code == status.HTTP_200_OK
        q = dbsession.query(Button).filter(Button.id == db_button.id)
        assert not q.one_or_none()
        get_res = client.get(f"/category/{db_category.id}/button/{db_button.id}")
        assert get_res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_success(self, db_button, client, db_category):
        body = {"icon": "cool icon", "name": "nice name", "order": 2, "link": "ya.ru", "type": "nice type"}
        res = client.patch(f"/category/{db_category.id}/button/{db_button.id}", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["icon"] == body["icon"]
        assert res_body["order"] == body["order"]
        assert res_body["name"] == body["name"]
        assert res_body["link"] == body["link"]
        assert res_body["type"] == body["type"]

    def test_patch_unset_params(self, client, db_button, db_category):
        body = {}
        res = client.patch(f"/category/{db_category.id}/button/{db_button.id}", data=json.dumps(body))
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        body["icon"] = "string"
        body["order"] = 1
        res = client.patch(f"/category/{db_category.id}/button/{db_button.id}", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["icon"] == body["icon"]
        body_name = {"name": "string", "order": 1}
        res = client.patch(f"/category/{db_category.id}/button/{db_button.id}", data=json.dumps(body_name))
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["name"] == body_name["name"]

    def test_get_by_id_not_found(self, client, db_button, db_category):
        res = client.get(f"/category/{db_category.id}/button/{db_button.id + 1}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_by_id_not_found(self, client, db_button, db_category):
        res = client.delete(f"/category/{db_category.id}/button/{db_button.id + 1}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, client, db_button, db_category):
        body = {"icon": "cool icon", "name": "nice name"}
        res = client.patch(f"/category/{db_category.id}/button/{db_button.id + 1}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_create_first(self, client, db_button, db_category):
        body = {
            "icon": "test",
            "name": "test",
            "link": "test",
            "type": "test",
        }

        res = client.post(f"/category/{db_category.id}/button/", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK

        res = client.patch(f"/category/{db_category.id}/button/{res.json()['id']}", data=json.dumps({"order": 1}))
        assert res.json()["order"] == 1
        res_old = client.get(f"/category/{db_category.id}/button/{db_button.id}")
        assert res_old.json()["order"] == 2

    def test_patch_order_fail(self, client, db_button, db_category):
        body = {
            "icon": "test",
            "name": "new",
            "link": "test",
            "type": "test",
        }
        res1 = client.post(f"/category/{db_category.id}/button/", data=json.dumps(body))
        assert res1.status_code == status.HTTP_200_OK

        body_patch = {
            "name": db_button.name,
            "order": 44,
        }
        res = client.patch(f"/category/{db_category.id}/button/{res1.json()['id']}", data=json.dumps(body_patch))
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_negative_order_fail(self, db_button, client, db_category):
        body = {
            "icon": "test",
            "name": "new",
            "link": "test",
            "type": "test",
        }
        res = client.post(f"/category/{db_category.id}/button/", data=json.dumps(body))
        res1 = client.patch(f"/category/{db_category.id}/button/{res.json()['id']}", data=json.dumps({"order": -10}))
        assert res1.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_order(self, db_button, client, db_category):
        body = {
            "icon": "test",
            "name": "new",
            "link": "test",
            "type": "test",
        }
        res1 = client.post(f"/category/{db_category.id}/button/", data=json.dumps(body))
        assert res1.status_code == status.HTTP_200_OK

        res = client.delete(f"/category/{db_category.id}/button/{res1.json()['id']}")
        assert res.status_code == status.HTTP_200_OK

        res = client.get(f"/category/{db_category.id}/button/{db_button.id}")
        assert res.json()['order'] == 1
