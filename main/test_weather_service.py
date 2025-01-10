import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from Utils.weather_utils import fetch_weather_data
from Utils.database_utils import initialize_database, fetch_all_data
from Utils.something_useful import prepare_data, train_model, predict_next_days, suggest_activity, train_clustering_model

DB_NAME = "data/weather_data.db"

class TestWeatherService(unittest.TestCase):

    def setUp(self):
        """Set up a fresh database for testing."""
        initialize_database(DB_NAME)

    @patch('Utils.weather_utils.fetch_weather_data')
    def test_empty_api_response(self, mock_fetch):
        """Test handling of empty API response."""
        mock_fetch.return_value = []  # Simulate empty API response
        with self.assertRaises(ValueError):
            weather_data = fetch_weather_data(0, 0)  # Call with dummy coordinates
            self.assertEqual(len(weather_data), 0)

    def test_database_empty(self):
        """Test behavior when the database is empty."""
        data = fetch_all_data(DB_NAME)
        self.assertEqual(len(data), 0, "Database should be empty initially.")

    def test_temperature_extremes(self):
        """Test logical activity suggestions for extreme temperatures."""
        mock_temps = [50, -30, 25, 10]  # Simulated extreme temperatures
        clustering_model, scaler = train_clustering_model(mock_temps, n_clusters=4)

        activities = [suggest_activity(temp, clustering_model, scaler) for temp in mock_temps]
        self.assertEqual(activities[0], "Beach Day")
        self.assertEqual(activities[1], "Stay Indoors")
        self.assertIn(activities[2], ["Running", "Outdoor Walk"])

    def test_predictions_stored_correctly(self):
        """Test that predictions are saved correctly without overwriting."""
        mock_data = [(1, 'City', 'Country', '2025-01-01', 10, 5, 7.5, 'Stay Indoors')]
        X, y = prepare_data(mock_data)
        model = train_model(X, y)
        predictions = predict_next_days(model, start_day=2, num_days=5)

        self.assertEqual(len(predictions), 5, "Should generate 5 predictions.")

    @patch('Utils.weather_utils.fetch_weather_data')
    def test_invalid_city_data(self, mock_fetch):
        """Test behavior when city data is invalid."""
        mock_fetch.return_value = [{'date': '2025-01-01', 'max_temp': None, 'min_temp': None}]
        with self.assertRaises(ValueError):
            fetch_weather_data(0, 0)

    def test_empty_clusters(self):
        """Test handling of empty clusters."""
        mock_temps = [25, 25, 25]  # All temperatures are the same
        clustering_model, scaler = train_clustering_model(mock_temps, n_clusters=4)

        empty_clusters = []
        for i in range(clustering_model.n_clusters):
            cluster_temps = [temp for temp in mock_temps if clustering_model.predict(scaler.transform([[temp]]))[0] == i]
            if not cluster_temps:
                empty_clusters.append(i)

        self.assertGreater(len(empty_clusters), 0, "Should detect empty clusters.")

    def tearDown(self):
        """Clean up after tests."""
        import os
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)

if __name__ == "__main__":
    unittest.main()
