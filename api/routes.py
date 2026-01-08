from flask import Blueprint, request, jsonify
from app.services.weather_service import get_weather_by_coords
from app.services.geocoding_service import search_city

api = Blueprint("api", __name__)

@api.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "Backend running"})

@api.route("/weather", methods=["GET"])
def weather():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    if not latitude or not longitude:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    return jsonify(get_weather_by_coords(latitude, longitude))

@api.route("/city", methods=["GET"])
def city():
    name = request.args.get("name")

    if not name:
        return jsonify({"error": "City name is required"}), 400

    return jsonify(search_city(name))
