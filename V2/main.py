from typing import Optional
from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import urllib.parse
from queries import get_cards,gender_dist, hourly_trips, top_routes, top_locations, stations

description = """
The following API's are used on my Ecobici dashboard. 🚀
"""

app = FastAPI(
    title="Ecobici Quick API",
    description=description
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/cards/{trip_year}")
def read_cards(trip_year:int, trip_month:Optional[int]=None, trip_day:Optional[int]=None):

    if trip_year == 2018:
        q1=f'trip_year > {trip_year}'
    else:
        q1=f'trip_year = {trip_year}'
    
    if trip_month:
        q2 = f" AND trip_month = {trip_month}"
    else:
        q2="" 
    
    if trip_day:
        q3= f" AND trip_day = {trip_day}"
    else:
        q3=""

    query = f"{q1}{q2}{q3}"
    
    # print(query)

    cards = get_cards(cardsdate=query)
    gender = gender_dist(cardsdate=query)
    hours = hourly_trips(cardsdate=query)
    routes = top_routes(cardsdate=query)
    topLocations = top_locations(cardsdate=query)
    allStations = stations()
 
    return{
        "cardsData":cards,
        "gender":gender,
        "hourly_trips": hours,
        "top_routes":routes,
        "top_locations":topLocations,
        "stations":allStations
    }

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}