import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

def search_city(name):
    response = requests.get(
        GEOCODING_URL,
        params={
            "name": name,
            "language": "en"
        }
    )

    if response.status_code != 200:
        return {"error": "City data not found"}

    data = response.json()

    if not data.get("results"):
        return {"data": []}

    results = []
    for city in data["results"]:
        results.append({
            "id": city['id'],
            "name": city['name'],
            "state": city.get('admin1', ''),
            "country": city['country'],
            "country_code": city['country_code'],
            "latitude": city["latitude"],
            "longitude": city["longitude"]
        })

    return {"data": results}
