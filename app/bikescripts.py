import psycopg2
import psycopg2.extras

dconnector="host=34.66.221.94 port=5432 dbname=ecobici user=postgres password=password"
nameOfTheFile = "ecobici_may"

def total_trips_per_day(fileName):
    q= f"""
        SELECT 
            full_date_retiro, COUNT(*) as viajes_totales 
        FROM 
            public.{fileName} 
        WHERE 
            full_date_retiro >= '2021-07-01'
        group by 
            full_date_retiro 
        order by 
            full_date_retiro
        """
    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q)
    fulldf = cur.fetchall()
    listOfDates=[str(i["full_date_retiro"])[5:] for i in fulldf]
    listOfTrips = [int(i["viajes_totales"]) for i in fulldf]
    
    tripsChart= {
        "listOfDates":listOfDates,
        "listOfTrips":listOfTrips
    }
    
    return tripsChart

def gender_trips(fileName):
    q= f"""
        SELECT 
            genero_usuario, COUNT(*) as pct
        FROM 
            public.{fileName} 
        WHERE 
            full_date_retiro >= '2021-07-01'
        GROUP BY genero_usuario
        """
    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q)
    fulldf = cur.fetchall()
    listOfDates=[str(i["genero_usuario"]) for i in fulldf]
    listOfTrips = [int(i["pct"]) for i in fulldf]

    total = 0
    list1 = listOfTrips
    
    # Iterate each element in list
    # and add them in variable total
    for ele in range(0, len(list1)):
        total = total + list1[ele]
    
    get_pct = [round((i/total)*100) for i in listOfTrips]
    
    genderChart= {
        "genero":listOfDates,
        "tripsGender":get_pct
    }
    
    return genderChart

def trips_on_week(fileName):
    q= f"""
    SELECT 
        EXTRACT(ISODOW FROM full_date_aribo) as dia_semana, count(*) as trips_per_day
    FROM 
        public.{fileName} 
    WHERE 
        full_date_retiro >= '2021-07-01'
    GROUP BY
        dia_semana
    ORDER BY
        dia_semana
        """
    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q)
    fulldf = cur.fetchall()
    dia_semana=[str(i["dia_semana"]) for i in fulldf]
    trips_per_day = [int(i["trips_per_day"]) for i in fulldf]
    
    weekChart= {
        "dia_semana":dia_semana,
        "trips_per_day":trips_per_day
    }

    return weekChart

def cards_stats(fileName):
    q= f"""
    SELECT 
	    PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY CAST(time_delta AS double precision)) as median_trips
    FROM 
	    public.{fileName}
    WHERE 
        full_date_retiro >= '2021-07-01'
    """

    qI=f"""
    SELECT 
	    ROUND(CAST(float8 (PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY location_dist)) as numeric), 2) as median_distance
    FROM 
        public.{fileName}
    WHERE 
        full_date_retiro >= '2021-07-01'
    """

    qII =f"""
    SELECT 
	    name_retiro, count(*) as trip_inits
    FROM 
        public.{fileName}
    WHERE 
        full_date_retiro >= '2021-07-01'
    GROUP BY 
        name_retiro
    ORDER BY 
        trip_inits desc
    LIMIT 1
    """
    
    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q)
    fulldf = cur.fetchall()
    
    connI = psycopg2.connect(dconnector)
    curI = connI.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    curI.execute(qI)
    fulldfI = curI.fetchall()
    
    connII = psycopg2.connect(dconnector)
    curII = connII.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    curII.execute(qII)
    fulldfII = curII.fetchall()

    medianTrips=[float(i["median_trips"]) for i in fulldf]
    
    medianDistance=[float(i["median_distance"]) for i in fulldfI]
    
    statationCounTrips=[int(i["trip_inits"]) for i in fulldfII]
    stationName = [str(i["name_retiro"]) for i in fulldfII]

    weekChart= {
        "median_trips":medianTrips,
        "median_distance":medianDistance,
        "popularStation":{
            "stationTrips":statationCounTrips,
            "nameStation":stationName
        }
    }

    return weekChart

def trip_hours(fileName):
    q= f"""
    SELECT CAST(hora as text), trips_on_hour FROM(SELECT 
	CAST(hora as int), count(*) as trips_on_hour
    FROM public.{fileName}
    WHERE full_date_retiro >= '2021-07-01'
    GROUP BY hora
    ORDER BY hora asc) as tb1
    """
    
    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q)
    fulldf = cur.fetchall()

    hourOfTrip=[str(i["hora"]) for i in fulldf]
    amountofTrips = [int(i["trips_on_hour"]) for i in fulldf]

    tripsHour= {
        "hora":hourOfTrip,
        "amountOfTrips":amountofTrips
    }

    return tripsHour


if __name__ == "__main__":
    total_trips_per_day()