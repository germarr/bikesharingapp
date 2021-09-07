import pandas as pd
import numpy as np
import geopy.distance
import psycopg2
import psycopg2.extras
import csv
from datetime import datetime, timedelta
import json

#Links of Interest
#https://www.ecobici.cdmx.gob.mx/es/informacion-del-servicio/open-data
#https://datos.cdmx.gob.mx/dataset/estaciones-de-ecobici/resource/0e5da76b-e551-40ee-9b8c-692167d1fa61
#https://www.postgresqltutorial.com/postgresql-data-types/

def new_ecobici_table(date, dbConnection):
    conn = psycopg2.connect(dbConnection)
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE {date}(
            id SERIAL PRIMARY KEY,
            Genero_Usuario text,
            Edad_Usuario  NUMERIC(4,2),
            Bici VARCHAR(6),
            Ciclo_Estacion_Retiro VARCHAR(4),
            Ciclo_EstacionArribo VARCHAR(4),
            full_date_retiro date,
            full_date_aribo date,
            Mes VARCHAR(4),
            Hora VARCHAR(4),
            time_delta VARCHAR(10),
            viaje VARCHAR(9),
            name_retiro TEXT,
            location_lat_retiro float(8),
            location_lon_retiro float(8),
            name_arribo TEXT,
            location_lat_arribo float(8),
            location_lon_arribo float(8),
            location_dist NUMERIC
        )
        """)

    conn.commit()

#new_ecobici_table(date=fileName, dbConnection=dbC)

#monthdf=pd.read_csv('./ecobicidata/2021-06.csv').sample(20000)

def transform_df(ene):
    ene["full_date_retiro"] = pd.to_datetime(ene["Fecha_Retiro"] + " " + ene["Hora_Retiro"], format="%d/%m/%Y %H:%M:%S").copy()
    ene["full_date_aribo"] = pd.to_datetime(ene["Fecha_Arribo"] + " " + ene["Hora_Arribo"], format="%d/%m/%Y %H:%M:%S").copy()
    ene["Mes"] = ene["full_date_retiro"].dt.month
    ene["Hora"] = ene["full_date_retiro"].dt.hour
    ene["time_delta"] = round((ene["full_date_aribo"]  - ene["full_date_retiro"]) / np.timedelta64(1,"m"),2)
    ene["Ciclo_Estacion_Retiro"]= ene[["Ciclo_Estacion_Retiro"]].astype(str)
    ene["Ciclo_Estacion_Retiro"] = [i for i in ene["Ciclo_Estacion_Retiro"]]
    ene["Bici"]= ene[["Bici"]].astype(str)
    ene["Bici"] = [i[:-2] for i in ene["Bici"]]
    ene["viaje"] = ene["Ciclo_Estacion_Retiro"].astype(str)+"-"+ene["Ciclo_EstacionArribo"].astype(str)
    return ene.iloc[:,[0,1,2,3,6,9,10,11,12,13,14]]

#df = transform_df(ene=monthdf)

def estaciones_df():
    estaciones = pd.read_csv("./ecobicidata/estaciones-de-ecobici.csv")[["id","name","districtcode","districtname","location_lat","location_lon","stationtype","punto_geo"]]
    estaciones["Ciclo_Estacion_Retiro"] = estaciones["id"].astype(str).copy()
    estaciones["Ciclo_EstacionArribo"] = estaciones["id"].copy()
    estaciones_retiro = estaciones.iloc[:,[-2,1,2,3,4,5,6,7]].rename(columns={"name":"name_retiro","districtcode":"districtcode_retiro","districtname":"districtname_retiro","location_lat":"location_lat_retiro","location_lon":"location_lon_retiro","stationtype":"stationtype_retiro","punto_geo":"punto_geo_retiro"}).copy().iloc[:,[0,1,4,5,7]]
    estaciones_arribo = estaciones.iloc[:,[-1,1,2,3,4,5,6,7]].rename(columns={"name":"name_arribo","districtcode":"districtcode_arribo","districtname":"districtname_arribo","location_lat":"location_lat_arribo","location_lon":"location_lon_arribo","stationtype":"stationtype_arribo","punto_geo":"punto_geo_arribo"}).copy().iloc[:,[0,1,4,5,7]]
    return estaciones_retiro, estaciones_arribo

#estaciones_retiro, estaciones_arribo = estaciones_df()

def mergingfiles(month, er, ea):
    first = month.merge(er, on="Ciclo_Estacion_Retiro", how="left").merge(ea, on="Ciclo_EstacionArribo", how="left")
    return first

#exportfile = mergingfiles(month=df, er=estaciones_retiro, ea=estaciones_arribo)

def filetoexport(first, nameOfFile):
    location_lat_retiro = first["location_lat_retiro"].fillna('19.412182').to_list()
    location_lon_retiro = first["location_lon_retiro"].fillna('19.412182').to_list()
    location_lat_arribo = first["location_lat_arribo"].fillna('19.412182').to_list()
    location_lon_arribo = first["location_lon_arribo"].fillna('19.412182').to_list()

    distances = pd.DataFrame({"location_dist":[geopy.distance.distance((location_lat_retiro[i],location_lon_retiro[i]), (location_lat_arribo[i],location_lon_arribo[i])).km for i in range(len(location_lon_arribo))]})
    
    l = pd.concat([first, distances], axis=1, join="inner").iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,19]]
    l["Genero_Usuario"] = l["Genero_Usuario"].fillna("X")

    # l["Ciclo_Estacion_Retiro"] = l["Ciclo_Estacion_Retiro"].fillna(0.0)
    # l["name_retiro"] = l["Ciclo_Estacion_Retiro"].fillna(0.0)
    # l["location_lat_retiro"] = l["location_lat_retiro"].fillna(0.0)
    # l["location_lon_retiro"] = l["location_lon_retiro"].fillna(0.0)
    # l["location_lat_arribo"] = l["location_lat_retiro"].fillna(0.0)
    # l["location_lon_arribo"] = l["location_lon_retiro"].fillna(0.0)
    # l["name_arribo"] = l["name_arribo"].fillna("No Station")
    

    l.dropna(axis=0).to_csv(f'./ecobicidata/{nameOfFile}_resume.csv')
    return l
# = filetoexport(first=exportfile, nameOfFile="testfilejune")

def push_data_to_table(datefile,dbConnection):
    conn = psycopg2.connect(dbConnection)
    cur = conn.cursor()
    with open(f'./ecobicidata/{datefile}_resume.csv', 'r', encoding="utf8") as f:
        # Notice that we don't need the `csv` module.
        next(f) # Skip the header row.
        cur.copy_from(f, f'{datefile}', sep=',')

    conn.commit()

def mainI(dbC, fileName):
    monthdf=pd.read_csv(f'./ecobicidata/{fileName}.csv').sample(20000)
    df = transform_df(ene=monthdf)
    estaciones_retiro, estaciones_arribo = estaciones_df()
    exportfile = mergingfiles(month=df, er=estaciones_retiro, ea=estaciones_arribo)
    l = filetoexport(first=exportfile, nameOfFile=fileName)
    print("File Adjusted!")

    new_ecobici_table(date=fileName, dbConnection=dbC)
    print("Table Created!")

    push_data_to_table(datefile=fileName,dbConnection=dbC)
    print("Data Added to Table!")

if __name__ == "__main__":
    dconnector="host=34.66.221.94 port=5432 dbname=ecobici user=postgres password=password"
    nameOfTheFile = "all_year"
    mainI(dbC=dconnector,fileName=nameOfTheFile)
