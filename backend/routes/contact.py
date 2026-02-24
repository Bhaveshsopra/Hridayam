"""Contact form API routes."""

from flask import Blueprint, request, jsonify
from database import db, ContactMessage

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["POST"])
def submit_contact():
    """
    Handle contact form submission.

    Expected JSON:
    {
        "name": "Ravi Sharma",
        "email": "ravi@email.com",
        "user_type": "Traveler planning a trip",
        "message": "I want to plan a heritage trip..."
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data provided",
            }), 400

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        message = data.get("message", "").strip()

        # Validation
        if not name:
            return jsonify({
                "success": False,
                "message": "Name is required",
            }), 400

        if not email or "@" not in email:
            return jsonify({
                "success": False,
                "message": "Valid email is required",
            }), 400

        if not message:
            return jsonify({
                "success": False,
                "message": "Message is required",
            }), 400

        # Save to database
        contact = ContactMessage(
            name=name,
            email=email,
            user_type=data.get(
                "user_type", "General"
            ),
            message=message,
        )
        db.session.add(contact)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": (
                f"Thank you, {name}! 🙏 Your message has "
                f"been received. We'll respond within "
                f"24 hours to {email}."
            ),
            "contact_id": contact.id,
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}",
        }), 500


@contact_bp.route("/contact/list", methods=["GET"])
def list_contacts():
    """List all contact messages (admin)."""
    messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).limit(50).all()

    return jsonify({
        "success": True,
        "count": len(messages),
        "messages": [m.to_dict() for m in messages],
    })