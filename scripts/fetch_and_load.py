import requests
import sqlite3

# USGS API for earthquakes in the past day
URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
DB_PATH = "earthquakes.db"

def create_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    with open("sql/create_tables.sql", "r") as f:
        sql_script = f.read()
    conn = create_connection()
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

def fetch_earthquake_data():
    response = requests.get(URL)
    return response.json()["features"]

def insert_data(features):
    conn = create_connection()
    cursor = conn.cursor()
    
    for f in features:
        props = f["properties"]
        coords = f["geometry"]["coordinates"]
        quake_id = f["id"]
        time = int(props["time"] / 1000)  # convert ms to seconds
        magnitude = props["mag"]
        place = props["place"]
        longitude, latitude, depth = coords
        
        cursor.execute("""
            INSERT OR REPLACE INTO earthquakes (id, time, latitude, longitude, depth, magnitude, place)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (quake_id, time, latitude, longitude, depth, magnitude, place))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    data = fetch_earthquake_data()
    insert_data(data)
    print(f"Inserted {len(data)} earthquakes into the database.")
