# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import requests


# # app instance
# app = Flask(__name__)
# CORS(app)


# @app.route('/api/weather', methods=['POST'])
# def send_location():
#     data = request.get_json()
#     user_location = data.get('userLocation')

# @app.route('/api/weather', methods=['GET'])
# def send_location():
    
#     userlocation = 'houston'
#     PARAMS = {'address':userlocation}
#     api_key = "03f11aa770bb749257a45573c2754aa1"
#     URL = f'http://api.openweathermap.org/data/2.5/weather?q={userlocation}&appid={api_key}'

#     response = requests.get(url = URL, params = PARAMS)

#     print("response: ", response.status_code)
#     print("response json: ", response.json())

#     weather_data = response.json()
#     print(weather_data)

#     if response.status_code == 200:
#         weather_data = response.json()
#         city = weather_data.get("name")
#         temp = weather_data.get("main", {}).get("temp")
#         print(f"City: ", city, "Temp: ", temp)
#     else:
#         city = "N/A"
#         temp = "N/A"

#     return jsonify({
#         'weather_info': [userlocation, temp, city]
#     })


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5328, debug=True)

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

# app instance
app = Flask(__name__)
CORS(app)

@app.route('/api/weather', methods=['POST'])
def send_location():
    data = request.get_json()
    user_location = data.get('userLocation', 'Houston')  # Default to 'Houston' if no location is provided

    api_key = "03f11aa770bb749257a45573c2754aa1"
    URL = f'http://api.openweathermap.org/data/2.5/weather?q={user_location}&appid={api_key}'

    response = requests.get(url=URL)

    if response.status_code == 200:
        weather_data = response.json()
        city = weather_data.get("name")
        temp = weather_data.get("main", {}).get("temp")
        description = weather_data.get("weather", [{}])[0].get("description", "")
    else:
        city = "N/A"
        temp = "N/A"
        description = "N/A"

    return jsonify({
        'city': city,
        'temp': temp,
        'description': description
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5328, debug=True)