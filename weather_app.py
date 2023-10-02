import requests
# Define the main function
def main():
    # Prompt the user for their zip code or city
    location = input("Search for a zip code or city: ")

    # Validate the user input
    if not location:
        print("You must enter a valid zip code or city")
        return
    
    # Call the function to fetch weather data
    weather_data = fetch_weather_data(location)

    # If the weather data is found, display it to the user
    if weather_data:
        print_weather_data(weather_data)
    else:
        print("Could not retrieve weather data for the specified location")

# Function to fetch weather data from the webservice
def fetch_weather_data(location):
    try:
        # Make a request to the webservice
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid=ee4fc84f29103a26ae2400ec30a26411&units=imperial'

        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Return the weather data
            return response.json()
        else:
            print("Failed to retrieve weather data.")
            return None
    except requests.exceptions.RequestException as e:
        print("An error occurred while connecting to the webservice:", str(e))
        return None

# Function to display weather data to the user
def print_weather_data(weather_data):
    # Extract relevant information from the weather data
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    description = weather_data["weather"][0]["description"]
    wind = weather_data["wind"]["speed"]
    # Display the weather information to the user
    print("\nWeather forecast:")
    print("\nTemperature:", round(temperature), "°F")
    print("Humidity:", humidity, "%")
    print("Description:", description)
    print("Wind Speed:", wind, "mph")
# Call the main function to start the program
main()

