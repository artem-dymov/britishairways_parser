import time
from typing import Union
import uvicorn
import asyncio

import config
from parser.Flight import Flight

from fastapi import FastAPI
from pydantic import BaseModel, Field

from threading import Thread

from parser.Session import Session

app = FastAPI()

session = None
if session is None:
    print('if not')
    session = Session()
else:
    print('else')

session.startup_manual_request()


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


@app.post("/search_flights/")
async def search_flights(flights_request_body: FlightsRequestBody):

    response = {}
    count = 0
    for flight_search in flights_request_body.flights:
        flights_response = []

        onds = (f'{flight_search.departure_airport_code}-{flight_search.arrival_airport_code}_'
                f'{flight_search.departure_date}')
        ad = flights_request_body.passengers.ad
        yad = flights_request_body.passengers.yad
        ch = flights_request_body.passengers.ch
        inf = flights_request_body.passengers.inf

        cabin = flight_search.cabin
        flex = flight_search.flex

        ond = 1

        link_params = f'?onds={onds}&ad={ad}&yad={yad}&ch={ch}&inf={inf}&cabin={cabin}&flex={flex}&ond={ond}'
        weblink = config.base_request_link + link_params

        session.make_request(weblink)

        flights = session.parse_page()

        if flights:
            for flight in flights:
                # Conditions not parsing now so they always None
                del flight.conditions

                # saving fares without WebElement button
                # saving and sending response with fares with WebElement button can invoke error
                new_fares = {}
                for fare_name, value in flight.fares.items():
                    new_fares.update({fare_name: value[0]})
                flight.fares = new_fares

                # Converting Flight object with its data to BaseModel object
                fl = FlightResponseModel(**flight.__dict__)
                flights_response.append(fl)

            response.update({f'flight_request{count}_results': flights_response})

        else:
            response.update({f'flight_request{count}_results': None})

        count += 1

    return {'search_results': response}

