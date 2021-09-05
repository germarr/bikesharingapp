from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
from bikescripts import total_trips_per_day, gender_trips, trips_on_week,cards_stats

app=FastAPI()

templates = Jinja2Templates(directory="templates")
@app.get("/")
def read_root(request:Request):

    getMonth = "ecobici_may"
    tripsChart = total_trips_per_day(fileName=getMonth)
    genderTrips = gender_trips(fileName=getMonth)
    weekChart = trips_on_week(fileName=getMonth)
    stationChart = cards_stats(fileName=getMonth)
    
    return templates.TemplateResponse("index.html", {
        "request":request,
        "trips":tripsChart,
        "gender":genderTrips,
        "week": weekChart,
        "stations":stationChart
    })

# @app.get("/totalTrips")
# def get_trips():
#     getMonth = "ecobici_may"
#     tripsChart = total_trips_per_day(fileName=getMonth)

#     return{
#         "bike_trips":tripsChart
#     }


