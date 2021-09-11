from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
from bikescripts import total_trips_per_day, gender_trips, trips_on_week,cards_stats,trip_hours
from stations import stations_data, stations_dict
import json
  
# Opening JSON file
f = open('./sample6.json',)
s = open('./topstation1.json',)
  
# returns JSON object as 
# a dictionary
datajson = json.load(f)
datastations = json.load(s)

app=FastAPI()

templates = Jinja2Templates(directory="templates")
@app.get("/")
def read_root(request:Request):

    getMonth = "ecobici_may"
    tripsChart = total_trips_per_day(fileName=getMonth)
    genderTrips = gender_trips(fileName=getMonth)
    weekChart = trips_on_week(fileName=getMonth)
    stationChart = cards_stats(fileName=getMonth)
    tripsHour= trip_hours(fileName=getMonth)
    
    return templates.TemplateResponse("index.html", {
        "request":request,
        "trips":tripsChart,
        "gender":genderTrips,
        "week": weekChart,
        "stations":stationChart,
        "tripsH":tripsHour
    })

@app.get("/stations")
def get_stations(request:Request):

    stationsData,stations = stations_data(fileName= "estaciones_ecobici")

    return templates.TemplateResponse("stations.html",{
        "request":request,
        "stations":stationsData,
        "stationsI":stations
        })

@app.get("/stationsv2")
def get_stationsI(request:Request):

    getMonth = "ecobici_may"
    building_dict,building_dictI,trip_dict = stations_dict(fileName= getMonth)
    stationsData,stations = stations_data(fileName= "estaciones_ecobici")

    return templates.TemplateResponse("stationsv2.html",{
        "request":request,
        "trip_dict":building_dict,
        "trip_dictI":building_dictI,
        "list_of_trips":trip_dict,
        "stationsI":stations,
        'topStation':datastations
        })


@app.get("/indexv2")
def read_test(request:Request):


    return templates.TemplateResponse(f"indexv2.html", {
        "request":request,
        "fake_data":datajson
        })

@app.get("/{nameofpage}")
def read_pages(request:Request, nameofpage:str):
    return templates.TemplateResponse(f"{nameofpage}.html", {
        "request":request
        })



# @app.get("/totalTrips")
# def get_trips():
#     getMonth = "ecobici_may"
#     tripsChart = total_trips_per_day(fileName=getMonth)

#     return{
#         "bike_trips":tripsChart
#     }


