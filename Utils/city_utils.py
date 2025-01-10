#This file handles the selection of a random city from the worldcities.csv

import csv
import random

def load_cities(file_path):
    #load the city data from the csv file to choose a random one later 
    cities = [] # loads all city data into a list 
    with open(file_path, mode="r", encoding="utf-8") as file:# file is data/worldcities.csv
        reader = csv.DictReader(file)
        for row in reader:
            try:#extracting the city data
                city = row["city"]
                country = row["country"]
                latitude = float(row["lat"])
                longitude = float(row["lng"])
                cities.append({
                    "city": city,
                    "country": country,
                    "latitude": latitude,
                    "longitude": longitude,
                })
            except (ValueError, KeyError) as e:
                # Skip the problematic row without adding it to cities list 
                print(f" invalid row: {row}. Error: {e}")
                
    return cities


def get_random_city(cities):
    #select random city from the list 
    return random.choice(cities)


if __name__ == "__main__":# Testing the functions in city_utils.py
    cities = load_cities("data/worldcities.csv")
    print( cities[:5])
    random_city = get_random_city(cities)
    print(random_city)