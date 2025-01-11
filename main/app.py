import os
import sys
from flask import Flask, jsonify, render_template, redirect, url_for
from weather import generate_and_save_weather_data


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Utils.database_utils import fetch_all_data

DB_NAME = "data/weather_data.db"

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET'])
def home():
    """Redirect to the dashboard by default."""
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Render the weather dashboard with summary cards."""
    try:
        data = fetch_all_data(DB_NAME)

        # Calculate summary statistics
        total_records = len(data)-5
        avg_temp = round(sum(row[6] for row in data) / total_records, 2)
        hottest_day = max(data, key=lambda x: x[4])  # Max Temp
        coldest_day = min(data, key=lambda x: x[5])  # Min Temp
        activities = [row[7] for row in data]
        most_frequent_activity = max(set(activities), key=activities.count)

        # Pass all data to the template
        return render_template(
            'dashboard.html',
            weather_data=data,
            total_records=total_records,
            avg_temp=avg_temp,
            hottest_day=hottest_day[4],  # Max Temp
            coldest_day=coldest_day[5],  # Min Temp
            most_frequent_activity=most_frequent_activity
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/data', methods=['GET'])
def get_weather_data():
    """Fetch all weather data from the database."""
    try:
        data = fetch_all_data(DB_NAME)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Check if the API is running."""
    return jsonify({"status": "API is running successfully!"})

if __name__ == '__main__':
    # Clear old data and generate new weather data
    print("Refreshing the weather database...")
    generate_and_save_weather_data()

    # Start the Flask application
    app.run(host='0.0.0.0', port=5000)
