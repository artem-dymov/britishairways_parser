from typing import Union
from selenium.webdriver.remote.webelement import WebElement


class Flight:
    # tariffs - dict where key - tariff name and value - list (price is string because contains currency sign).
    # value list contains 2 elements: 1st - price (price is string because contains currency sign),
    #                                 2nd - WebElement (button) that needed to select tariff and go to next page
    def __init__(self, departure: str, arrival: str, company: str, stops_info: str, duration_summary,
                 tariffs: dict[str, tuple[str, WebElement]], open_flight_cards_btn: WebElement,
                 conditions: Union[tuple[str], None] = None):

        self.open_flight_cards_btn = open_flight_cards_btn
        self.tariffs = tariffs
        self.duration_summary = duration_summary
        self.stops_info = stops_info
        self.company = company
        self.arrival = arrival
        self.departure = departure
        
        self.conditions = conditions



