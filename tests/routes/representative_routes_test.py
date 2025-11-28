from datetime import date


class TestCreateRepresentativeRoute:
    def test_create_representative_user(self, client, representative_repo):
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": date(2000, 1, 16).isoformat(),
            "email": "johndoe@gmail.com",
            "raw_password": "password",
        }
        response = client.post("/representatives", json=payload)

        assert response.status_code == 201
