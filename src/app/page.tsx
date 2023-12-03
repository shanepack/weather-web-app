"use client";
import { useState, useEffect, useRef } from 'react';
import { format, isToday, parseISO } from 'date-fns'
import axios from 'axios';

// Define the structure for the weather data
type WeatherData = {
  city: string;
  temp: string;
  description: string;
  local_time?: string;
  feels_like: string;
  wind: number;
  uv: string;
  rain_percent: string;
  temp_high: string;
  temp_low: string;
  hourly_data: {temp: string; time: string}[];
  forecast: Array<{
    date: string;
    temp: number;
    rain_chance: number;
  }>;
};

// The main component for the weather app page
export default function RectanglePage() {
  
  const [userLocation, setUserLocation] = useState('Pearland');
  const [weatherData, setWeatherData] = useState({ city: '', temp: '', description: '', local_time: undefined, feels_like: '', wind: '', uv: '', rain_percent: '', temp_high: '', temp_low: '', hourly_data: [], forecast: []});
  const [previousLocations, setPreviousLocations] = useState<string[]>([]);
  const [showHome, setHomePage] = useState(true);
  const [showList, setListPage] = useState(false);
  const [showSettings, setSettingsPage] = useState(false);
  const [units, setUnit] = useState('imperial'); // or 'imperial' for Fahrenheit
  const [localTime, setLocalTime] = useState<Date | null>(null);

  const locationInputRef = useRef<HTMLInputElement>(null);

  const handleKeyDown = async (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      const input = locationInputRef.current;
      if (input) {
        const newLocation = input.value;
        setUserLocation(newLocation);
        setPreviousLocations((prevLocations) => [newLocation, ...prevLocations]);
        await fetchWeatherData(newLocation, units);
      }
    }
  };

  const fetchWeatherData = async (location: string, units: string, updateTime: boolean = true) => {
    try {
      const response = await axios.post(`http://localhost:5328/api/weather`, { userLocation: location, units });
      // Convert string to float and then round it
      const roundedTemp = Math.round(parseFloat(response.data.temp));
      const roundedFeels_Like = Math.round(parseFloat(response.data.feels_like));
      const roundedTemp_High = Math.round(parseFloat(response.data.temp_high));
      const roundedTemp_Low = Math.round(parseFloat(response.data.temp_low));
      const hourlyData = response.data.hourly_data.map((hourlyEntry: { temp: number; time: string }) => ({
        temp: Math.round(hourlyEntry.temp).toString(),
        time: hourlyEntry.time,
      }));
      setWeatherData((currentData) => {
        return {
          ...currentData, // Spread operator to copy all current weatherData state values
          city: response.data.city,
          temp: roundedTemp.toString(), // Convert back to string if needed
          description: response.data.description,
          local_time: updateTime ? response.data.local_time : currentData.local_time, // Only update the time if updateTime is true
          feels_like: roundedFeels_Like.toString(),
          wind: response.data.wind,
          uv: response.data.uv,
          rain_percent: response.data.rain_percent,
          temp_high: roundedTemp_High.toString(),
          temp_low: roundedTemp_Low.toString(),
          hourly_data: hourlyData,
          forecast: response.data.forecast,
        };
      });
    } catch (error) {
      console.error('Error fetching weather data:', error);
    }
  };
  
  // celsius or fahrenheit
  const getUnitSymbol = (units: string) => {
    return units === 'metric' ? 'C' : 'F';
  };

  // meters per second or miles per hour
  const getUnitSymbol2 = (units: string) => {
    return units === 'metric' ? ' M/S' : ' MPH'
  }

  useEffect(() => {
    fetchWeatherData(userLocation, units);
  }, [userLocation, units]);

  useEffect(() => {
    // Update local time every minute
    const intervalId = setInterval(() => {
      setLocalTime(new Date()); // Update to the current time
    }, 60000); // Update every minute
  
    // Clear the interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  const toggleHome = () => {
    if (!showHome) {
      setHomePage(true);
      setListPage(false);
      setSettingsPage(false);
    }
  };

  const toggleList = () => {
    if (!showList) {
      setHomePage(false);
      setListPage(true);
      setSettingsPage(false);
    }
  };

  const toggleSettings = () => {
    if (!showSettings) {
      setHomePage(false);
      setListPage(false);
      setSettingsPage(true);
    }
  };
  
  // This function will be called when the user clicks on the Fahrenheit link
  const selectFahrenheit = () => {
    setUnit('imperial');
    fetchWeatherData(userLocation, 'imperial'); // Fetch new weather data with Fahrenheit unit
  };

  // This function will be called when the user clicks on the Celsius link
  const selectCelsius = () => {
    setUnit('metric');
    fetchWeatherData(userLocation, 'metric'); // Fetch new weather data with Celsius unit
  };

  return (
    <div className="bg-gray-800 h-screen w-screen grid grid-cols-[auto,1fr] p-8 gap-8">
      {/* Settings sidebar */}
      <div className="bg-gray-700 flex flex-col justify-between p-8 rounded-[20px] w-[120px]">
        <button className={`bg-gray-600 p-6 text-white mb-2 ${showHome ? 'active' : ''}`} onClick={toggleHome}>
          H
          O
          M
          E
        </button>
        <button className={`bg-gray-600 p-6 text-white mb-2 ${showList ? 'active' : ''}`} onClick={toggleList}>
          L
          I
          S
          T
        </button>
        <button className={`bg-gray-600 p-6 text-white ${showSettings ? 'active' : ''}`} onClick={toggleSettings}>
          S
          E
          T
          T
          I
          N
          G
          S
        </button>
      </div>

      {/* Main content */}
      {showHome && (
      <div className="flex flex-col">
        {/* Top bar */}
        <div className="flex justify-between items-center mb-8">
          <input
            type="text"
            id="locationInput"
            placeholder="Search for a City..."
            className="p-2 bg-gray-700 rounded-[20px] text-white focus:outline-none focus:border-white"
            onKeyDown={handleKeyDown}
            ref={locationInputRef}
          />
          <p className="text-white text-2xl">8:00PM</p>
        </div>

        <div className="flex-1 grid grid-cols-2 gap-8">
        {/* Main Left section */}
        <div className="grid grid-rows-3 gap-8">
            {/* City, Temperature & Today's Forecast */}
            <div className="bg-black p-8 rounded-[20px] flex flex-col justify-between row-span-2">
                <div>
                    <p className="text-white text-5xl mb-2"style={{ fontWeight: 'bold' }}>{weatherData.city}</p> 
                    <p className="text-white text-5xl mb-6"style={{ fontWeight: 'bold' }}>{weatherData.temp ? `${weatherData.temp}°${getUnitSymbol(units)}` : ''}</p>
                    <p className="text-white text-2x1 ml-2">{weatherData.temp_high ? `High: ${weatherData.temp_high}°${getUnitSymbol(units)}` : ''}</p>
                    <p className="text-white text-2x1 ml-2">{weatherData.temp_low ? `Low: ${weatherData.temp_low}°${getUnitSymbol(units)}` : ''}</p> 
                </div>

                <div className="bg-[#0C1117] p-8 rounded-[20px]">
                    <p className="text-white text-2xl mb-4">TODAY'S FORECAST</p>
                    <div className="grid grid-cols-6 gap-8">
                      {weatherData.hourly_data.length > 0 ? (
                        weatherData.hourly_data.map((hourlyEntry: { temp: string; time: string }, index) => (
                          <div key={index} className="flex flex-col items-center">
                            <p className="text-white text-2xl">{hourlyEntry.time}</p>
                            <p className="text-white text-2xl">{hourlyEntry.temp}°{getUnitSymbol(units)}</p>
                          </div>
                        ))
                      ) : (
                        <p className="text-white">Hourly data not available</p>
                      )}
                    </div>
                </div>
            </div>

            {/* Air Conditions */}
            <div className="bg-gray-700 p-8 rounded-[20px]">
                <p className="text-white text-2xl mb-10">AIR CONDITIONS</p>
                <div className="grid grid-cols-4 gap-8">  
                  <div className="flex flex-col items-center">
                    <p className="text-White text8x1 mb-2">Feels Like</p>
                    <p className="text-white text-3xl">{weatherData.feels_like ? `${weatherData.feels_like}°${getUnitSymbol(units)}` : ''}</p>
                  </div>
                  <div className="flex flex-col items-center">
                    <p className="text-White text8x1 mb-2">Chance of Rain</p>
                    <p className="text-white text-3xl">{weatherData.rain_percent ? `${weatherData.rain_percent}%` : '0%'}</p>
                  </div>
                  <div className="flex flex-col items-center">
                    <p className="text-White text8x1 mb-2">Wind</p>
                    {/* The line below has an error with weatherData.wind, but it works anyway. Fix later! */}
                    <p className="text-white text-3xl">{weatherData.wind ? `${Math.round(weatherData.wind)}${getUnitSymbol2(units)}` : ''}</p>
                  </div>
                  <div className="flex flex-col items-center">
                    <p className="text-White text8x1 mb-2">UV Index</p>
                    <p className="text-white text-3xl">{weatherData.uv ? `${weatherData.uv}` : 'N/A'}</p>
                  </div>
                </div>
            </div>
        </div>

          {/* Main Right section */}
          <div className="grid grid-rows-2 gap-8">
            {/* ChatGPT block */}
            <div className="bg-white p-6 rounded-[20px] min-h-[300px]"> {/* Use the desired value in place of 300px */}
              <p className="text-gray-800 mb-2" style={{ fontSize: 'clamp(0.8rem, 3vw, 2rem)' }}>
                This evening in Pearland, Independence Park is open until 10:00 PM and offers a nice late-night option for a peaceful walk or some stargazing in a park setting.
              </p>
              <p className="text-gray-600 text-right text-sm">
                Suggestion Generated by ChatGPT
              </p>
            </div>

            {/* 7 Day Forecast */}
            <div className="bg-gray-700 p-8 rounded-[20px] min-h-[300px]"> {/* Use the desired value in place of 300px */}
              <p className="text-white text-2xl mb-6">7 DAY FORECAST</p>
              <div className="grid grid-cols-7 gap-8">
                {/* <div className="flex flex-col items-center"> */}
                  {weatherData.forecast && weatherData.forecast.length > 0 ? (
                    weatherData.forecast.map((day: { date: string; rain_chance: number; temp: number }, index) => {
                      const dayDate = parseISO(day.date);
                      const displayDate = isToday(dayDate) ? 'Today' : format(dayDate, 'EEE');

                      return (
                        <div key={index} className="text-white">
                          <p>{displayDate}</p>
                          <p>{Math.round(day.temp)}°{getUnitSymbol(units)}</p>
                          <p>Rain: {Math.round(day.rain_chance)}%</p>
                        </div>
                      );
                    })
                  ) : (
                    <p className="text-white">Loading forecast...</p>
                  )}
                {/* </div> */}
              </div>
            </div>
          </div>
        </div>
      </div>
      )}

      {/* List Page */}
      {showList && (
      <div className="grid grid-cols-1 grid-rows-1 gap-8">
        <div className="grid grid-rows-1 gap-8">
          <div className="bg-gray-700 p-8 rounded-[20px] min-h-[100px]">
            <p className="text-white text-4xl mb-4">Previous Locations</p>
            <p>
                {previousLocations.map((location, index) => (
                    <li key={index} className="text-white text-sm">
                        {location}
                    </li>
                ))}
            </p>
          </div>
        </div>
      </div>
      )}

      {/* Setting Page */}
      {showSettings && (
      <div className="grid grid-cols-1 grid-rows-1 gap-8">
        <div className="grid grid-rows-1 gap-8">
          <div className="bg-gray-700 p-8 rounded-[20px] min-h-[100px]">
            <p className="text-white text-4xl mb-4">Appearance</p>
            <div className="inline-flex rounded-md shadow-sm mb-4">
              <a href="#" className="px-16 py-8 text-sm font-medium text-blue-700 bg-white border border-gray-200 rounded-l-lg hover:bg-gray-100 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-blue-500 dark:focus:text-white" aria-current="page">
                Dark
              </a>
              <a href="#" className="px-16 py-8 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-r-md hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-blue-500 dark:focus:text-white border-t border-b">
                Light
              </a>
            </div>
            <p className="text-white text-4xl mb-4">Units</p>
            <p className="text-gray-300 text-2xl mb-4">Temperature</p>
            <div className="inline-flex rounded-md shadow-sm mb-4">
              {/* Fahrenheit link */}
              <button
                onClick={selectFahrenheit}
                className="px-16 py-8 text-sm font-medium text-blue-700 bg-white border border-gray-200 rounded-l-lg hover:bg-gray-100 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-blue-500 dark:focus:text-white"
              >
                Fahrenheit
              </button>
              {/* Celsius link */}
              <button
                onClick={selectCelsius}
                className="px-16 py-8 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-r-md hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-blue-500 dark:focus:text-white border-t border-b"
              >
                Celsius
              </button>
            </div>
            <p className="text-gray-300 text-2xl mb-4">Wind Speed</p>
            <div className="inline-flex rounded-md shadow-sm mb-4">
              <a href="#" className="px-16 py-8 text-sm font-medium text-blue-700 bg-white border border-gray-200 rounded-l-lg hover:bg-gray-100 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-blue-500 dark:focus:text-white" aria-current="page">
                m/s
              </a>
              <a href="#" className="px-16 py-8 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-r-md hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-blue-500 dark:focus:text-white border-t border-b">
                km/h
              </a>
            </div>
          </div>
        </div>
      </div>
      )}
    </div>
  );
}