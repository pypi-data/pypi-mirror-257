import pytest
from uk_fuel_prices_api import UKFuelPricesApi


class TestApi:
    api: UKFuelPricesApi = None

    @pytest.fixture
    async def setup_api(self):
        if self.api is not None:
            return self.api

        self.api = UKFuelPricesApi()

        await self.api.get_prices()

        return self.api

    @pytest.mark.asyncio
    async def test_api(self, setup_api):
        api = await setup_api

        assert isinstance(api, UKFuelPricesApi)
        assert len(api.stations) > 0

    @pytest.mark.asyncio
    async def test_search(self, setup_api):
        api: UKFuelPricesApi = await setup_api

        stations = api.search("esso")  # search for Esso stations

        assert isinstance(stations, list)
        assert len(stations) > 0

        assert "brand" in stations[0].keys()
        assert "address" in stations[0].keys()
        assert "postcode" in stations[0].keys()

        assert stations[0]["brand"] == "ESSO"

    @pytest.mark.asyncio
    async def test_nearestN(self, setup_api):
        api: UKFuelPricesApi = await setup_api

        lat, lng = 53.743175, -1.882085  # Halifax Esso
        nearest_stations = api.nearestN(lat, lng)

        assert isinstance(nearest_stations, list)
        assert len(nearest_stations) == 5

        print(nearest_stations[0])

        assert "brand" in nearest_stations[0].keys()
        assert "address" in nearest_stations[0].keys()
        assert "postcode" in nearest_stations[0].keys()

        assert nearest_stations[0]["brand"] == "ESSO"

    def test_distance(self):
        dist = UKFuelPricesApi.distance(52, -1, 52, -2)
        assert round(dist, 2) == 68.46

        dist = UKFuelPricesApi.distance(12, 2, -10, -39)
        assert round(dist, 2) == 5148.18

    @pytest.mark.asyncio
    async def test_stationsWithinRadius(self, setup_api):
        api: UKFuelPricesApi = await setup_api

        lat, lng = 53.743175, -1.882085  # Halifax Esso
        radius = 0.1

        stations = api.stationsWithinRadius(lat, lng, radius)

        assert "brand" in stations[0].keys()
        assert "address" in stations[0].keys()
        assert "postcode" in stations[0].keys()

        assert len(stations) == 1
        assert stations[0]["brand"] == "ESSO"
        assert stations[0]["dist"] == 0

        # Larger radius
        # at time of writing this returns 9 stations
        radius = 5
        stations = api.stationsWithinRadius(lat, lng, radius)

        assert len(stations) > 1
        assert stations[0]["brand"] == "ESSO"


# TODO test endpoints are available
