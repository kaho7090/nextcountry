from __future__ import annotations

from nextcountry.flights.config import TravelportSettings, load_travelport_settings
from nextcountry.flights.models import FlightOffer, FlightSearchParams
from nextcountry.flights.travelport.auth import TravelportTokenProvider
from nextcountry.flights.travelport.client import TravelportSearchClient
from nextcountry.flights.travelport.parser import parse_search_response


class TravelportFlightSearchProvider:
    def __init__(
        self,
        settings: TravelportSettings | None = None,
        client: TravelportSearchClient | None = None,
    ) -> None:
        self._settings = settings or load_travelport_settings()
        if client is None:
            token_provider = TravelportTokenProvider(self._settings)
            client = TravelportSearchClient(self._settings, token_provider)
        self._client = client

    def search(self, params: FlightSearchParams) -> list[FlightOffer]:
        payload = self._client.search_catalog(params)
        return parse_search_response(payload)
