import os
import sys
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Utils.database_utils import initialize_database, save_weather_data, save_predictions, fetch_all_data
from Utils.weather_utils import fetch_weather_data
from Utils.city_utils import load_cities, get_random_city
from Utils.something_useful import prepare_data, train_model, predict_next_days, train_clustering_model, suggest_activity

DB_NAME = "data/weather_data.db"
WORLD_CITIES_FILE = "data/worldcities.csv"

def generate_and_save_weather_data():
    """Generate and save new weather data with predictions."""
    try:
        # Initialize database
        initialize_database(DB_NAME)

        # Load cities and fetch random city
        cities = load_cities(WORLD_CITIES_FILE)
        random_city = get_random_city(cities)
        city, country, lat, lon = random_city["city"], random_city["country"], random_city["latitude"], random_city["longitude"]
        print(f"Selected city: {city}, {country} (Lat: {lat}, Lon: {lon})")

        # Fetch weather data
        weather_data = fetch_weather_data(lat=lat, lon=lon)
        if not weather_data:
            raise ValueError("No weather data returned from the API.")

        # Train clustering model
        avg_temps = [day["max_temp"] for day in weather_data]
        clustering_model, scaler = train_clustering_model(avg_temps, n_clusters=5)

        # Save weather data with activity suggestions
        save_weather_data(DB_NAME, city, country, weather_data, clustering_model, scaler)
        print(f"Weather data for {city} saved successfully!")

        # Train prediction model
        data = fetch_all_data(DB_NAME)
        X, y = prepare_data(data)
        model = train_model(X, y)
        predictions = predict_next_days(model, len(X) + 1, 5)

        # Save predictions with activity suggestions
        save_predictions(DB_NAME, city, country, predictions, clustering_model, scaler)

    except Exception as e:
        print(f"Error in generate_and_save_weather_data: {e}")
        traceback.print_exc()

def main():
    """Main execution function."""
    generate_and_save_weather_data()

if __name__ == "__main__":
    main()
