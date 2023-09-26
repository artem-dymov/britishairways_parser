from fastapi import FastAPI
from api.pydantic_models import *
from api.process_session import process_session
from multiprocessing import Process, Manager, Queue

max_web_query_id = 0
manager = Manager()
queue: Queue = manager.Queue()
results = manager.list()

processes = []
for i in range(2):
    process = Process(target=process_session, args=(queue, results,), name='i')
    print('process created')

    process.daemon = True
    process.start()
    processes.append(process)

app = FastAPI()

# query in queue schema ( # - means some value and value`s type in braces )
# {'web_query_id: #(int)', 'flights_query_id': #(int), 'flights_search': #(list[FlightRequestModel]),
# 'passengers': #(PassengersRequestModel)}

# results
# {'web_query_id: #(int)', 'flights_query_id': #(int), 'flights_response': #(None | list[FLightResponseModel])


@app.post("/search_flights/")
async def search_flights(flights_request_body: FlightsRequestBody):
    global max_web_query_id
    max_web_query_id += 1
    web_query_id = max_web_query_id

    response = {}
    flights_query_id = 0
    for flight_search in flights_request_body.flights:
        queue.put({
            'web_query_id': web_query_id,
            'flights_query_id': flights_query_id,
            'flights_search': flight_search,
            'passengers': flights_request_body.passengers
        })

        flights_query_id += 1

    while True:
        for result in results:
            if result['web_query_id'] == web_query_id:
                response.update({f'flight_request{result["flights_query_id"]}_results': result['flights_response']})

        if len(response.keys()) == len(flights_request_body.flights):
            print('breaked')
            break
    # response.update({f'flight_request{count}_results': None})

    return {'search_results': response}
