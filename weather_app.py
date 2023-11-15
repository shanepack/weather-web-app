from datetime import datetime as dt, timedelta, timezone
from datetime import date
import pytz
import requests
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

# Extract relevant information from the weather data
temperature = data["current"]["temp"]
feels_like = data["current"]["feels_like"]
wind = data["current"]["wind_speed"]
uvi = data["current"]["uvi"]
rain = data["hourly"][0]["pop"]
sunrise = time.strftime("%I:%M %p", time.gmtime(data["daily"][0]["sunrise"] + data["timezone_offset"]))
sunset = time.strftime("%I:%M %p", time.gmtime(data["daily"][0]["sunset"] + data["timezone_offset"]))
pressure = data["current"]["pressure"]
vis = data["current"]["visibility"]
humidity = data["current"]["humidity"]

# Display the weather information to the user
print(f'\n{location}')
print(round(temperature), "°F\n")
print("--- Air Conditions ---")
print("Feels like:", round(feels_like), "°F")
print("Wind Speed:", wind, "mph")
print("UV Index:", uvi)
print("Chance of rain:", round(rain), "%\n")
print("--- Air Conditions (See More) ---")
print(sunrise)
print(sunset)
print("Pressure:", pressure, "hPa")
print("Visibility:", round(vis / 1000), "km")
print("Humidity:", humidity, "%\n")

high = []
low = []
descr = []

#Fetching the 'daily' temp
for i in data['daily']:
        
        #Get high temp
        high.append(round(i['temp']['max']))
        
        #Get low temp
        low.append(round(i['temp']['min']))
        
        #Get the weather condition and the description
        descr.append(i['weather'][0]['description'])
        
string = f'[ {location} - 8 days forecast]\n'

# Days of the week 
first = dt.now()
text=first.strftime("%A")

second = first+timedelta(1)
text1=second.strftime("%A")

third = first+timedelta(2)
text2=third.strftime("%A")

fourth = first+timedelta(3)
text3=fourth.strftime("%A")

fifth = first+timedelta(4)
text4=fifth.strftime("%A")

sixth = first+timedelta(5)
text5=sixth.strftime("%A")

seventh = first+timedelta(6)
text6=seventh.strftime("%A")

#Loop for as much days as there available (8 in this case):
for i in range(len(high)):
    
    #Print out the days of the week (monday, tuesday,...)
    
    if i == 0:
        string += f'\nToday\n'
        
    elif i == 1:
        string += f'\n{text1}\n'
        
    elif i == 2:
        string += f'\n{text2}\n'
        
    elif i == 3:
        string += f'\n{text3}\n'
        
    elif i == 4:
        string += f'\n{text4}\n'

    elif i == 5:
        string += f'\n{text5}\n'

    elif i == 6:
        string += f'\n{text6}\n'

    else:
        string+= f'\n{text}\n'
        
        
    string += 'High: ' + str(high[i]) + '°F' + "\n"
    string += 'Low: ' + str(low[i]) + '°F' + "\n"
    string += 'Conditions: ' + descr[i] + '\n'
    
print(string)

temp = []
#Fetching the 'hourly' temp
for i in data['hourly']:
        
       # Rounded temp added in 'temp = []'
        temp.append(round(i['temp']))
        
string = f'[ {location} - 48 hour forecast]\n'

# The current time through 48 hours of fetched temp
now = dt.now(pytz.timezone(data['timezone']))

c_time = now.strftime('%I %p')

c1_time = now + timedelta(hours = 1)
hr1time = c1_time.strftime('%I %p')

c2_time = now + timedelta(hours = 2)
hr2time = c2_time.strftime('%I %p')

c3_time = now + timedelta(hours = 3)
hr3time = c3_time.strftime('%I %p')

c4_time = now + timedelta(hours = 4)
hr4time = c4_time.strftime('%I %p')

c5_time = now + timedelta(hours = 5)
hr5time = c5_time.strftime('%I %p')

