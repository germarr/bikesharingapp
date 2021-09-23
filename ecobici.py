import pandas as pd
import numpy as np
import geopy.distance
import json

def main(months):
    fulldf = pd.concat([pd.read_csv(f"./ecobicidata/ecobici_{x}.csv") for i,x in enumerate(months)])
    df = transform_df(ene=fulldf.sample(352301))
    estaciones_retiro, estaciones_arribo = estaciones_df()
    exportfileI = mergingfiles(month=df, er=estaciones_retiro, ea=estaciones_arribo)
    efile = exportfileI.replace("",np.nan).dropna(axis=0)
    topBike = top_bike(efile=efile) 
    finaltrips = hunded_trips(efile=efile)
    dictionary = build_dict(efile=efile, finaltrips=finaltrips, topBike=topBike)

    with open("./app/sample6.json", "w") as outfile:
        json.dump(dictionary, outfile) 
    
    return dictionary

def transform_df(ene):
    ene["full_date_retiro"] = pd.to_datetime(ene["Fecha_Retiro"] + " " + ene["Hora_Retiro"], format="%d/%m/%Y %H:%M:%S").copy()
    ene["full_date_aribo"] = pd.to_datetime(ene["Fecha_Arribo"] + " " + ene["Hora_Arribo"], format="%d/%m/%Y %H:%M:%S").copy()
    ene["Mes"] = ene["full_date_retiro"].dt.month
    ene["Hora"] = ene["full_date_retiro"].dt.hour
    ene["time_delta"] = round((ene["full_date_aribo"]  - ene["full_date_retiro"]) / np.timedelta64(1,"m"),2)
    ene["Ciclo_Estacion_Retiro"]= ene[["Ciclo_Estacion_Retiro"]].astype(str)
    ene["Ciclo_Estacion_Retiro"] = [i[:-2] for i in ene["Ciclo_Estacion_Retiro"]]
    ene["Bici"]= ene[["Bici"]].astype(str)
    ene["Bici"] = [i[:-2] for i in ene["Bici"]]
    ene["Ciclo_EstacionArribo"] = ene["Ciclo_EstacionArribo"].astype(str)
    ene["viaje"] = ene["Ciclo_Estacion_Retiro"].astype(str)+"-"+ene["Ciclo_EstacionArribo"]
    ene["Genero_Usuario"] = ene["Genero_Usuario"].fillna("X")
    ene = ene.dropna(axis=0).copy()
    return ene

def estaciones_df():
    estaciones = pd.read_csv("./ecobicidata/estaciones-de-ecobici.csv")[["id","name","districtcode","districtname","location_lat","location_lon","stationtype","punto_geo"]]
    estaciones["Ciclo_Estacion_Retiro"] = estaciones["id"].astype("str").copy()
    estaciones["Ciclo_EstacionArribo"] = estaciones["id"].astype("str").copy()
    estaciones_retiro = estaciones.iloc[:,[-2,1,2,3,4,5,6,7]].rename(columns={"name":"name_retiro","districtcode":"districtcode_retiro","districtname":"districtname_retiro","location_lat":"location_lat_retiro","location_lon":"location_lon_retiro","stationtype":"stationtype_retiro","punto_geo":"punto_geo_retiro"}).copy().iloc[:,[0,1,4,5,7]]
    estaciones_arribo = estaciones.iloc[:,[-1,1,2,3,4,5,6,7]].rename(columns={"name":"name_arribo","districtcode":"districtcode_arribo","districtname":"districtname_arribo","location_lat":"location_lat_arribo","location_lon":"location_lon_arribo","stationtype":"stationtype_arribo","punto_geo":"punto_geo_arribo"}).copy().iloc[:,[0,1,4,5,7]]
    return estaciones_retiro, estaciones_arribo

