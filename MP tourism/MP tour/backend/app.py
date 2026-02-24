"""
app.py — AI Smart Tourism MP
Flask backend for the Hridayam AI tourism platform for Madhya Pradesh.

Run:
    pip install flask flask-cors
    python app.py

Endpoints:
    GET  /                      → Serve main HTML page
    POST /api/itinerary         → Generate AI trip itinerary
    POST /api/contact           → Handle contact form submissions
    POST /api/sos               → Trigger emergency SOS alert
    GET  /api/destinations      → Return list of MP destinations
    GET  /api/weather/<city>    → Return mock weather data for a city
    GET  /api/crowd/<place>     → Return crowd prediction for a place
    GET  /api/budget            → Return budget estimate breakdown
"""

from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
from datetime import datetime
import random
import os
import json

app = Flask(__name__, static_folder="static")
CORS(app)

# ─── LOAD HTML ──────────────────────────────────────────────────────────────
HTML_FILE = os.path.join(os.path.dirname(__file__), "index.html")


# ─── STATIC DATA ────────────────────────────────────────────────────────────

DESTINATIONS = [
    {
        "id": "khajuraho",
        "name": "Khajuraho Temples",
        "district": "Chhatarpur",
        "category": "UNESCO World Heritage",
        "description": "Marvel at 85 medieval Hindu and Jain temples adorned with intricate carvings — masterpieces of Chandela architecture.",
        "best_time": "October – March",
        "entry_fee": 40,  # INR
        "lat": 24.8318,
        "lng": 79.9199,
        "tags": ["history", "architecture", "heritage"],
    },
    {
        "id": "sanchi",
        "name": "Sanchi Stupa",
        "district": "Raisen",
        "category": "Buddhist Heritage",
        "description": "Emperor Ashoka's 3rd century BCE Buddhist stupa — one of the oldest stone structures in India.",
        "best_time": "October – March",
        "entry_fee": 30,
        "lat": 23.4793,
        "lng": 77.7402,
        "tags": ["history", "spirituality", "heritage"],
    },
    {
        "id": "ujjain",
        "name": "Ujjain Mahakaleshwar",
        "district": "Ujjain",
        "category": "Jyotirlinga Shrine",
        "description": "One of India's 12 sacred Jyotirlingas. Experience the mesmerizing Bhasma Aarti at dawn.",
        "best_time": "October – March",
        "entry_fee": 0,
        "lat": 23.1828,
        "lng": 75.7682,
        "tags": ["spirituality", "religion", "culture"],
    },
    {
        "id": "pachmarhi",
        "name": "Pachmarhi",
        "district": "Hoshangabad",
        "category": "Hill Station · Nature",
        "description": "MP's only hill station — lush Satpura forests, ancient caves, enchanting waterfalls.",
        "best_time": "October – June",
        "entry_fee": 0,
        "lat": 22.4675,
        "lng": 78.4340,
        "tags": ["nature", "adventure", "wildlife"],
    },
    {
        "id": "bhimbetka",
        "name": "Bhimbetka Caves",
        "district": "Raisen",
        "category": "30,000 BCE Rock Art",
        "description": "Over 700 rock shelters with cave paintings spanning 30,000 years — a window into our ancestors.",
        "best_time": "October – March",
        "entry_fee": 25,
        "lat": 22.9358,
        "lng": 77.6122,
        "tags": ["history", "heritage", "adventure"],
    },
    {
        "id": "orchha",
        "name": "Orchha Fort",
        "district": "Tikamgarh",
        "category": "Bundelkhand Heritage",
        "description": "A perfectly preserved Bundela kingdom — palaces, temples, and cenotaphs rising from the Betwa river.",
        "best_time": "October – March",
        "entry_fee": 25,
        "lat": 25.3521,
        "lng": 78.6415,
        "tags": ["history", "architecture", "heritage"],
    },
    {
        "id": "bandhavgarh",
        "name": "Bandhavgarh Tiger Reserve",
        "district": "Umaria",
        "category": "Wildlife Safari",
        "description": "Highest density of Royal Bengal Tigers in India. Ancient fort ruins inside a wild jungle paradise.",
        "best_time": "October – June",
        "entry_fee": 1500,
        "lat": 23.7196,
        "lng": 81.0406,
        "tags": ["wildlife", "nature", "adventure"],
    },
    {
        "id": "mandu",
        "name": "Mandu",
        "district": "Dhar",
        "category": "Afghan Architecture",
        "description": "City of joy — romantic ruins of an Afghan-era kingdom perched dramatically on a clifftop plateau.",
        "best_time": "July – March",
        "entry_fee": 25,
        "lat": 22.3644,
        "lng": 75.3966,
        "tags": ["history", "architecture", "heritage"],
    },
    {
        "id": "gwalior",
        "name": "Gwalior Fort",
        "district": "Gwalior",
        "category": "Rajput Fortress",
        "description": "The 'Gibraltar of India' — a towering 8th-century fort with spectacular Jain sculptures and royal palaces.",
        "best_time": "October – March",
        "entry_fee": 75,
        "lat": 26.2232,
        "lng": 78.1686,
        "tags": ["history", "architecture", "heritage"],
    },
    {
        "id": "kanha",
        "name": "Kanha National Park",
        "district": "Mandla",
        "category": "Tiger Reserve",
        "description": "Inspiration for Rudyard Kipling's Jungle Book — home to Barasingha deer, tigers, and leopards.",
        "best_time": "October – June",
        "entry_fee": 1200,
        "lat": 22.2591,
        "lng": 80.6122,
        "tags": ["wildlife", "nature", "adventure"],
    },
]

