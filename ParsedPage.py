from selenium.webdriver.remote.webelement import WebElement
from Flight import Flight

class ParsedPage:
    def __init__(self, loading_marker: WebElement, locations: str, flight: Flight):
        self.flight = flight
        self.locations = locations
        self.loading_marker = loading_marker


