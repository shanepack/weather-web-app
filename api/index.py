from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import requests
import json
import openai 

def load_api_keys():
    secrets_file = "C:/Users/anony/Documents/GitHub/weather-web-app/api/secrets.json"
    try:
        with open(secrets_file) as f:
            secrets = json.load(f)
        return secrets
    except Exception as e:
        print(f"Error loading secrets file: {e}")
        return None


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

    # Default
    weather_data = weather_response.json()
    city = weather_data.get("name", "N/A")
    # user_city = city
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
        onecall_URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&units={units}&appid={openweather_api_key}'
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
            for i in onecall_data.get('hourly', [])[:6]:  # Fetching the 'hourly' temp up to 6 hours
                hourly_temp = round(i.get('temp', 0))
                # Calculate the hourly time
                hourly_datetime = local_time + timedelta(seconds=i.get('dt'))
                # Format the hour manually to remove leading zero
                hour = hourly_datetime.hour % 12
                hour = hour if hour != 0 else 12  # Convert '0' hour to '12'
                am_pm = 'AM' if hourly_datetime.hour < 12 else 'PM'
                hourly_time = f'{hour} {am_pm}'
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

@app.route('/api/chatgpt', methods=['POST'])
def chatgptResponse():
    input = request.get_json()
    print("Received data: ", input)
    messages = []
    question = {}
    user_city = input.get('user_city', '')
    question['role'] = 'user'
    question['content'] = f"What are some things to do in {user_city} ? Please keep the response short (around 50 words or less), I want the answer to be in-line with the following example: If the question is regarding Houston, I want the answer to be 'In Houston, consider exploring Buffalo Bayou Park where you can take a stroll or bike ride along the scenic trails that wind through this 160-acre park', then any more supplemental details (DO NOT EXPLICITLY STATE THAT YOU ARE PROVIDING SUPPLEMENTAL DETAILS). KEEP THE RESPONSE SHORT! THIS IS GOING TO BE USED ON THE FRONT PAGE OF A WEATHER APP. DO NOT MENTION THE SAME SUGGESTION MORE THAN ONCE, ALWAYS PICK SOMETHING NEW FROM THE AREA."
    messages.append(question)

    print('backend user_city: ', user_city)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    try:
        answer = completion['choices'][0]['message']['content'].split('\n')[0].strip()
        print(answer)
    except: 
        answer = 'Oops error encountered'
    return jsonify({'text': answer}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5328, debug=True)