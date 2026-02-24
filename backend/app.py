"""
AI Smart Tourism MP — Flask Backend
Main application factory and configuration.
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from database import db, init_db

# Import route blueprints
from routes.planner import planner_bp
from routes.contact import contact_bp
from routes.safety import safety_bp
from routes.chatbot import chatbot_bp
from routes.places import places_bp
from routes.weather import weather_bp


def create_app():
    """Application factory."""
    app = Flask(
        __name__,
        static_folder="static",
        static_url_path="",
    )
    app.config.from_object(Config)

    # Enable CORS for all routes
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
    )

    # Initialize database
    init_db(app)

    # Register blueprints (all API routes)
    app.register_blueprint(planner_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(safety_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(weather_bp)

    # ─── ROOT & HEALTH ROUTES ─── #

    @app.route("/")
    def index():
        """Serve the frontend."""
        return send_from_directory("static", "index.html")

    @app.route("/health")
    def health():
        """API health check."""
        return jsonify({
            "status": "healthy",
            "service": "AI Smart Tourism MP",
            "version": "1.0.0",
            "endpoints": {
                "POST /plan": "Generate AI trip plan",
                "POST /plan/quick": "Quick trip plan",
                "POST /contact": "Submit contact form",
                "POST /sos": "Emergency SOS alert",
                "POST /chatbot": "Chat with AI assistant",
                "GET  /places": "Get all tourist places",
                "GET  /places/<id>": "Get place details",
                "GET  /places/<id>/crowd": "Crowd prediction",
                "GET  /places/search?q=": "Search places",
                "GET  /weather/<city>": "Get weather",
                "GET  /weather": "All cities weather",
                "POST /budget/optimize": "Budget optimizer",
                "GET  /safety/emergency-numbers": "Emergency contacts",
                "POST /safety/score": "Location safety score",
            },
        })

    @app.route("/api")
    def api_info():
        """API documentation."""
        return jsonify({
            "name": "AI Smart Tourism MP API",
            "version": "1.0.0",
            "description": (
                "AI-powered tourism platform for "
                "Madhya Pradesh, India"
            ),
            "base_url": "http://127.0.0.1:5000",
            "documentation": "/health",
            "contact": "info@aismartourism.mp.in",
        })

    # ─── ERROR HANDLERS ─── #

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "success": False,
            "message": "Endpoint not found",
        }), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({
            "success": False,
            "message": "Internal server error",
        }), 500

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "success": False,
            "message": "Method not allowed",
        }), 405

    return app


# Create app instance
app = create_app()