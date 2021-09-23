import psycopg2
import psycopg2.extras
import csv
import pandas as pd
from datetime import datetime, timedelta
import json
 
dconnector="host=173.255.226.165 port=5432 dbname=apidata user=gmarr password=password"
nameOfTheFile = "smalldb"

def get_cards(cardsdate):
    q1=f"""
        with worktable as (SELECT *, 
            EXTRACT(Year from full_date_retiro) as trip_year,
            EXTRACT(month from full_date_retiro) as trip_month,
            EXTRACT(day from full_date_retiro) as trip_day,
            CASE 
                WHEN CAST(time_delta as float) >= 45.0 AND CAST(time_delta as float)<= 60.0 THEN 14.47
                WHEN CAST(time_delta as float) > 60.0 then (4.47+ ((CAST(time_delta as float)/60)*44))
                ELSE 0 END as revenue
        FROM public.smalldb )
 
        SELECT
            COUNT(*) as total_trips, 
            PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY CAST(time_delta as float))as avg_time,
            ROUND(CAST(PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY CAST(location_dist as float)) as numeric),2) as avg_distance,
            ROUND(SUM(location_dist)) as total_kms,
            ROUND(SUM(revenue)) as total_revenue
        from worktable
        where {cardsdate}
        """
    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q1)
    fulldf = cur.fetchall()
    df=[{
        "total_trips":float(i['total_trips']),
        "avg_time":round(float(i["avg_time"]),2),
        "avg_distance":float(i['avg_distance']),
        "total_kms":int(i['total_kms']),
        "total_revenue":int(i['total_revenue'])
    } for i in fulldf]
    dfII = [df[i] for i,x in enumerate(df)]
    return dfII
 
cards = get_cards(cardsdate='trip_year = 2021 AND trip_month = 4 AND trip_day = 19')

def gender_dist(cardsdate):
    q1=f"""
    with worktable as (SELECT *, 
            EXTRACT(Year from full_date_retiro) as trip_year,
            EXTRACT(month from full_date_retiro) as trip_month,
            EXTRACT(day from full_date_retiro) as trip_day,
            CASE 
                WHEN CAST(time_delta as float) >= 45.0 AND CAST(time_delta as float)<= 60.0 THEN 14.47
                WHEN CAST(time_delta as float) > 60.0 then (4.47+ ((CAST(time_delta as float)/60)*44))
                ELSE 0 END as revenue
        FROM public.smalldb)

        SELECT * FROM (SELECT genero_usuario, count(*) as counts, 
			   (SELECT COUNT(*) FROM worktable where {cardsdate})as total
                from worktable
                where {cardsdate}
                group by genero_usuario) as tb1
        """
    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q1)
    fulldf = cur.fetchall()
    df=[{
        "genero_usuario":str(i['genero_usuario']),
        "counts":round(float((i["counts"]/i["total"])*100),2)
    } for i in fulldf]
    dfII = [df[i] for i,x in enumerate(df)]
    return dfII


def hourly_trips(cardsdate):
    q1=f"""
    with worktable as (SELECT *, 
            EXTRACT(Year from full_date_retiro) as trip_year,
            EXTRACT(month from full_date_retiro) as trip_month,
            EXTRACT(day from full_date_retiro) as trip_day,
            CASE 
                WHEN CAST(time_delta as float) >= 45.0 AND CAST(time_delta as float)<= 60.0 THEN 14.47
                WHEN CAST(time_delta as float) > 60.0 then (4.47+ ((CAST(time_delta as float)/60)*44))
                ELSE 0 END as revenue
        FROM public.smalldb )

    SELECT CAST(hora as float) as hourly, count(*) as counts from worktable
    where {cardsdate}
    group by hourly
    order by hourly 
    """

    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q1)
    fulldf = cur.fetchall()
    hours=[float(i["hourly"]) for i in fulldf]
    trips_per_hour = [float(i["counts"]) for i in fulldf]
    
    tripsChart= {
        "hourly":hours,
        "tripsPerHour":trips_per_hour
    }

    return tripsChart

def hourly_trips(cardsdate):
    q1=f"""
    with worktable as (SELECT *, 
            EXTRACT(Year from full_date_retiro) as trip_year,
            EXTRACT(month from full_date_retiro) as trip_month,
            EXTRACT(day from full_date_retiro) as trip_day,
            CASE 
                WHEN CAST(time_delta as float) >= 45.0 AND CAST(time_delta as float)<= 60.0 THEN 14.47
                WHEN CAST(time_delta as float) > 60.0 then (4.47+ ((CAST(time_delta as float)/60)*44))
                ELSE 0 END as revenue
        FROM public.smalldb )

    SELECT CAST(hora as float) as hourly, count(*) as counts from worktable
    where {cardsdate}
    group by hourly
    order by hourly 
    """

    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q1)
    fulldf = cur.fetchall()
    hours=[float(i["hourly"]) for i in fulldf]
    trips_per_hour = [float(i["counts"]) for i in fulldf]
    
    tripsChart= {
        "hourly":hours,
        "tripsPerHour":trips_per_hour
    }

    return tripsChart

