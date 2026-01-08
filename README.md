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

    GET /city?name=villupuram

Response:

    {
      "data": [
        { "name": "Villupuram / Tamil Nadu / India", "latitude": 12.9, "longitude": 79.1 }
      ]
    }

------------------------------------------------------------------------

### Weather Data

    GET /weather?latitude=13&longitude=77.625

Response:

    {
      "data": {
        "condition": "Mainly clear",
        "temperature": 26.5,
        "windspeed": 13.4,
        "winddirection": 54,
        "is_day": true,
        "time": "2026-01-07T11:45",
        "units": {
          "temperature": "°C",
          "windspeed": "km/h",
          "winddirection": "°"
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
    python app.py

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
