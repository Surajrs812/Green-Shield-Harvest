import requests
import serial
import time
import json
import os

# OpenWeather API section
API_KEY = os.environ.get("WEATHER_API_KEY") 
location = "Bengaluru"

# OpenWeather API endpoint for current weather data
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"

def get_weather_data():
    """Fetch the current weather data (temperature and humidity) from OpenWeather API."""
    try:
        response = requests.get(weather_url)
        response.raise_for_status()  # Raise exception if the status code isn't 200
        data = response.json()

        # Extract temperature and humidity from the JSON response
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        
        return temperature, humidity

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None, None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None, None

def get_arduino_data(arduino_port='COM4', baud_rate=9600):
    """Read sensor data from Arduino and return the status of sensor 1 and sensor 2."""
    c = 0
    try:
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Successfully connected to {arduino_port}")
    except serial.SerialException as e:
        print(f"Error connecting to {arduino_port}: {e}")
        return "NA", "NA"  # Return NA for both sensor statuses

    sensor1_status = "NA"
    sensor2_status = "NA"
    start_time = time.time()

    # Give some time for Arduino to start sending data
    time.sleep(2)

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Raw data from Arduino: {line}")  # Debug print to see raw input
            if c == 0:
                sensor1_status = line
            elif c == 1:
                sensor2_status = line
            elif c == 2:
                continue
            elif c == 3:
                continue
            c += 1
            # Expecting the format: "Some Moisture, No Moisture"
                
        # Break after a certain time
        if time.time() - start_time > 5:
            break

    ser.close()
    print(sensor1_status, sensor2_status)  # Close the serial connection after reading
    return sensor1_status, sensor2_status

def get_device_status():
    """Fetch weather and sensor data, and return the JSON response."""
    # Fetch weather data (temperature, humidity)
    temperature, humidity = get_weather_data()

    # Fetch sensor data from Arduino
    sensor1_status, sensor2_status = get_arduino_data()

    # Format the final JSON response with sensor statuses and weather data
    data = {
        "Status": "ON",
        "Moisture Sensor 1": sensor1_status,  # Status from Arduino for sensor 1
        "Moisture Sensor 2": sensor2_status,  # Status from Arduino for sensor 2
        "Temperature": temperature,            # Temperature from OpenWeather API
        "Humidity": humidity,                  # Humidity from OpenWeather API
    }
    
    filename = 'device_status.json'

    # Open a file in write mode and save the JSON data
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    with open(filename, 'r') as jf:
        ld_w = json.load(jf)

    # Return the JSON object
    return ld_w

if __name__ == '__main__':
    print("Starting data collection...")

    # Allow the connection to stabilize
    time.sleep(2)
    values = get_device_status()
    print(values)