WEATHER_DATA = {
    "bhopal":     {"temp": 24, "condition": "Partly Cloudy", "humidity": 52, "icon": "⛅"},
    "khajuraho":  {"temp": 26, "condition": "Clear", "humidity": 38, "icon": "☀️"},
    "ujjain":     {"temp": 27, "condition": "Sunny", "humidity": 35, "icon": "☀️"},
    "pachmarhi":  {"temp": 18, "condition": "Cool & Clear", "humidity": 68, "icon": "🌤️"},
    "orchha":     {"temp": 25, "condition": "Clear", "humidity": 40, "icon": "☀️"},
    "gwalior":    {"temp": 23, "condition": "Hazy", "humidity": 44, "icon": "🌫️"},
    "mandu":      {"temp": 22, "condition": "Pleasant", "humidity": 55, "icon": "⛅"},
    "sanchi":     {"temp": 24, "condition": "Clear", "humidity": 46, "icon": "☀️"},
    "bandhavgarh":{"temp": 28, "condition": "Sunny", "humidity": 42, "icon": "☀️"},
    "kanha":      {"temp": 27, "condition": "Warm", "humidity": 48, "icon": "🌤️"},
}

CROWD_LEVELS = ["Very Low", "Low", "Moderate", "High", "Very High"]

INTERESTS_MAP = {
    "history":     ["khajuraho", "sanchi", "bhimbetka", "orchha", "gwalior", "mandu"],
    "spirituality":["ujjain", "orchha"],
    "nature":      ["pachmarhi", "bandhavgarh", "kanha"],
    "wildlife":    ["bandhavgarh", "kanha", "pachmarhi"],
    "adventure":   ["pachmarhi", "bandhavgarh", "kanha", "bhimbetka"],
    "culture":     ["ujjain", "orchha", "gwalior", "mandu"],
    "architecture":["khajuraho", "orchha", "gwalior", "mandu"],
}

SAMPLE_HOTELS = {
    "budget":   {"name": "MP Tourism Yatri Niwas",   "price_per_night": 700},
    "mid":      {"name": "Hotel Jehan Numa",          "price_per_night": 1800},
    "luxury":   {"name": "Taj Lake Front Bhopal",     "price_per_night": 7500},
}


# ─── HELPER FUNCTIONS ────────────────────────────────────────────────────────

def get_hotel_tier(budget_per_day: float) -> str:
    if budget_per_day < 1500:
        return "budget"
    elif budget_per_day < 4000:
        return "mid"
    return "luxury"


