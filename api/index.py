from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import requests
# app instance
app = Flask(__name__)
CORS(app)

@app.route('/api/weather', methods=['POST'])
def send_location():
    data = request.get_json()
    user_location = data.get('userLocation', 'Houston')  # Default to 'Houston' if no location is provided
    units = data.get('units', 'imperial')  # Default to 'imperial' if no unit is provided

    api_key = "03f11aa770bb749257a45573c2754aa1"
    URL = f'http://api.openweathermap.org/data/2.5/weather?q={user_location}&units={units}&appid={api_key}'
    HOURLY_URL = f'http://api.openweathermap.org/data/2.5/forecast?q={user_location}&units={units}&appid={api_key}'

    response = requests.get(url=URL)
    response_hourly = requests.get(url=HOURLY_URL)

    if response.status_code == 200 and response_hourly.status_code == 200:
        weather_data = response.json()
        weather_data_hourly = response_hourly.json()
        
        # Get the UTC datetime and timezone offset
        dt_utc = datetime.utcfromtimestamp(weather_data.get("dt"))
        timezone_offset = timedelta(seconds=weather_data.get("timezone"))
        # Convert UTC datetime to local time
        local_time = dt_utc + timezone_offset
        # Convert UTC datetime to local time and format it in ISO 8601
        local_time_iso = (dt_utc + timezone_offset).isoformat()

        # Defauly data
        city = weather_data.get("name")
        temp = weather_data.get("main", {}).get("temp")
        description = weather_data.get("weather", [{}])[0].get("description", "")
        temp_high = weather_data.get("main", {}).get("temp_max")
        temp_low = weather_data.get("main", {}).get("temp_min")
        
        # Air Conditions
        feels_like = weather_data.get("main", {}).get("feels_like")
        wind = weather_data.get("wind", {}).get("speed")

        # Location's lat & lon
        lat = weather_data.get("coord", {}).get("lat")
        lon = weather_data.get("coord", {}).get("lon")

        # Hourly data
        hourly_data = []
        for i in weather_data_hourly.get('list', [])[:6]: #Fetching the 'hourly' temp up to 6 hours
            hourly_temp = round(i.get('main', {}).get('temp', 0))
            hourly_time = (local_time + timedelta(seconds=i.get('dt'))).strftime('%I %p') # Rounded temp added in 'temp = []'
            hourly_data.append({'temp': hourly_temp, 'time': hourly_time})

    else:
        city = "N/A"
        temp = "N/A"
        description = "N/A"
        local_time_iso = "N/A"
        temp_high = "N/A"
        temp_low = "N/A"
        
        # Air Conditions
        feels_like = "N/A"
        wind = "N/A"

        # Hourly
        hourly_data = []

    return jsonify({
        'city': city,
        'temp': temp,
        'description': description,
        'local_time': local_time_iso,
        'feels_like': feels_like,
        'wind': wind,
        'temp_high': temp_high,
        'temp_low': temp_low,
        'hourly_data': hourly_data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5328, debug=True)

# pip install --upgrade Werkzeug
# pip install --upgrade Flask
# pip install --upgrade pip