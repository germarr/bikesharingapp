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
    listOfDates=[str(i["full_date_retiro"]) for i in fulldf]
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
    
    genderChart= {
        "genero":listOfDates,
        "tripsGender":listOfTrips
    }
    
    return genderChart

if __name__ == "__main__":
    total_trips_per_day()