def build_itinerary(budget: int, days: int, interests: list) -> dict:
    """Build a simplified AI-style itinerary based on inputs."""
    daily_budget = budget / days if days else budget
    hotel_tier = get_hotel_tier(daily_budget)
    hotel = SAMPLE_HOTELS[hotel_tier]

    # Pick destinations based on interests
    scored = {}
    for interest in interests:
        for dest_id in INTERESTS_MAP.get(interest.lower(), []):
            scored[dest_id] = scored.get(dest_id, 0) + 1

    # Fallback if no interests matched
    if not scored:
        scored = {d["id"]: 1 for d in DESTINATIONS[:days]}

    # Sort by score, pick top `days` destinations
    sorted_dests = sorted(scored, key=lambda x: scored[x], reverse=True)
    selected_ids = sorted_dests[:days]
    selected = [d for d in DESTINATIONS if d["id"] in selected_ids]

    # Build day-by-day plan
    itinerary_days = []
    total_entry = 0
    for i, dest in enumerate(selected, 1):
        total_entry += dest.get("entry_fee", 0)
        itinerary_days.append({
            "day": i,
            "destination": dest["name"],
            "district": dest["district"],
            "category": dest["category"],
            "activities": [
                f"Arrive at {dest['name']} — AI audio guide activated",
                f"Explore main highlights ({dest['category']})",
                "Local cuisine recommendations via AI food guide",
                "Evening cultural experience or sunset viewpoint",
            ],
            "entry_fee": dest["entry_fee"],
            "ai_tip": f"Best visiting time: {dest.get('best_time', 'October – March')}. "
                      f"Crowd prediction: {'Low — great time!' if i % 2 == 0 else 'Moderate — arrive early.'}",
        })

    # Budget breakdown
    hotel_cost = hotel["price_per_night"] * days
    food_cost = 350 * days       # estimated per person per day
    transport_cost = 400 * days
    misc_cost = 200 * days

    total_estimated = hotel_cost + food_cost + transport_cost + total_entry + misc_cost
    safety_score = min(100, 85 + len(interests) * 2)

    return {
        "summary": {
            "total_days": days,
            "destinations_count": len(selected),
            "hotel": hotel,
            "hotel_tier": hotel_tier,
            "safety_score": safety_score,
        },
        "budget_breakdown": {
            "hotel": hotel_cost,
            "food": food_cost,
            "transport": transport_cost,
            "entry_fees": total_entry,
            "miscellaneous": misc_cost,
            "total_estimated": total_estimated,
            "input_budget": budget,
            "within_budget": total_estimated <= budget,
        },
        "days": itinerary_days,
    }


# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main HTML frontend."""
    if os.path.exists(HTML_FILE):
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            return f.read(), 200, {"Content-Type": "text/html; charset=utf-8"}
    return "<h2>index.html not found. Place it alongside app.py.</h2>", 404


@app.route("/api/itinerary", methods=["POST"])
def generate_itinerary():
    """
    Generate a personalized AI trip itinerary.

    Request JSON:
        {
            "budget": 15000,          // total budget in INR
            "days": 5,                // number of travel days
            "interests": ["history", "nature"]  // list of interest tags
        }

    Response JSON:
        { "success": true, "itinerary": { ... } }
    """
    data = request.get_json(silent=True) or {}

    budget = int(data.get("budget", 10000))
    days = int(data.get("days", 3))
    interests = data.get("interests", ["history"])

    # Basic validation
    if budget < 500:
        return jsonify({"success": False, "error": "Budget too low. Minimum ₹500 required."}), 400
    if not (1 <= days <= 15):
        return jsonify({"success": False, "error": "Days must be between 1 and 15."}), 400

    itinerary = build_itinerary(budget, days, interests)

    return jsonify({
        "success": True,
        "generated_at": datetime.now().isoformat(),
        "itinerary": itinerary,
    })


@app.route("/api/contact", methods=["POST"])
def contact():
    """
    Handle contact form submission.

    Request JSON:
        {
            "name": "Ravi Sharma",
            "email": "ravi@email.com",
            "role": "Traveler planning a trip",
            "message": "Hello..."
        }
    """
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    role = data.get("role", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "error": "Name, email, and message are required."}), 400

    # In production: save to DB / send email via SMTP or SendGrid
    print(f"[CONTACT] From: {name} <{email}> | Role: {role}")
    print(f"[CONTACT] Message: {message}")

    return jsonify({
        "success": True,
        "message": f"Thank you, {name}! We'll get back to you at {email} within 24 hours.",
    })


@app.route("/api/sos", methods=["POST"])
def sos_alert():
    """
    Trigger an emergency SOS alert.

    Request JSON:
        {
            "user_name": "Priya Singh",
            "lat": 24.8318,
            "lng": 79.9199,
            "contact_number": "+91 9876543210"
        }
    """
    data = request.get_json(silent=True) or {}

    user_name = data.get("user_name", "Anonymous Traveler")
    lat = data.get("lat")
    lng = data.get("lng")
    contact = data.get("contact_number", "N/A")

    alert_id = f"SOS-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"

    # In production: notify local police API, send SMS, push notification
    print(f"[SOS ALERT] {alert_id} | User: {user_name} | Location: {lat},{lng} | Contact: {contact}")

    return jsonify({
        "success": True,
        "alert_id": alert_id,
        "message": "SOS alert dispatched! Emergency services and your contacts have been notified.",
        "dispatched_to": ["Local Police (MP 100)", "Emergency Contact", "Nearest MP Tourism Help Desk"],
        "timestamp": datetime.now().isoformat(),
    })


