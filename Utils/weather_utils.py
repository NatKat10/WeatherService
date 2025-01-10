#this file fatching min max temertures for the past 30 days for specific lat and lon that we get from the csv file, we use open-meteo api for this
import requests

def fetch_weather_data(lat, lon):
    #Fetch weather data for the past 30 days using Open-Meteo API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&past_days=30&timezone=auto"

    response = requests.get(url)#sending an http get request to the api 
    if response.status_code == 200:
        data = response.json()#if successful i parse json response
        daily_data = []
        for i, date in enumerate(data["daily"]["time"]):#provides both the index and the date 
            #for each date it creates a dictionary with date, max temp and min temp 
            daily_data.append({
                "date": date,
                "max_temp": data["daily"]["temperature_2m_max"][i],
                "min_temp": data["daily"]["temperature_2m_min"][i],
            })
        daily_data = daily_data[:30]#limits to 30 records 
        return daily_data
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}, {response.text}")

if __name__ == "__main__":#just for thesting
    weather_data = fetch_weather_data(lat=40.7128, lon=-74.0060)  
    print(weather_data)