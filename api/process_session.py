from typing import Union
from parser.Session import Session
import time
from multiprocessing import Manager, Queue

from parser.Flight import Flight
from api.pydantic_models import *
import config

# query in queue schema ( # - means some value and value`s type in braces )
# {'web_query_id: #(int)', 'flights_query_id': #(int), 'flights_search': #(list[FlightRequestModel]),
# 'passengers': #(PassengersRequestModel)}

# results
# {'web_query_id: #(int)', 'flights_query_id': #(int), 'flights_response': #(None | list[FLightResponseModel])


def process_session(queue: Queue, results: list[dict]):
    print('creating session')
    session = Session()
    print('starting manual request')
    # session.startup_manual_request()
    print('Session started')

    while True:
        if queue.qsize() > 0:
            query: dict = queue.get()
            passengers: PassengersRequestModel = query['passengers']

            flight_search = query['flights_search']
            flight_search: FlightRequestModel
            flights_response = []

            onds = (f'{flight_search.departure_airport_code}-{flight_search.arrival_airport_code}_'
                    f'{flight_search.departure_date}')
            ad = passengers.ad
            yad = passengers.yad
            ch = passengers.ch
            inf = passengers.inf

            cabin = flight_search.cabin
            flex = flight_search.flex

            ond = 1

            link_params = f'?onds={onds}&ad={ad}&yad={yad}&ch={ch}&inf={inf}&cabin={cabin}&flex={flex}&ond={ond}'
            weblink = config.base_request_link + link_params

            session.make_request(weblink)

            # returns None if no flights found
            flights: Union[list[Flight], None] = session.parse_page()

            if flights:
                for flight in flights:
                    # saving fares without WebElement button
                    # saving and sending response with fares with WebElement button can invoke error
                    new_fares = {}
                    for fare_name, value in flight.fares.items():
                        new_fares.update({fare_name: value[0]})
                    flight.fares = new_fares

                    # Converting Flight object with its data to BaseModel object
                    fl = FlightResponseModel(**flight.__dict__)
                    flights_response.append(fl)
            else:
                flights_response = None

            # response.update({f'flight_request{count}_results': flights_response})
            results.append({
                'web_query_id': query['web_query_id'],
                'flights_query_id': query['flights_query_id'],
                'flights_response': flights_response
            })

        time.sleep(2)


# process_session()
