"use client";
import { useState, useEffect } from 'react';
import {InputUserLocation} from './scripts.js';
import axios from 'axios';

<<<<<<< Updated upstream
=======
// Define the structure for the weather data
type WeatherData = {
  city: string;
  temp: string;
  description: string;
  local_time?: string;
  feels_like: string;
  wind: string;
  temp_high: string;
  temp_low: string;
};

// The main component for the weather app page
>>>>>>> Stashed changes
export default function RectanglePage() {
  
  const [userLocation, setUserLocation] = useState('Pearland');
<<<<<<< Updated upstream
  const [showHome, setHomePage] = useState(true);
  const [showList, setListPage] = useState(false);
  const [showSettings, setSettingsPage] = useState(false);
  const [previousLocations, setPreviousLocations] = useState<string[]>([]);
=======
  const [weatherData, setWeatherData] = useState({ city: '', temp: '', description: '', local_time: undefined, feels_like: '', wind: '', temp_high: '', temp_low: ''});
  const [previousLocations, setPreviousLocations] = useState<string[]>([]);
  const [showHome, setHomePage] = useState(true);
  const [showList, setListPage] = useState(false);
  const [showSettings, setSettingsPage] = useState(false);
  const [units, setUnit] = useState('imperial'); // or 'imperial' for Fahrenheit
  const [localTime, setLocalTime] = useState<Date | null>(null);
>>>>>>> Stashed changes

  // const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
  //   if (e.key === 'Enter') {
  //     sendLocationToPython();
  //   }
  // };

<<<<<<< Updated upstream
  // const sendLocationToPython = async () => {
  //   try {
  //     console.log('-----Sending data to python-----');
  //     const encodedLocation = encodeURIComponent(userLocation);
  //     const response = await axios.post('/', { userLocation: encodedLocation });
  //     console.log('-----Returned-----');
      
  //   } catch (error) {
  //     console.error('Error sending data to Python:', error);
  //   }
  // };
=======
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
      setWeatherData((currentData) => {
        return {
          ...currentData, // Spread operator to copy all current weatherData state values
          city: response.data.city,
          temp: roundedTemp.toString(), // Convert back to string if needed
          description: response.data.description,
          local_time: updateTime ? response.data.local_time : currentData.local_time, // Only update the time if updateTime is true
          feels_like: roundedFeels_Like.toString(),
          wind: response.data.wind,
          temp_high: roundedTemp_High.toString(),
          temp_low: roundedTemp_Low.toString(),
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
>>>>>>> Stashed changes

  // meters per second or miles per hour
  const getUnitSymbol2 = (units: string) => {
    return units === 'metric' ? ' M/S' : ' MPH'
  }

  useEffect(() => {
    InputUserLocation((userLocation : string) => {
        setPreviousLocations((prevLocations) => [userLocation, ...prevLocations]);
    });
}, []);

  useEffect(() => {
    InputUserLocation(setUserLocation);
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
            //onKeyDown={handleKeyPress}
          />
          <p className="text-white text-2xl">8:00PM</p>
        </div>

        <div className="flex-1 grid grid-cols-2 gap-8">
        {/* Main Left section */}
        <div className="grid grid-rows-3 gap-8">
            {/* City, Temperature & Today's Forecast */}
            <div className="bg-black p-8 rounded-[20px] flex flex-col justify-between row-span-2">
                <div>
<<<<<<< Updated upstream
                    <p className="text-white text-4xl mb-2">{userLocation}</p>
                    <p className="text-white text-6xl">110°</p>
=======
                    <p className="text-white text-4xl mb-2">{weatherData.city}</p> 
                    <p className="text-white text-6xl mb-6">{weatherData.temp ? `${weatherData.temp}°${getUnitSymbol(units)}` : ''}</p>
                    <p className="text-white text-2x1 ml-2">{weatherData.temp_high ? `High: ${weatherData.temp_high}°${getUnitSymbol(units)}` : ''}</p>
                    <p className="text-white text-2x1 ml-2">{weatherData.temp_low ? `Low: ${weatherData.temp_low}°${getUnitSymbol(units)}` : ''}</p> 
>>>>>>> Stashed changes
                </div>

                <div className="bg-[#0C1117] p-8 rounded-[20px]">
                    <p className="text-white text-2xl">TODAY'S FORECAST</p>
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
                    <p className="text-White text8x1 mb-2">Change of Rain</p>
                    <p className="text-white text-3xl">{weatherData.feels_like ? `${weatherData.feels_like}°${getUnitSymbol(units)}` : ''}</p>
                  </div>
                  <div className="flex flex-col items-center">
                    <p className="text-White text8x1 mb-2">Wind</p>
                    <p className="text-white text-3xl">{weatherData.wind ? `${weatherData.wind}${getUnitSymbol2(units)}` : ''}</p>
                  </div>
                  <div className="flex flex-col items-center">
                    <p className="text-White text8x1 mb-2">UV Index</p>
                    <p className="text-white text-3xl">{weatherData.feels_like ? `${weatherData.feels_like}°${getUnitSymbol(units)}` : ''}</p>
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
              <p className="text-white text-2xl">7 DAY FORECAST</p>
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
              <a href="#" className="px-16 py-8 text-sm font-medium text-blue-700 bg-white border border-gray-200 rounded-l-lg hover:bg-gray-100 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-blue-500 dark:focus:text-white" aria-current="page">
                Fahrenheit
              </a>
              <a href="#" className="px-16 py-8 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-r-md hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-blue-500 dark:focus:text-white border-t border-b">
                Celsius
              </a>
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