c6_time = now + timedelta(hours = 6)
hr6time = c6_time.strftime('%I %p')

c7_time = now + timedelta(hours = 7)
hr7time = c7_time.strftime('%I %p')

c8_time = now + timedelta(hours = 8)
hr8time = c8_time.strftime('%I %p')

c9_time = now + timedelta(hours = 9)
hr9time = c9_time.strftime('%I %p')

c10_time = now + timedelta(hours = 10)
hr10time = c10_time.strftime('%I %p')

c11_time = now + timedelta(hours = 11)
hr11time = c11_time.strftime('%I %p')

c12_time = now + timedelta(hours = 12)
hr12time = c12_time.strftime('%I %p')

c13_time = now + timedelta(hours = 13)
hr13time = c13_time.strftime('%I %p')

c14_time = now + timedelta(hours = 14)
hr14time = c14_time.strftime('%I %p')

c15_time = now + timedelta(hours = 15)
hr15time = c15_time.strftime('%I %p')

c16_time = now + timedelta(hours = 16)
hr16time = c16_time.strftime('%I %p')
    
c17_time = now + timedelta(hours = 17)
hr17time = c17_time.strftime('%I %p')

c18_time = now + timedelta(hours = 18)
hr18time = c18_time.strftime('%I %p')

c19_time = now + timedelta(hours = 19)
hr19time = c19_time.strftime('%I %p')

c20_time = now + timedelta(hours = 20)
hr20time = c20_time.strftime('%I %p')

c21_time = now + timedelta(hours = 21)
hr21time = c21_time.strftime('%I %p')

c22_time = now + timedelta(hours = 22)
hr22time = c22_time.strftime('%I %p')

c23_time = now + timedelta(hours = 23)
hr23time = c23_time.strftime('%I %p')

#Loop for as much hours as there available (48 in this case):
for i in range(len(temp)):
    
    #Print out the temp every hour (48 hour forecast)
       
   if i in [0]:
        string += f'\n{c_time}\n'
        
   elif i in [1,25]:
        string += f'\n{hr1time}\n'
        
   elif i in [2,26]:
        string += f'\n{hr2time}\n'
        
   elif i in [3,27]:
        string += f'\n{hr3time}\n'
        
   elif i in [4,28]:
        string += f'\n{hr4time}\n'
        
   elif i in [5,29]:
        string += f'\n{hr5time}\n'
        
   elif i in [6,30]:
        string += f'\n{hr6time}\n'
        
   elif i in [7,31]:
        string += f'\n{hr7time}\n'
        
   elif i in [8,32]:
        string += f'\n{hr8time}\n'

   elif i in [9,33]:
        string += f'\n{hr9time}\n'
        
   elif i in [10,34]:
        string += f'\n{hr10time}\n'
        
   elif i in [11,35]:
        string += f'\n{hr11time}\n'
        
   elif i in [12,36]:
        string+= f'\n{hr12time}\n'

   elif i in [13,37]:
        string += f'\n{hr13time}\n'
        
   elif i in [14,38]:
        string += f'\n{hr14time}\n'
        
   elif i in [15,39]:
        string += f'\n{hr15time}\n'
        
   elif i in [16,40]:
        string += f'\n{hr16time}\n'
        
   elif i in [17,41]:
        string += f'\n{hr17time}\n'
        
   elif i in [18,42]:
        string += f'\n{hr18time}\n'
        
   elif i in [19,43]:
        string += f'\n{hr19time}\n'
        
   elif i in [20,44]:
        string += f'\n{hr20time}\n'

   elif i in [21,45]:
        string += f'\n{hr21time}\n'
        
   elif i in [22,46]:
        string += f'\n{hr22time}\n'
        
   elif i in [23,47]:
        string += f'\n{hr23time}\n'
        
   else :
        string+= f'\n{c_time}\n'
        
        
   string += str(temp[i]) + '°F' + "\n"
    
print(string)



