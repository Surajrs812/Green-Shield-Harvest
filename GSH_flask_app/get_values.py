import requests
import serial
import time
import json

# OpenWeather API section
API_KEY = "91c92360e208de9e42487a58a9e41766"  # Replace with your actual API key
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
    # Try to initialize the connection to the Arduino
    try:
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Successfully connected to {arduino_port}")
        serial_available = True
    except serial.SerialException as e:
        print(f"Error connecting to {arduino_port}: {e}")
        ser = None  # Mark as None if the connection fails
        serial_available = False  # Mark that serial is not available

    def read_arduino_data():
        try:
            if ser and ser.in_waiting > 0:
                # Read a line from the serial output
                line = ser.readline().decode('utf-8').strip()
                return line
        except Exception as e:
            print(f"Error reading data: {e}")
        return None

    if not serial_available:
        # If COM4 is not accessible, return 'NA' for moisture sensor statuses
        sensor1_status = "NA"
        sensor2_status = "NA"
    else:
        # If COM4 is accessible, read status data from Arduino
        sensor1_status = read_arduino_data() or "NA"  # Default to 'NA' if no data
        sensor2_status = read_arduino_data() or "NA"  # Default to 'NA' if no data

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
        "Moisture Sensor 1": sensor1_status,  # Moisture sensor 1 status
        "Moisture Sensor 2": sensor2_status,  # Moisture sensor 2 status
        "Temperature": temperature,  # Temperature from OpenWeather API
        "Humidity": humidity,  # Humidity from OpenWeather API
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
    # Adjust the delay as needed
    time.sleep(1)
