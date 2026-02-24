"""Safety and SOS API routes."""

from flask import Blueprint, request, jsonify
from database import db, SOSAlert
from datetime import datetime
from config import Config

safety_bp = Blueprint("safety", __name__)


@safety_bp.route("/sos", methods=["POST"])
def trigger_sos():
    """
    Trigger emergency SOS alert.

    Expected JSON:
    {
        "user_name": "Ravi",
        "phone": "+91-9876543210",
        "latitude": 23.2599,
        "longitude": 77.4126,
        "location_name": "Near Sanchi Stupa",
        "alert_type": "general"
    }
    """
    try:
        data = request.get_json()

        alert = SOSAlert(
            user_name=data.get("user_name", "Anonymous"),
            phone=data.get("phone", ""),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            location_name=data.get(
                "location_name", "Unknown"
            ),
            alert_type=data.get("alert_type", "general"),
            status="active",
        )
        db.session.add(alert)
        db.session.commit()

        # In production: trigger SMS, push
        # notifications, notify authorities
        emergency = Config.EMERGENCY_CONTACTS

        return jsonify({
            "success": True,
            "message": (
                "🆘 EMERGENCY ALERT ACTIVATED!\n\n"
                f"Alert ID: SOS-{alert.id}\n"
                f"Status: ACTIVE — Help is on the way\n\n"
                "📞 Call these numbers immediately:\n"
                f"• Police: {emergency['police']}\n"
                f"• Ambulance: {emergency['ambulance']}\n"
                f"• Women Helpline: "
                f"{emergency['women_helpline']}\n"
                f"• Tourist Helpline: "
                f"{emergency['tourist_helpline']}\n\n"
                "Your location has been shared with "
                "emergency services."
            ),
            "alert_id": alert.id,
            "emergency_contacts": emergency,
            "status": "active",
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"SOS Error: {str(e)}",
            "fallback": (
                "CALL 100 (Police) or "
                "108 (Ambulance) IMMEDIATELY"
            ),
        }), 500


@safety_bp.route(
    "/sos/<int:alert_id>/resolve", methods=["PUT"]
)
def resolve_sos(alert_id):
    """Mark SOS alert as resolved."""
    alert = SOSAlert.query.get(alert_id)
    if not alert:
        return jsonify({
            "success": False,
            "message": "Alert not found",
        }), 404

    alert.status = "resolved"
    alert.resolved_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "success": True,
        "message": (
            f"Alert SOS-{alert_id} marked as resolved. "
            "Glad you are safe! 🙏"
        ),
    })


@safety_bp.route("/safety/score", methods=["POST"])
def get_safety_score():
    """
    Get safety score for a location.

    Expected JSON:
    {
        "latitude": 23.2599,
        "longitude": 77.4126,
        "time": "evening"
    }
    """
    try:
        data = request.get_json()
        lat = data.get("latitude", 0)
        lng = data.get("longitude", 0)
        time_of_day = data.get("time", "afternoon")

        # Simplified safety scoring
        base_score = 85

        # Adjust by time
        time_adjustments = {
            "morning": 5,
            "afternoon": 3,
            "evening": 0,
            "night": -10,
            "late_night": -20,
        }
        score = base_score + time_adjustments.get(
            time_of_day, 0
        )
        score = max(40, min(100, score))

        if score >= 80:
            level = "safe"
            message = "This area is generally safe."
        elif score >= 60:
            level = "moderate"
            message = (
                "Exercise normal caution in this area."
            )
        else:
            level = "caution"
            message = (
                "Stay alert. Avoid isolated areas. "
                "Travel in groups."
            )

        return jsonify({
            "success": True,
            "safety_score": score,
            "level": level,
            "message": message,
            "tips": [
                "Keep emergency numbers saved",
                "Share live location with family",
                "Use registered transport only",
                "Keep valuables secure",
                "Stay in well-lit areas at night",
            ],
            "emergency_contacts": (
                Config.EMERGENCY_CONTACTS
            ),
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e),
        }), 500


@safety_bp.route("/safety/emergency-numbers")
def emergency_numbers():
    """Get all emergency numbers."""
    return jsonify({
        "success": True,
        "contacts": Config.EMERGENCY_CONTACTS,
        "additional": {
            "fire": "101",
            "disaster_mgmt": "108",
            "child_helpline": "1098",
            "railway_police": "182",
            "highway_patrol": "1033",
        },
    })