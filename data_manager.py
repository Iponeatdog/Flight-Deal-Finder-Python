import requests_cache
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        load_dotenv()
        self.SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.session = requests_cache.CachedSession(
            'sheety_cache',
            expire_after=3600
        )

    def get_data(self):
        response = self.session.get(url=self.SHEETY_ENDPOINT)
        response.raise_for_status()

        print("From cache:", response.from_cache)

        return response.json()


    def post_data(self):
        response = self.session.get(url=self.SHEETY_ENDPOINT)
        response.raise_for_status()

        print("From cache:", response.from_cache)
        return response.json()

    def update_lowest_price(self, row_id, new_price):
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        requests.put(
            url=f"{self.SHEETY_ENDPOINT}/{row_id}",
            json=new_data,
            auth=self._authorization
        )


