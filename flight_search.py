import requests_cache
import os
from dotenv import load_dotenv

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        load_dotenv()

        self.session = requests_cache.CachedSession(
            'flight_cache',
            expire_after=3600
        )

        self.FLIGHT_ENDPOINT = "https://serpapi.com/search"
        self.API_KEY = os.getenv("SERPAPI_API_KEY")

    def get_data(self, origin_city_code, destination_city_code, from_time, to_time):

        flight_parameters = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "currency": "THB",
            "type": "1",
            "adults": "1",
            "outbound_date": from_time,
            "return_date": to_time,
            "api_key": self.API_KEY
        }

        response = self.session.get(
            self.FLIGHT_ENDPOINT,
            params=flight_parameters
        )
        print("From cache:", response.from_cache)
        print(response.url)
        return response.json()