@app.route("/api/destinations", methods=["GET"])
def get_destinations():
    """
    Return the full list of MP tourist destinations.

    Query params:
        tag   — filter by interest tag (e.g. ?tag=wildlife)
        limit — max results (default: all)
    """
    tag = request.args.get("tag", "").lower()
    limit = request.args.get("limit", type=int)

    results = DESTINATIONS
    if tag:
        results = [d for d in results if tag in d.get("tags", [])]
    if limit:
        results = results[:limit]

    return jsonify({
        "success": True,
        "count": len(results),
        "destinations": results,
    })


@app.route("/api/weather/<city>", methods=["GET"])
def get_weather(city: str):
    """
    Return weather data for a given MP city.

    Path param:
        city — e.g. /api/weather/bhopal
    """
    city_key = city.lower().strip()
    data = WEATHER_DATA.get(city_key)

    if not data:
        # Return generic warm weather for unknown MP cities
        data = {"temp": 25, "condition": "Partly Cloudy", "humidity": 50, "icon": "⛅"}

    return jsonify({
        "success": True,
        "city": city.title(),
        "weather": data,
        "fetched_at": datetime.now().isoformat(),
        "note": "Live weather integration (OpenWeatherMap) planned for Phase 2.",
    })


@app.route("/api/crowd/<place>", methods=["GET"])
def crowd_prediction(place: str):
    """
    Return crowd prediction for a tourist place.

    Path param:
        place — e.g. /api/crowd/khajuraho

    Query params:
        hour — hour of day 0–23 (default: current hour)
    """
    hour = request.args.get("hour", default=datetime.now().hour, type=int)

    # Simple crowd heuristic: peak hours 10–13 and 15–18
    if 10 <= hour <= 13 or 15 <= hour <= 18:
        level_idx = random.randint(3, 4)  # High / Very High
    elif 7 <= hour <= 9 or 18 <= hour <= 20:
        level_idx = random.randint(1, 2)  # Low / Moderate
    else:
        level_idx = 0  # Very Low

    recommendation = (
        "Great time to visit — minimal crowds!" if level_idx <= 1
        else "Moderate crowd expected. Arrive 30 min early."
        if level_idx == 2
        else "High crowd expected. Consider visiting at 7–9 AM or after 6 PM."
    )

    return jsonify({
        "success": True,
        "place": place.replace("-", " ").title(),
        "hour": hour,
        "crowd_level": CROWD_LEVELS[level_idx],
        "crowd_index": level_idx,
        "recommendation": recommendation,
        "predicted_at": datetime.now().isoformat(),
    })


@app.route("/api/budget", methods=["GET"])
def budget_estimator():
    """
    Return a quick budget estimate for an MP trip.

    Query params:
        days     — number of days (default: 3)
        tier     — budget | mid | luxury (default: budget)
        pax      — number of persons (default: 1)
    """
    days = request.args.get("days", default=3, type=int)
    tier = request.args.get("tier", default="budget").lower()
    pax  = request.args.get("pax", default=1, type=int)

    if tier not in SAMPLE_HOTELS:
        tier = "budget"

    hotel = SAMPLE_HOTELS[tier]
    hotel_cost   = hotel["price_per_night"] * days * pax
    food_cost    = 350 * days * pax
    transport    = 500 * days
    entry_fees   = 250 * days           # average
    misc         = 200 * days * pax

    total = hotel_cost + food_cost + transport + entry_fees + misc

    return jsonify({
        "success": True,
        "inputs": {"days": days, "tier": tier, "persons": pax},
        "breakdown": {
            "hotel": hotel_cost,
            "food": food_cost,
            "transport": transport,
            "entry_fees": entry_fees,
            "miscellaneous": misc,
        },
        "total_estimated_inr": total,
        "hotel_details": hotel,
        "per_day_average": round(total / days, 2),
    })


# ─── HEALTH CHECK ─────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "AI Smart Tourism MP — Hridayam Backend",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    })


# ─── ERROR HANDLERS ───────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Endpoint not found."}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "error": "Internal server error."}), 500


# ─── RUN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  Hridayam — AI Smart Tourism MP")
    print("  Backend server starting...")
    print("=" * 60)
    print(f"  Destinations loaded : {len(DESTINATIONS)}")
    print(f"  HTML file found     : {os.path.exists(HTML_FILE)}")
    print("=" * 60)
    print("  API Endpoints:")
    print("    GET  /                      → Frontend")
    print("    POST /api/itinerary         → Generate itinerary")
    print("    POST /api/contact           → Contact form")
    print("    POST /api/sos               → Emergency SOS")
    print("    GET  /api/destinations      → All MP destinations")
    print("    GET  /api/weather/<city>    → Weather data")
    print("    GET  /api/crowd/<place>     → Crowd prediction")
    print("    GET  /api/budget            → Budget estimator")
    print("    GET  /api/health            → Health check")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)