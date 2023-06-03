import requests
import geocoder
import datetime
import sys

API_KEY = "OPENWEATHERMAP API KEY"

def get_time(timestamp):
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)
    human_time = datetime_obj.strftime('%H:%M')
    return human_time

def get_weather(postal_code):
    try:
        postal_code = int(postal_code)
    except ValueError:
        print("Invalid postal code.")
        return

    g = geocoder.arcgis(postal_code)
    if not g.ok:
        print("Failed to get coordinates.")
        return

    lat, lng = g.latlng
    latitude = round(lat, 4)
    longitude = round(lng, 4)

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        raw_weather_data = response.json()
    except (requests.RequestException, ValueError):
        print("Failed to fetch weather data.")
        return

    sunrise = get_time(raw_weather_data["sys"]["sunrise"])
    sunset = get_time(raw_weather_data["sys"]["sunset"])
    feelslike = round(raw_weather_data["main"]["feels_like"] - 273.15)
    visibility = (str(int(raw_weather_data["visibility"]/100)) + "%")
    humidity = raw_weather_data["main"]["humidity"]
    pressure = raw_weather_data["main"]["pressure"]
    weather_main = raw_weather_data["weather"][0]["main"]
    weather_description = (raw_weather_data["weather"][0]["description"]).title()
    temperature = round(raw_weather_data["main"]["temp"] - 273.15)

    print("Weather:", weather_main)
    print("Description", weather_description)
    print("Temperature: {}°C".format(temperature))
    print("Feels Like: {}°C".format(feelslike))
    print("Humidity:", humidity)
    print("Pressure:", pressure)
    print("Visibility:", visibility)
    print("Sunrise:", sunrise)
    print("Sunset:", sunset)

postal_code = int(sys.argv[1])
get_weather(postal_code)
