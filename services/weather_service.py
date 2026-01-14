import requests
from utils.weather_codes import WEATHER_CODE_MAP

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

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
    if not data or "current_weather" not in data:
        return {"error": "Current weather data not available"}

    current = data["current_weather"]
    daily_data = data["daily"] if data.get("daily") else {}
    # daily_data = data["daily"]
    daily = []
    for i in range(len(daily_data["time"])):
         daily.append(
            {
            "date": daily_data["time"][i],
            "max_temperature": daily_data["temperature_2m_max"][i],
            "min_temperature": daily_data["temperature_2m_min"][i],
            "condition": WEATHER_CODE_MAP.get(daily_data["weathercode"][i], "Unknown")
            }
         )

    return {
        "data": {
            "current": {
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "temperature": current["temperature"],
                "condition": WEATHER_CODE_MAP.get(current["weathercode"], "Unknown"),
                "windspeed": current["windspeed"],
                "winddirection": current["winddirection"],
                "time": current["time"],
                "is_day": bool(current["is_day"]),
            },
            "daily": daily,
            "units": {
                "temperature": data["current_weather_units"]["temperature"],
                "windspeed": data["current_weather_units"]["windspeed"],
                "winddirection": data["current_weather_units"]["winddirection"]
            }
        }
    }
