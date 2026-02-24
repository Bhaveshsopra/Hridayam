"""Places and exploration API routes."""

import json
import os
from flask import Blueprint, request, jsonify
from services.crowd_predictor import CrowdPredictor

places_bp = Blueprint("places", __name__)


def load_places():
    """Load places data from JSON."""
    path = os.path.join(
        os.path.dirname(__file__),
        "..", "data", "places.json",
    )
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"places": []}


@places_bp.route("/places", methods=["GET"])
def get_all_places():
    """
    Get all tourist places.
    Optional query params: type, city, min_rating
    """
    data = load_places()
    places = data.get("places", [])

    # Filter by type
    place_type = request.args.get("type")
    if place_type:
        places = [
            p for p in places
            if place_type.lower() in p.get("type", [])
        ]

    # Filter by city
    city = request.args.get("city")
    if city:
        places = [
            p for p in places
            if city.lower() in p.get("city", "").lower()
        ]

    # Filter by min rating
    min_rating = request.args.get("min_rating")
    if min_rating:
        places = [
            p for p in places
            if p.get("rating", 0) >= float(min_rating)
        ]

    return jsonify({
        "success": True,
        "count": len(places),
        "places": places,
    })


@places_bp.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """Get single place details."""
    data = load_places()
    place = next(
        (
            p
            for p in data.get("places", [])
            if p["id"] == place_id
        ),
        None,
    )

    if not place:
        return jsonify({
            "success": False,
            "message": "Place not found",
        }), 404

    return jsonify({"success": True, "place": place})


@places_bp.route(
    "/places/<place_id>/crowd", methods=["GET"]
)
def get_crowd(place_id):
    """Get crowd prediction for a place."""
    time_of_day = request.args.get(
        "time", "morning"
    )
    prediction = CrowdPredictor.predict(
        place_id, time_of_day=time_of_day
    )

    return jsonify({
        "success": True,
        "prediction": prediction,
    })


@places_bp.route("/places/search", methods=["GET"])
def search_places():
    """Search places by keyword."""
    query = request.args.get("q", "").lower()

    if not query:
        return jsonify({
            "success": False,
            "message": "Provide search query: ?q=khajuraho",
        }), 400

    data = load_places()
    results = []

    for place in data.get("places", []):
        searchable = (
            f"{place.get('name', '')} "
            f"{place.get('city', '')} "
            f"{place.get('description', '')} "
            f"{' '.join(place.get('type', []))}"
        ).lower()

        if query in searchable:
            results.append(place)

    return jsonify({
        "success": True,
        "query": query,
        "count": len(results),
        "results": results,
    })