def top_bike(efile):
    top_bike = efile[["Bici"]].groupby("Bici").size().reset_index().sort_values(by=0, ascending=False)["Bici"].to_list()[0]
    bike = efile.loc[ efile["Bici"]==top_bike]
    trips_per_month = bike[["Mes"]].groupby("Mes").size().reset_index().set_index("Mes").rename(columns={0:"Trips"}).transpose().to_dict()
    
    location_lat_retiro = bike["location_lat_retiro"].fillna('19.412182').to_list()
    location_lon_retiro = bike["location_lon_retiro"].fillna('19.412182').to_list()
    location_lat_arribo = bike["location_lat_arribo"].fillna('19.412182').to_list()
    location_lon_arribo = bike["location_lon_arribo"].fillna('19.412182').to_list()

    distances = pd.DataFrame({"location_dist":[geopy.distance.distance((location_lat_retiro[i],location_lon_retiro[i]), (location_lat_arribo[i],location_lon_arribo[i])).km for i in range(len(location_lon_arribo))]})
    
    last_trips = bike.sort_values(by="Fecha_Retiro").tail(100)[["Fecha_Retiro","viaje","location_lat_retiro", "location_lon_retiro","location_lat_arribo","location_lon_arribo"]].reset_index()
    trips_dict = last_trips.transpose().to_dict()

    lastbiketrips = [{
    "location_lat_retiro":trips_dict[i]["location_lat_retiro"],
    "location_lon_retiro":trips_dict[i]["location_lon_retiro"],
    "location_lat_arribo":trips_dict[i]["location_lat_arribo"],
    "location_lon_arribo":trips_dict[i]["location_lon_arribo"],
    } for i in range(len(trips_dict))]

    topBike={
        "trips_per_moth":trips_per_month,
        "total_km":int(distances.sum()),
        "last_trips":lastbiketrips
    }

    return topBike

def hunded_trips(efile):
    listofhundredtrips = efile[["name_arribo","name_retiro","viaje"]].groupby(["name_arribo","name_retiro","viaje"]).size().reset_index().set_index("viaje").sort_values(by=0,ascending=False).head(100).reset_index()

    last_dict = listofhundredtrips.transpose().to_dict()

    finaltrips = [{
        "name_arribo":last_dict[i]["name_arribo"],
        "name_retiro":last_dict[i]["name_retiro"],
        "viaje":last_dict[i][0]
        } for i in range(len(last_dict))]
    
    return finaltrips

def build_dict(efile, finaltrips, topBike):
    all_yearsample = pd.read_csv("./ecobicidata/allyear.csv", index_col=0)
    
    full_year_dataI={
    "trips_per_month":{
        "month":efile[["Mes"]].groupby("Mes").size().reset_index()["Mes"].to_list(),
        "trips":efile[["Mes"]].groupby("Mes").size().reset_index().set_index("Mes").rename(columns={0:"Trips"})["Trips"].to_list()
    },
    "age_distribution":{
        "age":efile[["Edad_Usuario"]].groupby("Edad_Usuario").size().reset_index().set_index("Edad_Usuario").rename(columns={0:"Trips"}).reset_index()["Edad_Usuario"].to_list(),
        "trips":efile[["Edad_Usuario"]].groupby("Edad_Usuario").size().reset_index().set_index("Edad_Usuario").rename(columns={0:"Trips"}).reset_index()["Trips"].to_list()
    },
    "median_trip_time":efile["time_delta"].median(),
    "total_trips":len(efile),
    "median_trips_per_bike":efile[["Bici"]].groupby("Bici").size().reset_index()[0].median(),
    "top_100_trips":{
        "name_arribo":efile[["name_arribo","name_retiro","viaje"]].groupby(["name_arribo","name_retiro","viaje"]).size().reset_index().set_index("viaje").sort_values(by=0,ascending=False).head(100)["name_arribo"].to_list(),
        "name_retiro":efile[["name_arribo","name_retiro","viaje"]].groupby(["name_arribo","name_retiro","viaje"]).size().reset_index().set_index("viaje").sort_values(by=0,ascending=False).head(100)["name_retiro"].to_list(),
        "num_of_trips":efile[["name_arribo","name_retiro","viaje"]].groupby(["name_arribo","name_retiro","viaje"]).size().reset_index().set_index("viaje").sort_values(by=0,ascending=False).head(100)[0].to_list(),
        "dict_of_trips":finaltrips
    },
    "avg_km_per_trip":round(all_yearsample["location_dist"].median(),2),
    "avg_time_per_trip_per_year":all_yearsample[["Mes","time_delta"]].groupby("Mes").median().reset_index().set_index("Mes").transpose().to_dict(),
    "avg_time_delta":all_yearsample[["Mes","time_delta"]].groupby("Mes").median().reset_index().set_index("Mes")["time_delta"].median(),
    "topBike":topBike
    }
    return full_year_dataI

def mergingfiles(month, er, ea):
    first = month.merge(er, on="Ciclo_Estacion_Retiro", how="left").merge(ea, on="Ciclo_EstacionArribo", how="left")
    return first



if __name__ == "__main__":
    m= ["jan","feb","mar","apr","may","jun","jul"]
    main(months=m)