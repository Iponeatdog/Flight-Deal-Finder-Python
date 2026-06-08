import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        load_dotenv()
        self.SHEETY_ENDPOINT_PRICES = os.getenv("SHEETY_ENDPOINT_PRICES")
        self.SHEETY_ENDPOINT_USERS = os.getenv("SHEETY_ENDPOINT_USERS")
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.session = requests.Session()

    def get_destination_data(self):
        response = self.session.get(url=self.SHEETY_ENDPOINT_PRICES, auth=self._authorization)
        data = response.json()
        destination_data = data["prices"]
        return destination_data

    def update_lowest_price(self, row_id, new_price):
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        requests.put(
            url=f"{self.SHEETY_ENDPOINT_PRICES}/{row_id}",
            json=new_data,
            auth=self._authorization
        )

    def get_customer_emails(self):
        response = self.session.get(url=self.SHEETY_ENDPOINT_USERS, auth=self._authorization)
        data = response.json()["users"]
        emails_list = [item["email"] for item in data]
        return emails_list
