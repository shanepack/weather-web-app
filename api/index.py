

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import requests
# app instance
app = Flask(__name__)
CORS(app)

# @app.route('/api/weather', methods=['POST'])
# def send_location():
#     data = request.get_json()
#     user_location = data.get('userLocation', 'Houston')  # Default to 'Houston' if no location is provided
#     units = data.get('units', 'imperial') 

#     api_key = "03f11aa770bb749257a45573c2754aa1"
#     URL = f'http://api.openweathermap.org/data/2.5/weather?q={user_location}&units={units}&appid={api_key}'

#     response = requests.get(url=URL)

#     if response.status_code == 200:
#         weather_data = response.json()
#         city = weather_data.get("name")
#         temp = weather_data.get("main", {}).get("temp")
#         description = weather_data.get("weather", [{}])[0].get("description", "")
#         dt = weather_data.get("dt")
#         timezone = weather_data.get("timezone")
#     else:
#         city = "N/A"
#         temp = "N/A"
#         description = "N/A"
#         dt = None
#         timezone = None

#     return jsonify({
#         'city': city,
#         'temp': temp,
#         'description': description
#         'dt': dt,
#         'timezone': timezone
#     })

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5328, debug=True)

@app.route('/api/weather', methods=['POST'])
def send_location():
    data = request.get_json()
    user_location = data.get('userLocation', 'Houston')  # Default to 'Houston' if no location is provided
    units = data.get('units', 'imperial')  # Default to 'imperial' if no unit is provided

    api_key = "03f11aa770bb749257a45573c2754aa1"
    URL = f'http://api.openweathermap.org/data/2.5/weather?q={user_location}&units={units}&appid={api_key}'

    response = requests.get(url=URL)

    if response.status_code == 200:
        weather_data = response.json()
        city = weather_data.get("name")
        temp = weather_data.get("main", {}).get("temp")
        description = weather_data.get("weather", [{}])[0].get("description", "")

        # Get the UTC datetime and timezone offset
        dt_utc = datetime.utcfromtimestamp(weather_data.get("dt"))
        timezone_offset = timedelta(seconds=weather_data.get("timezone"))
        # Convert UTC datetime to local time
        local_time = dt_utc + timezone_offset
        # Convert UTC datetime to local time and format it in ISO 8601
        local_time_iso = (dt_utc + timezone_offset).isoformat()

    else:
        city = "N/A"
        temp = "N/A"
        description = "N/A"
        local_time_iso = "N/A"

    return jsonify({
        'city': city,
        'temp': temp,
        'description': description,
        'local_time': local_time_iso
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5328, debug=True)