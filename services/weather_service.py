import requests
from app.utils.weather_codes import WEATHER_CODE_MAP

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather_by_coords(latitude, longitude):
    response = requests.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True
        }
    )

    if response.status_code != 200:
        return {"error": "Weather data not found"}

    data = response.json()
    current = data["current_weather"]

    return {
        "data": {
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "temperature": current["temperature"],
            "condition": WEATHER_CODE_MAP.get(current["weathercode"], "Unknown"),
            "windspeed": current["windspeed"],
            "winddirection": current["winddirection"],
            "time": current["time"],
            "is_day": bool(current["is_day"]),
            "units": {
                "temperature": data["current_weather_units"]["temperature"],
                "windspeed": data["current_weather_units"]["windspeed"],
                "winddirection": data["current_weather_units"]["winddirection"]
            }
        }
    }
