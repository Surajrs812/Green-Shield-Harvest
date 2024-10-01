import requests

# Replace this with your actual OpenWeather API key
API_KEY = "91c92360e208de9e42487a58a9e41766"
location = "Bangalore"

# OpenWeather API endpoint for current weather data
url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"

def get_weather_data():
    try:
        response = requests.get(url)
        # Raise exception if the status code isn't 200
        response.raise_for_status()
        data = response.json()

        # Extract temperature and humidity from the JSON response
        temperature = data['main']['temp']
        humidity = data['main']['humidity']

        print(f"Temperature in {location}: {temperature}°C")
        print(f"Humidity in {location}: {humidity}%")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

if __name__ == "__main__":
    get_weather_data()
