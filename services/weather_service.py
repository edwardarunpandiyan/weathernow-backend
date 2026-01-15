import requests
from utils.weather_codes import WEATHER_CODE_MAP

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def parse_daily_weather(daily: dict) -> list:
    if not daily or not isinstance(daily, dict):
        return []
    times = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    codes = daily.get("weathercode", [])

    length = min(len(times), len(max_temps), len(min_temps), len(codes))

    daily_data = []
    for i in range(length):
        daily_data.append({
            "date": times[i],
            "max_temperature": max_temps[i],
            "min_temperature": min_temps[i],
            "condition": WEATHER_CODE_MAP.get(codes[i], "Unknown"),
        })
    return daily_data

def parse_hourly_weather(hourly: dict) -> list:
    if not hourly or not isinstance(hourly, dict):
        return []
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    speeds = hourly.get("windspeed_10m", [])
    codes = hourly.get("weathercode", [])

    length = min(len(times), len(temps), len(speeds), len(codes))

    hourly_data = []
    for i in range(length):
        hourly_data.append({
            "date": times[i],
            "temperature": temps[i],
            "windspeed": speeds[i],
            "condition": WEATHER_CODE_MAP.get(codes[i], "Unknown"),
        })
    return hourly_data

def parse_current_weather(current: dict) -> dict:
    if not current or not isinstance(current, dict):
        return {}

    temperature = current.get("temperature")
    weather_code = current.get("weathercode")
    windspeed = current.get("windspeed")
    winddirection = current.get("winddirection")
    time = current.get("time")
    is_day = current.get("is_day")

    return {
        "temperature": temperature,
        "condition": WEATHER_CODE_MAP.get(weather_code, "Unknown"),
        "windspeed": windspeed,
        "winddirection": winddirection,
        "time": time,
        "is_day": bool(is_day) if is_day is not None else None,
    }

def parse_weather_units(units: dict) -> dict:
    if not units or not isinstance(units, dict):
        return {}

    temperature = units.get("temperature")
    windspeed = units.get("windspeed")
    winddirection = units.get("winddirection")

    return {
        "temperature": temperature,
        "windspeed": windspeed,
        "winddirection": winddirection,
        }

def get_weather_by_coords(latitude, longitude):
    response = requests.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
            "hourly": "temperature_2m,weathercode,windspeed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,weathercode",
            "forecast_days": "7",
            "timezone": "auto"
        }
    )
    print(response)
    if response.status_code != 200:
        return {"error": "Weather data not found"}
    data = response.json()
    # print(data)
    if not isinstance(data, dict):
        return {"error": "Invalid weather data"}

    REQUIRED_KEYS = ("current_weather", "latitude", "longitude")

    if not data or not all(k in data for k in REQUIRED_KEYS):
        return {"error": "Essential weather data missing"}

    return {
        "data": {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "current": parse_current_weather(data.get("current_weather", {})),
            "hourly": parse_hourly_weather(data.get("hourly", {})),
            "daily": parse_daily_weather(data.get("daily", {})),
            "units": parse_weather_units(data.get("current_weather_units", {})),
        }
    }
