import os
import sys
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Utils.database_utils import initialize_database, fetch_all_data, save_weather_data
from Utils.weather_utils import fetch_weather_data
from Utils.city_utils import load_cities, get_random_city
from Utils.something_useful import train_clustering_model, suggest_activity

DB_NAME = "../data/test_weather_data.db"  # Test database
WORLD_CITIES_FILE = "../data/worldcities.csv"


class TestWeatherService(unittest.TestCase):
    def setUp(self):
        """Set up a clean database for each test."""
        initialize_database(DB_NAME)

    def test_database_empty(self):
        """Test that the database is empty after initialization."""
        data = fetch_all_data(DB_NAME)
        self.assertEqual(len(data), 0, "Database should be empty after initialization.")

    def test_city_selection(self):
        """Test loading cities and selecting a random city."""
        cities = load_cities(WORLD_CITIES_FILE)
        self.assertGreater(len(cities), 0, "Cities list should not be empty.")
        random_city = get_random_city(cities)
        self.assertIn("city", random_city, "Random city should have a 'city' field.")
        self.assertIn("country", random_city, "Random city should have a 'country' field.")

    def test_fetch_weather_data(self):
        """Test fetching weather data for a valid city."""
        weather_data = fetch_weather_data(lat=40.7128, lon=-74.0060)  # New York
        self.assertEqual(len(weather_data), 30, "Should fetch 30 days of weather data.")
        self.assertIn("date", weather_data[0], "Weather data should include 'date'.")
        self.assertIn("max_temp", weather_data[0], "Weather data should include 'max_temp'.")
        self.assertIn("min_temp", weather_data[0], "Weather data should include 'min_temp'.")

    def test_suggest_activity(self):
        """Test activity suggestions for various temperatures."""
        avg_temps = [10, 20, 30]
        clustering_model, scaler = train_clustering_model(avg_temps, n_clusters=3) 
        activities = [suggest_activity(temp, clustering_model, scaler) for temp in avg_temps]
        self.assertEqual(len(activities), len(avg_temps), "Should suggest activities for all temperatures.")
        self.assertIn("Stay Indoors", activities)
        self.assertIn("Outdoor Walk", activities)

    def test_save_weather_data(self):
        """Test saving weather data to the database."""
        weather_data = [{"date": "2024-12-01", "max_temp": 25.0, "min_temp": 15.0}]
        clustering_model, scaler = train_clustering_model([25.0], n_clusters=1)  
        save_weather_data(DB_NAME, "Test City", "Test Country", weather_data, clustering_model, scaler)
        data = fetch_all_data(DB_NAME)
        self.assertEqual(len(data), 1, "One record should be saved in the database.")
        self.assertEqual(data[0][1], "Test City", "Saved city should match the input.")
        self.assertEqual(data[0][2], "Test Country", "Saved country should match the input.")


if __name__ == "__main__":
    unittest.main()
