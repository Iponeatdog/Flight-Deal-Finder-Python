#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from pprint import pprint
from datetime import datetime, timedelta

sheety = DataManager()
sheet_data = sheety.get_data()
# pprint(sheet_data)

now = datetime.now()
tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
six_month_from_today = (now + timedelta(days=180)).strftime("%Y-%m-%d")

flights = FlightSearch().get_data(
    origin_city_code="LHR",
    destination_city_code="CDG",
    from_time=tomorrow,
    to_time=six_month_from_today
)
# pprint(flights)
cheapest_flight = find_cheapest_flight(flights, return_date=six_month_from_today.strftime("%Y-%m-%d"))
pprint(f"{sheet_data[0]['city']}: GBP {cheapest_flight.price}")

if cheapest_flight.price != "N/A" and cheapest_flight.price < sheet_data[0]["lowestPrice"]:
    pprint(f"Lower price flight found to {sheet_data[0]['city']}!")
    sheety.update_lowest_price(sheet_data[0]["id"], cheapest_flight.price)
