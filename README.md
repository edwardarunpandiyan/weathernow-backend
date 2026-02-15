# WeatherNow Backend

WeatherNow Backend is a Python-based REST API that provides city
suggestions, geocoding, and normalized weather data for frontend
consumption.

It abstracts third-party APIs and returns clean, frontend-ready JSON
responses.

------------------------------------------------------------------------

## 🚀 Features

-   City autocomplete search API
-   City-to-latitude/longitude resolution
-   Real-time weather retrieval using Open-Meteo
-   Weather code to human-readable condition mapping
-   Normalized API responses for frontend simplicity

------------------------------------------------------------------------

## 🛠 Tech Stack

-   Python
-   Flask / FastAPI
-   Requests
-   Open-Meteo Weather API
-   Open-Meteo Geocoding API

------------------------------------------------------------------------

## 📂 Project Structure

    backend/
    ├── app.py
    ├── services/
    │   ├── weather_service.py
    │   └── geocoding_service.py
    ├── utils/
    │   └── weather_codes.py
    └── requirements.txt

------------------------------------------------------------------------

## 📡 API Endpoints

### City Suggestions

    GET /city?name=london

Response:

    {
      "data": [
        {
            "country": "United Kingdom",
            "country_code": "GB",
            "id": 2643743,
            "latitude": 51.50853,
            "longitude": -0.12574,
            "name": "London",
            "state": "England"
        },
      ]
    }

------------------------------------------------------------------------

### Weather Data

    GET /weather?latitude=51&longitude=-0.12

Response:

    {
      "data": {
        "daily": [
          {
            "condition": "Light rain showers",
            "date": "2026-02-15",
            "day": "Sun",
            "id": 1,
            "maxTemp": 8.1,
            "minTemp": 3,
            "weatherCode": 80
          }
        ],    
        "hourly": [
          {
            "condition": "Overcast",
            "feelsLike": 0,
            "hour": 0,
            "humidity": 73,
            "id": 0,
            "isDay": false,
            "isNow": false,
            "precipitation": 0,
            "temp": 3,
            "timeLabel": "12:00 AM",
            "weatherCode": 3,
            "wind": "8 km/h S",
            "windDir": "S",
            "windSpeed": 8
          }
        ],
        "latitude": 51,
        "locationNow": "2026-02-15T06:35:50.372107+00:00",
        "longitude": -0.120000124,
        "units": {
          "temperature": "°C",
          "winddirection": "°",
          "windspeed": "km/h"
        }
      }
}

------------------------------------------------------------------------

## ▶️ Getting Started

### Prerequisites

-   Python 3.9+
-   pip

### Installation

    pip install -r requirements.txt
    python main.py

Server runs on:

    http://localhost:5000

------------------------------------------------------------------------

## 📌 Design Principles

-   Backend owns all third-party API integrations
-   Frontend receives only UI-ready data
-   Clean and predictable API contracts
-   Easy to extend for forecasts and geolocation

------------------------------------------------------------------------

## 📄 License

MIT
