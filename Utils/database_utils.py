#this file handles all things that are related to the sqlite database 
import sqlite3
from Utils.something_useful import suggest_activity
import datetime


def initialize_database(db_name="weather_data.db"):# initializing a database 
    #connects to the db or creates if not exist
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS weather")#if the table exist i drop it so we can start with 30 new records 
    #creates the table 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        country TEXT,
        date TEXT,
        max_temp REAL,
        min_temp REAL,
        avg_temp REAL,
        activity TEXT
    )
    """)
    #commit the changes and close the connection 
    conn.commit()
    conn.close()


def save_weather_data(db_name, city, country, weather_data, clustering_model,scaler):
    #connect to database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weather")  # Clear old data

    for day in weather_data:#go over the data i got 
        avg_temp = (day["max_temp"] + day["min_temp"]) / 2#calculating the average temp
        #use the clustering model for the activity column (from something_useful.py)
        activity = suggest_activity(avg_temp, clustering_model,scaler)
        #insert all relevant data to table, with the suggested activity 
        cursor.execute("""
        INSERT INTO weather (city, country, date, max_temp, min_temp, avg_temp, activity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (city, country, day["date"], round(day["max_temp"], 2), round(day["min_temp"], 2), round(avg_temp, 2), activity))

    conn.commit()
    conn.close()


def save_predictions(db_name, city, country, predictions, clustering_model,scaler):
    #for my something useful i did a prediction for the next 5 days 
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for prediction in predictions:
        #go over the predictions and choose the correct activity 
        activity = suggest_activity(prediction["avg_temp"], clustering_model,scaler)

        #inserting the prediction as the 5 last rows in the database
        cursor.execute("""
        INSERT INTO weather (city, country, date, max_temp, min_temp, avg_temp, activity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (f"{city} (Prediction)", f"{country} ", prediction["date"], 
              round(prediction["max_temp"], 2), round(prediction["min_temp"], 2), 
              round(prediction["avg_temp"], 2), activity))

    conn.commit()
    conn.close()


def fetch_all_data(db_name="weather_data.db"):
    #Fetch all stored weather data from the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()#cursor object to execute sql queries
    cursor.execute("SELECT * FROM weather")
    rows = cursor.fetchall()#returns rows as list of tubles 
    conn.close()
    return rows
