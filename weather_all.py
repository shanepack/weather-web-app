import requests
import datetime 
import time
api_key = "ee4fc84f29103a26ae2400ec30a26411"

location = input("Search for a zip code or city: ")

weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'

req = requests.get(weather_url)
data = req.json()
#Get the name, the longitude and latitude

lon = data['coord']['lon']
lat = data['coord']['lat']
part = "minutely"

oc_url =f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}&units=imperial'

req = requests.get(oc_url)
data = req.json()

temperature = data["current"]["temp"]
humidity = data["current"]["humidity"]
description = data["current"]["weather"][0]["description"]
wind = data["current"]["wind_speed"]
    # Display the weather information to the user
print("\nWeather forecast:")
print("\nTemperature:", round(temperature), "°F")
print("Humidity:", humidity, "%")
print("Description:", description)
print("Wind Speed:", wind, "mph\n")

high = []
low = []
descr = []

#We need to access 'daily'
for i in data['daily']:
        
        #We notice that the temperature is in Kelvin, so we need to do -273.15 for every datapoint
        
        #Let's start by days
        #Let's round the decimal numbers to 2
        high.append(round(i['temp']['max']))
        
        #Nights
        low.append(round(i['temp']['min']))
        
        #Let's now get the weather condition and the description
        #'weather' [0] 'main' + 'weather' [0] 'description'
        descr.append(i['weather'][0]['main'] + ": " +i['weather'][0]['description'])
string = f'[ {location} - 8 days forecast]\n'

#Let's now loop for as much days as there available (8 in this case):
for i in range(len(high)):
    
    #We want to print out the day (day1,2,3,4..)
    #Also, day 1 = today and day 2 = tomorrow for reference
    
    if i == 0:
        string += f'\nDay {i+1} (Today)\n'
        
    elif i == 1:
        string += f'\nDay {i+1} (Tomorrow)\n'
        
    else:
        string += f'\nDay {i+1}\n'
        
    string += 'High:' + str(high[i]) + '°F' + "\n"
    string += 'Low:' + str(low[i]) + '°F' + "\n"
    string += 'Conditions:' + descr[i] + '\n'
    
print(string)

temp = []

#We need to access 'hourly'
for i in data['hourly']:
        
        #Let's start by days
        #Let's round the decimal numbers 
        temp.append(round(i['temp']))
        
string = f'[ {location} - 48 hour forecast]\n'
time_string = time.strftime('%H %p')
#Let's now loop for as much hours as there available (48 in this case):
for i in range(len(temp)):
    
    #We want to print out the day (Hour1,2,3,4..)
   
    
    if i == 0:
        string +=f'\n (Now) \n'
        
    elif i == 1:
        string +=f'\n {time_string} \n' 
        
    else:
        string += f'\n {time_string} \n'
        
    string += 'Temp:' + str(temp[i]) + '°F' + "\n"
    
print(string)
