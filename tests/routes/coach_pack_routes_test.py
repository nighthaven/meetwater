from tests.fixtures.coach_pack_factory import CoachPackFactory


class TestCoachPackRoutes:
    def test_create_coach_pack_routes(self, swimming_coach_client):

        payload = {
            "sessions_count": 1,
            "price": 2000,
            "final_price": 2000,
        }

        response = swimming_coach_client.post("/coach_pack/", json=payload)
        assert response.status_code == 201

    def test_delete_coach_pack_routes(self, swimming_coach_client):
        swimming_coach = swimming_coach_client.user_type
        coach_pack = CoachPackFactory(swimming_coach=swimming_coach)

        response = swimming_coach_client.delete(f"/coach_pack/{str(coach_pack.id)}")
        assert response.status_code == 204
