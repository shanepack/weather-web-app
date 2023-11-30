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
#     HOURLY_URL = f'http://api.openweathermap.org/data/2.5/forecast?q={user_location}&units={units}&appid={api_key}'
#     WEEk_URL = f'https://api.openweathermap.org/data/2.5/forecast/daily?q={user_location}&units={units}&appid={api_key}'

#     response = requests.get(url=URL)
#     response_hourly = requests.get(url=HOURLY_URL)
#     response_week = requests.get(url=WEEk_URL)

#     # print('\n\n\nWeather API response:', response.json())
#     # print('\n\n\nHourly API response:', response_hourly.json())
#     print('\n\n\nWeek API response:', response_week.json())

#     if response.status_code == 200 and response_hourly.status_code == 200 and response_week.status_code == 200:
#         weather_data = response.json()
#         weather_data_hourly = response_hourly.json()
#         weather_data_week = response_week.json()
        
#         # Get the UTC datetime and timezone offset
#         dt_utc = datetime.utcfromtimestamp(weather_data.get("dt"))
#         timezone_offset = timedelta(seconds=weather_data.get("timezone"))
#         # Convert UTC datetime to local time
#         local_time = dt_utc + timezone_offset
#         # Convert UTC datetime to local time and format it in ISO 8601
#         local_time_iso = (dt_utc + timezone_offset).isoformat()

#         # Defauly data
#         city = weather_data.get("name")
#         temp = weather_data.get("main", {}).get("temp")
#         description = weather_data.get("weather", [{}])[0].get("description", "")
        
        
#         # Air Conditions
#         feels_like = weather_data.get("main", {}).get("feels_like")
#         wind = weather_data.get("wind", {}).get("speed")

#         # Location's lat & lon
#         lat = weather_data.get("coord", {}).get("lat")
#         lon = weather_data.get("coord", {}).get("lon")

#         # Hourly data
#         hourly_data = []
#         for i in weather_data_hourly.get('list', [])[:6]: #Fetching the 'hourly' temp up to 6 hours
#             hourly_temp = round(i.get('main', {}).get('temp', 0))
#             hourly_time = (local_time + timedelta(seconds=i.get('dt'))).strftime('%I %p') # Rounded temp added in 'temp = []'
#             hourly_data.append({'temp': hourly_temp, 'time': hourly_time})

#         # Week data
#         week_data = []
#         for i in weather_data_week.get('daily', [])[:7]:
#             week_temp_high = round(i.get('temp', {}).get('max', 0))
#             week_temp_low = round(i.get('temp', {}).get('min', 0))
#             week_time = (local_time + timedelta(seconds=i.get('dt'))).strftime('%I %p')
#             week_data.append({'week_temp_high': week_temp_high, 'week_temp_low': week_temp_low, 'week_time': week_time})

#     else:
#         city = "N/A"
#         temp = "N/A"
#         description = "N/A"
#         local_time_iso = "N/A"
#         temp_high = "N/A"
#         temp_low = "N/A"
        
#         # Air Conditions
#         feels_like = "N/A"
#         wind = "N/A"

#         # Hourly
#         hourly_data = []

#         # Week
#         week_data = []

#     return jsonify({
#         'city': city,
#         'temp': temp,
#         'description': description,
#         'local_time': local_time_iso,
#         'feels_like': feels_like,
#         'wind': wind,
#         'temp_high': temp_high,
#         'temp_low': temp_low,
#         'hourly_data': hourly_data,
#         'week_data': week_data
#     })

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5328, debug=True)

# # pip install --upgrade Werkzeug
# # pip install --upgrade Flask
# # pip install --upgrade pip

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
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

    # Default
    weather_data = weather_response.json()
    city = weather_data.get("name", "N/A")
    temp = weather_data.get("main", {}).get("temp", "N/A")
    description = weather_data.get("weather", [{}])[0].get("description", "N/A")
    coords = weather_data.get("coord", {})
    temp_high = weather_data.get("main", {}).get("temp_max")
    temp_low = weather_data.get("main", {}).get("temp_min")

    # Air Conditions
    feels_like = weather_data.get("main", {}).get("feels_like")
    wind = weather_data.get("wind", {}).get("speed")

    # Get the UTC datetime and timezone offset
    dt_utc = datetime.utcfromtimestamp(weather_data.get("dt"))
    timezone_offset = timedelta(seconds=weather_data.get("timezone"))
    # Convert UTC datetime to local time
    local_time = dt_utc + timezone_offset
    # Convert UTC datetime to local time and format it in ISO 8601
    local_time_iso = local_time.isoformat()

    # If coordinates are available, use the onecall API for the 7-day forecast
    if coords:
        lat, lon = coords.get("lat"), coords.get("lon")
        onecall_URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&units={units}&appid={api_key}'
        onecall_response = requests.get(url=onecall_URL)
        
        if onecall_response.ok:
            onecall_data = onecall_response.json()
            forecast_data = process_forecast_data(onecall_data.get('daily', [])[0:7])

            # print('\n\n\n\nOneCall response:', onecall_response.json())

            # Air Conditions
            # uv = onecall_data["current"]["uvi"]
            uv = onecall_data.get("current", {}).get("uvi")
            print('\n\n\n\nUV: ', uv)

            rain_percent = onecall_data["hourly"][0].get("pop", 0) * 100
            # for i in onecall_data.get('daily', [])[0:1]:
            #     rain_percent = i.get('pop', 0) * 100
            print('Rain: ', rain_percent)

            # Hourly Data
            hourly_data = []
            for i in onecall_data.get('hourly', [])[:6]: #Fetching the 'hourly' temp up to 6 hours
                hourly_temp = round(i.get('temp', 0))
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
            uv = "N/A"
            rain_percent = "N/A"

            # Hourly
            hourly_data = []
            
            # Forecast
            forecast_data = []
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
        uv = "N/A"
        rain_percent = "N/A"

        # Hourly
        hourly_data = []

        # Forecast
        forecast_data = []

    return jsonify({
        'city': city,
        'temp': temp,
        'description': description,
        'local_time': local_time_iso,
        'feels_like': feels_like,
        'wind': wind,
        'uv' : uv,
        'rain_percent' : rain_percent,
        'temp_high': temp_high,
        'temp_low': temp_low,
        'hourly_data': hourly_data,
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