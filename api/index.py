# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from datetime import datetime, timedelta
# import requests
# # app instance
# app = Flask(__name__)
# CORS(app)

# @app.route('/api/weather', methods=['POST'])
# def send_location():
#     data = request.get_json()
#     user_location = data.get('userLocation', 'Houston')  # Default to 'Houston' if no location is provided
#     units = data.get('units', 'imperial')  # Default to 'imperial' if no unit is provided

#     api_key = "03f11aa770bb749257a45573c2754aa1"
#     URL = f'http://api.openweathermap.org/data/2.5/weather?q={user_location}&units={units}&appid={api_key}'

#     response = requests.get(url=URL)

#     if response.status_code == 200:
#         weather_data = response.json()
#         city = weather_data.get("name")
#         temp = weather_data.get("main", {}).get("temp")
#         description = weather_data.get("weather", [{}])[0].get("description", "")

#         # Get the UTC datetime and timezone offset
#         dt_utc = datetime.utcfromtimestamp(weather_data.get("dt"))
#         timezone_offset = timedelta(seconds=weather_data.get("timezone"))
#         # Convert UTC datetime to local time
#         local_time = dt_utc + timezone_offset
#         # Convert UTC datetime to local time and format it in ISO 8601
#         local_time_iso = (dt_utc + timezone_offset).isoformat()

#     else:
#         city = "N/A"
#         temp = "N/A"
#         description = "N/A"
#         local_time_iso = "N/A"

#     return jsonify({
#         'city': city,
#         'temp': temp,
#         'description': description,
#         'local_time': local_time_iso
#     })

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5328, debug=True)

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from datetime import datetime
# import requests

# app = Flask(__name__)
# CORS(app)

# @app.route('/api/weather', methods=['POST'])
# def send_location():
#     data = request.get_json()
#     user_location = data.get('userLocation', 'Houston')  # Default to 'Houston' if no location is provided
#     units = data.get('units', 'imperial')  # Default to 'imperial' if no unit is provided
    
#     api_key = "ee4fc84f29103a26ae2400ec30a26411"

#     # Geocoding API to get latitude and longitude
#     geo_URL = f'http://api.openweathermap.org/geo/1.0/direct?q={user_location}&appid={api_key}'
#     geo_response = requests.get(url=geo_URL)
#     if not geo_response.ok or not geo_response.json():
#         return jsonify({'error': 'Location not found or invalid response from geocoding API'}), 404

#     lat, lon = geo_response.json()[0]['lat'], geo_response.json()[0]['lon']

#     # One Call API for current weather and 7-day forecast
#     weather_URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units={units}&appid={api_key}'
#     weather_response = requests.get(url=weather_URL)
#     if not weather_response.ok:
#         return jsonify({'error': 'Failed to retrieve weather data'}), weather_response.status_code

#     weather_data = weather_response.json()
#     current_weather = weather_data.get("current", {})
#     city = user_location  # Using user input as city name
#     temp = current_weather.get("temp")
#     description = current_weather.get("weather", [{}])[0].get("description", "")
#     local_time_iso = datetime.utcfromtimestamp(current_weather.get("dt")).isoformat()

#     daily_forecast = weather_data.get('daily', [])[0:7]
#     forecast_data = [
#         {
#             'date': datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d'),
#             'temp': day['temp']['day'],
#             'rain_chance': day.get('pop', 0) * 100
#         } for day in daily_forecast
#     ]

#     return jsonify({
#         'city': city,
#         'temp': temp,
#         'description': description,
#         'local_time': local_time_iso,
#         'forecast': forecast_data
#     })

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5328, debug=True)

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/weather', methods=['POST'])
def send_location():
    data = request.get_json()
    user_location = data.get('userLocation', 'Houston')
    units = data.get('units', 'imperial')
    api_key = "ee4fc84f29103a26ae2400ec30a26411"

    # First, use the weather API to get basic weather info and coordinates
    weather_URL = f'http://api.openweathermap.org/data/2.5/weather?q={user_location}&units={units}&appid={api_key}'
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
