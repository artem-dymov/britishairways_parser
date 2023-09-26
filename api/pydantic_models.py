from pydantic import BaseModel, Field


class FlightRequestModel(BaseModel):
    departure_airport_code: str = Field(max_length=3, min_length=3)
    arrival_airport_code: str = Field(max_length=3, min_length=3)
    departure_date: str

    cabin: str
    flex: str


class PassengersRequestModel(BaseModel):
    ad: int
    yad: int
    ch: int
    inf: int


class FlightsRequestBody(BaseModel):
    flights: list[FlightRequestModel]
    passengers: PassengersRequestModel


class FlightResponseModel(BaseModel):
    departure: str
    arrival: str
    company: str
    stops_info: str
    duration_summary: str
    fares: dict
