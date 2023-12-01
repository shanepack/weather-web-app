from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests
import json
import openai 

def load_api_keys(secrets_file="../../weather-web-app/secrets.json"):
    with open(secrets_file) as f:
        secrets = json.load(f)
    return secrets

api_keys = load_api_keys()
openweather_api_key = api_keys['OPENWEATHER_API_KEY']
openai.api_key = api_keys['OPENAI_API_KEY']

app = Flask(__name__)
CORS(app)

@app.route('/api/weather', methods=['POST'])
def send_location():
    data = request.get_json()
    user_location = data.get('userLocation', 'Houston')
    units = data.get('units', 'imperial')

    # First, use the weather API to get basic weather info and coordinates
    weather_URL = f'http://api.openweathermap.org/data/2.5/weather?q={user_location}&units={units}&appid={openweather_api_key}'
    weather_response = requests.get(url=weather_URL)
    if not weather_response.ok:
        return jsonify({'error': 'Failed to retrieve weather data'}), weather_response.status_code

    weather_data = weather_response.json()
    city = weather_data.get("name", "N/A")
    temp = weather_data.get("main", {}).get("temp", "N/A")
    description = weather_data.get("weather", [{}])[0].get("description", "N/A")
    coords = weather_data.get("coord", {})

    # If coordinates are available, use the onecall API for the 7-day forecast
    if coords:
        lat, lon = coords.get("lat"), coords.get("lon")
        onecall_URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units={units}&appid={api_key}'
        onecall_response = requests.get(url=onecall_URL)
        if onecall_response.ok:
            onecall_data = onecall_response.json()
            forecast_data = process_forecast_data(onecall_data.get('daily', [])[0:7])
        else:
            forecast_data = []
    else:
        forecast_data = []

    return jsonify({
        'city': city,
        'temp': temp,
        'description': description,
        'forecast': forecast_data
    })

def process_forecast_data(daily_forecast):
    return [
        {
            'date': datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d'),
            'temp': day['temp']['day'],
            'rain_chance': day.get('pop', 0) * 100
        } for day in daily_forecast
    ]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5328, debug=True)
