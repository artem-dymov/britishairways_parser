from typing import Union


class Flight:
    # prices - dict where key - tariff name and value - price (price is string because contains currency sign)
    def __init__(self, departure: str, arrival: str, company: str, stops_info: str, duration_summary,
                 tariffs: dict[str, str], detailed_info_link: str,
                 conditions: Union[list[str], None] = None):

        self.detailed_info_link = detailed_info_link
        self.tariffs = tariffs
        self.duration_summary = duration_summary
        self.stops_info = stops_info
        self.company = company
        self.arrival = arrival
        self.departure = departure

        self.conditions = conditions



