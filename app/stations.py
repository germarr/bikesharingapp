import psycopg2
import psycopg2.extras

dconnector="host=34.66.221.94 port=5432 dbname=ecobici user=postgres password=password"
nameOfTheFile = "estaciones_ecobici"

def stations_data(fileName):
    q= f"""
        select * from public.{fileName}
        """
    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q)
    fulldf = cur.fetchall()

    id=[str(i["id"]) for i in fulldf]
    name = [str(i["name"]) for i in fulldf]
    address = [str(i["address"]) for i in fulldf]
    name = [str(i["name"]) for i in fulldf]
    zipcode = [str(i["zipcode"]) for i in fulldf]
    districtcode = [str(i["districtcode"]) for i in fulldf]
    districtname = [str(i["districtname"]) for i in fulldf]
    location_lat = [float(i["location_lat"]) for i in fulldf]
    location_lon = [float(i["location_lon"]) for i in fulldf]
    stationtype = [str(i["location_lon"]) for i in fulldf]
    
    building_dict= [{
        "id":str(i["id"]),
        "name":str(i["name"]) ,
        "address":str(i["address"]),
        "zipcode":str(i["zipcode"]),
        "districtcode":str(i["districtcode"]),
        "districtname":str(i["districtname"]),
        "location_lat":float(i["location_lat"]),
        "location_lon":float(i["location_lon"]),
        "stationtype":str(i["location_lon"])
    } for i in fulldf]

    stations= {
        "id":id,
        "name":name,
        "address":address,
        "zipcode":zipcode,
        "districtcode":districtcode,
        "districtname":districtname,
        "location_lat":location_lat,
        "location_lon":location_lon,
        "stationtype":stationtype
    }

    return building_dict,stations


def stations_dict(fileName):
    q=f"""
    SELECT 
	    name_retiro,ciclo_estacion_retiro,location_lat_retiro,
	    location_lon_retiro, count(*) as trips
    FROM 
        public.{fileName}
    GROUP BY name_retiro, ciclo_estacion_retiro,location_lat_retiro,
	    location_lon_retiro
    ORDER BY 
        trips desc
    LIMIT 50
    """


    qI=f"""
    SELECT 
	    name_arribo,ciclo_estacionarribo,location_lat_arribo,
	location_lon_arribo, count(*) as trips
    FROM 
        public.{fileName}
    GROUP BY name_arribo,ciclo_estacionarribo,location_lat_arribo,
	    location_lon_arribo
    ORDER BY 
        trips desc
    LIMIT 50
    """

    conn = psycopg2.connect(dconnector)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q)
    fulldf = cur.fetchall()

    connI = psycopg2.connect(dconnector)
    curI = connI.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    curI.execute(qI)
    fulldfI = curI.fetchall()

    name_retiro=[str(i["name_retiro"]) for i in fulldf]
    ciclo_estacion_retiro = [str(i["ciclo_estacion_retiro"]) for i in fulldf]
    location_lat_retiro = [float(i["location_lat_retiro"]) for i in fulldf]
    location_lon_retiro = [float(i["location_lon_retiro"]) for i in fulldf]
    trips = [int(i["trips"]) for i in fulldf]

    building_dict= [{
        "name_retiro":str(i["name_retiro"]) ,
        "ciclo_estacion_retiro":str(i["ciclo_estacion_retiro"]),
        "location_lat_retiro":float(i["location_lat_retiro"]),
        "location_lon_retiro":float(i["location_lon_retiro"]),
        "trips":int(i["trips"])
    } for i in fulldf]

    building_dictI= [{
        "name_arribo":str(i["name_arribo"]) ,
        "ciclo_estacion_arribo":str(i["ciclo_estacionarribo"]),
        "location_lat_arribo":float(i["location_lat_arribo"]),
        "location_lon_arribo":float(i["location_lon_arribo"]),
        "trips":int(i["trips"])
    } for i in fulldfI]

    trip_dict= {
        "name_retiro":name_retiro,
        "ciclo_estacion_retiro":ciclo_estacion_retiro,
        "location_lat_retiro":location_lat_retiro,
        "location_lon_retiro":location_lon_retiro,
        "trips":trips
    }

    return building_dict,building_dictI,trip_dict

if __name__ == "__main__"   :
    stations_data(fileName=nameOfTheFile)