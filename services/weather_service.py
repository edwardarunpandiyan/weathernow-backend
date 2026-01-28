import requests
from datetime import datetime
from utils.weather_codes import WEATHER_CODE_MAP

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

SHORT_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def degrees_to_compass(deg: float) -> str:
    directions = ["N","NE","E","SE","S","SW","W","NW"]
    idx = round(deg / 45) % 8
    return directions[idx]

def format_time_label(dt: datetime) -> str:
    return dt.strftime("%-I:%M %p")

def get_short_day_name(date_str: str) -> str:
    """
    Converts 'YYYY-MM-DD' to short English weekday (Mon, Tue, etc.)
    Deterministic and locale-independent.
    """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return SHORT_DAYS[dt.weekday()]
    except Exception:
        return ""  # Fail-safe for bad data

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
            "id": i+1,
            "date": times[i],
            "day": get_short_day_name(times[i]),
            "maxTemp": max_temps[i],
            "minTemp": min_temps[i],
            "condition": WEATHER_CODE_MAP.get(codes[i], "Unknown"),
        })
    return daily_data

# def parse_hourly_weather(hourly: dict) -> list:
#     if not hourly or not isinstance(hourly, dict):
#         return []
#     times = hourly.get("time", [])
#     temps = hourly.get("temperature_2m", [])
#     speeds = hourly.get("windspeed_10m", [])
#     codes = hourly.get("weathercode", [])

#     length = min(len(times), len(temps), len(speeds), len(codes))

#     hourly_data = []
#     for i in range(length):
#         hourly_data.append({
#             "date": times[i],
#             "temperature": temps[i],
#             "windspeed": speeds[i],
#             "condition": WEATHER_CODE_MAP.get(codes[i], "Unknown"),
#         })
#     return hourly_data

def parse_hourly_weather(hourly: dict, current_weather: dict) -> list:
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    feels = hourly.get("apparent_temperature", [])
    humidity = hourly.get("relative_humidity_2m", [])
    precip = hourly.get("precipitation", [])
    codes = hourly.get("weathercode", [])
    wind_speeds = hourly.get("windspeed_10m", [])
    wind_dirs = hourly.get("winddirection_10m", [])

    length = min(len(times), len(temps), len(feels), len(humidity),
                 len(precip), len(codes), len(wind_speeds), len(wind_dirs))

    current_dt = None
    if current_weather and current_weather.get("time"):
        current_dt = datetime.fromisoformat(current_weather["time"])

    hourly_data = []

    for i in range(length):
        hour_dt = datetime.fromisoformat(times[i])

        # Check if this is the "current hour slot"
        is_current_hour = (
            current_dt
            and hour_dt.year == current_dt.year
            and hour_dt.month == current_dt.month
            and hour_dt.day == current_dt.day
            and hour_dt.hour == current_dt.hour
        )

        # Use real current time label for current hour
        if is_current_hour:
            time_label = format_time_label(current_dt)   # 5:21 PM
            is_now = True
        else:
            time_label = format_time_label(hour_dt)      # 5:00 PM
            is_now = False

        wind_dir_compass = degrees_to_compass(wind_dirs[i])

        hourly_data.append({
            "id": i,
            "hour": hour_dt.hour,
            "timeLabel": time_label,
            "condition": WEATHER_CODE_MAP.get(codes[i], "Unknown"),
            "temp": round(temps[i]),
            "feelsLike": round(feels[i]),
            "windSpeed": round(wind_speeds[i]),
            "windDir": wind_dir_compass,
            "wind": f"{round(wind_speeds[i])} km/h {wind_dir_compass}",
            "humidity": humidity[i],
            "precipitation": precip[i],
            "isNow": is_now
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
    # response = requests.get(
    #     WEATHER_URL,
    #     params={
    #         "latitude": latitude,
    #         "longitude": longitude,
    #         "current_weather": True,
    #         "hourly": "temperature_2m,weathercode,windspeed_10m",
    #         "daily": "temperature_2m_max,temperature_2m_min,weathercode",
    #         "forecast_days": "7",
    #         "timezone": "auto"
    #     }
    # )

    response = requests.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
            "hourly": ",".join([
                        "temperature_2m",
                        "apparent_temperature",
                        "relative_humidity_2m",
                        "precipitation",
                        "weathercode",
                        "windspeed_10m",
                        "winddirection_10m",
                        ]),
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
            "hourly": parse_hourly_weather(data.get("hourly", {}), data.get("current_weather", {})),
            "daily": parse_daily_weather(data.get("daily", {})),
            "units": parse_weather_units(data.get("current_weather_units", {})),
        }
    }
