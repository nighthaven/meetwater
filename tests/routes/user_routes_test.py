from datetime import date


class TestCreateUser:
    def test_create_users(self, client):
        response = client.post(
            "/users/",
            json={
                "email": "hello123@gmail.com",
                "password": "pass",
                "first_name": "Tom",
                "last_name": "Bombadil",
                "birth_date": date(2000, 1, 16).isoformat(),
            },
        )
        assert response.status_code == 201
