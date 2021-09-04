from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests

app=FastAPI()

templates = Jinja2Templates(directory="templates")
@app.get("/")
def read_root(request:Request):

    # r = requests.get("http://34.220.116.144/streamers/es")
    # twitch_videos= [r.json()[str(i)] for i in range(len(r.json()))]
    
    return templates.TemplateResponse("index.html", {
        "request":request
        # "twitch_videos":twitch_videos
    })