def top_routes(cardsdate):
    q1=f"""
        with worktable as (SELECT *, 
                    EXTRACT(Year from full_date_retiro) as trip_year,
                    EXTRACT(month from full_date_retiro) as trip_month,
                    EXTRACT(day from full_date_retiro) as trip_day,
                    CASE 
                        WHEN CAST(time_delta as float) >= 45.0 AND CAST(time_delta as float)<= 60.0 THEN 14.47
                        WHEN CAST(time_delta as float) > 60.0 then (4.47+ ((CAST(time_delta as float)/60)*44))
                        ELSE 0 END as revenue
                FROM public.smalldb )

        SELECT name_retiro, name_arribo, count(*) as counts
        from worktable
        where {cardsdate}
        group by name_retiro, name_arribo
        order by counts desc
        limit 10
        """

    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q1)
    fulldf = cur.fetchall()

    name_retiro=[str(i["name_retiro"]) for i in fulldf]
    name_arribo=[str(i["name_arribo"]) for i in fulldf]
    counts = [float(i["counts"]) for i in fulldf]
    
    tripsChart= {
        "name_retiro":name_retiro,
        "name_arribo":name_arribo,
        "counts":counts
    }

    return tripsChart

def top_locations(cardsdate):
    q1=f"""with worktable as (SELECT *, 
            EXTRACT(Year from full_date_retiro) as trip_year,
            EXTRACT(month from full_date_retiro) as trip_month,
            EXTRACT(day from full_date_retiro) as trip_day,
            CASE 
                WHEN CAST(time_delta as float) >= 45.0 AND CAST(time_delta as float)<= 60.0 THEN 14.47
                WHEN CAST(time_delta as float) > 60.0 then (4.47+ ((CAST(time_delta as float)/60)*44))
                ELSE 0 END as revenue
        FROM public.smalldb )

        SELECT ciclo_estacion_retiro, ciclo_estacionarribo, 
        location_lat_retiro, location_lon_retiro, location_lat_arribo, location_lon_arribo, count(*) as counts
        from worktable 
        WHERE ciclo_estacion_retiro = (
            SELECT ciclo_estacion_retiro FROM (SELECT ciclo_estacion_retiro, COUNT(*) as counts
            from worktable
            where {cardsdate} 
            group by ciclo_estacion_retiro
            order by counts desc
            LIMIT 1) as tb1) AND {cardsdate} 
        group by ciclo_estacion_retiro, ciclo_estacionarribo, location_lat_retiro, location_lon_retiro, location_lat_arribo, location_lon_arribo
        order by counts desc
        limit 40
        """

    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q1)
    fulldf = cur.fetchall()

    name_retiro=[[float(i["location_lat_retiro"]),float(i["location_lon_retiro"])] for i in fulldf]
    name_arribo=[[float(i["location_lat_arribo"]),float(i["location_lon_arribo"])] for i in fulldf]
    
    tripsChart= {
        "name_retiro":name_retiro,
        "name_arribo":name_arribo
    }

    return tripsChart


def stations():
    q1=f"""
        with worktable as (SELECT *, 
                EXTRACT(Year from full_date_retiro) as trip_year,
                EXTRACT(month from full_date_retiro) as trip_month,
                EXTRACT(day from full_date_retiro) as trip_day,
                CASE 
                    WHEN CAST(time_delta as float) >= 45.0 AND CAST(time_delta as float)<= 60.0 THEN 14.47
                    WHEN CAST(time_delta as float) > 60.0 then (4.47+ ((CAST(time_delta as float)/60)*44))
                    ELSE 0 END as revenue
            FROM public.smalldb )
            SELECT ciclo_estacion_retiro, name_retiro, location_lat_retiro, location_lon_retiro from worktable
            GROUP BY ciclo_estacion_retiro, name_retiro, location_lat_retiro, location_lon_retiro
            ORDER BY CAST(ciclo_estacion_retiro AS int) ASC
        """

    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q1)
    fulldf = cur.fetchall()

    stations=[[float(i["location_lat_retiro"]),float(i["location_lon_retiro"])] for i in fulldf]
    
    tripsChart= {
        "stations":stations
    }

    return tripsChart

print(top_locations(cardsdate='trip_year = 2021 AND trip_month = 4 AND trip_day = 19'))

