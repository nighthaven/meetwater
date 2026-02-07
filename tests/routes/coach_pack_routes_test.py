class TestCoachPackRoutes:
    def test_coach_pack_routes(self, swimming_coach_client):

        payload = {
            "sessions_count": 1,
            "price": 2000,
            "final_price": 2000,
        }

        response = swimming_coach_client.post("/coach_pack", json=payload)
        assert response.status_code == 201
