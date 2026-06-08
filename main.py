#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from pprint import pprint
from datetime import datetime, timedelta
from mail_manager import MailManager

sheety = DataManager()
sheet_data = sheety.get_destination_data()
# pprint(sheet_data)

now = datetime.now()
tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
six_month_from_today = (now + timedelta(days=180)).strftime("%Y-%m-%d")

flight_search = FlightSearch()

ORIGIN_CITY_IATA = "BKK"
for destination in sheet_data:
    pprint(f"Getting flights for {destination['city']}...")
    flights = flight_search.get_data(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights, return_date=six_month_from_today)
    pprint(f"{destination['city']}: THB {cheapest_flight.price}")


    if cheapest_flight == "N/A":
        print(f"No direct flight to {destination['city']}, looking for indirect flight...")
        stopover_flights = flight_search.get_data(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False,
        )
        cheapest_flight = find_cheapest_flight(stopover_flights, return_date=six_month_from_today)
        print(f"Cheapest indirect flight price is: THB {cheapest_flight.price}")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only THB {cheapest_flight.price} to fly direct "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only THB {cheapest_flight.price} to fly " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"with {cheapest_flight.stops} stop(s) " \
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        pprint(f"Lower price flight found to {destination['city']}!")
        sheety.update_lowest_price(destination["id"], cheapest_flight.price)
        email_list = sheety.get_customer_emails()
        mail_manager = MailManager()
        mail_manager.sendmails(
            email_list = email_list,
            destination=f"{destination['city']}",
            message_body=f"Low price alert! Only {cheapest_flight.price} THB to fly "
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )

email_list = sheety.get_customer_emails()
