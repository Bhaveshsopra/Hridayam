"""Chatbot API routes."""

from flask import Blueprint, request, jsonify
from database import db, ChatHistory
from services.chatbot_engine import ChatbotEngine
import uuid

chatbot_bp = Blueprint("chatbot", __name__)
chatbot = ChatbotEngine()


@chatbot_bp.route("/chatbot", methods=["POST"])
def chat():
    """
    Chat with AI tourism assistant.

    Expected JSON:
    {
        "message": "Tell me about Khajuraho",
        "language": "en",
        "session_id": "optional-session-id"
    }
    """
    try:
        data = request.get_json()

        if not data or not data.get("message"):
            return jsonify({
                "success": False,
                "message": "Please send a message.",
            }), 400

        message = data["message"].strip()
        language = data.get("language", "en")
        session_id = data.get(
            "session_id", str(uuid.uuid4())[:8]
        )

        # Get chatbot response
        response = chatbot.get_response(
            message=message,
            language=language,
            session_id=session_id,
        )

        # Save chat history
        chat_log = ChatHistory(
            session_id=session_id,
            user_message=message,
            bot_response=response["response"],
            language=language,
        )
        db.session.add(chat_log)
        db.session.commit()

        return jsonify({
            "success": True,
            "response": response["response"],
            "type": response.get("type", "general"),
            "suggestions": response.get(
                "suggestions", []
            ),
            "session_id": session_id,
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "response": (
                "Sorry, I'm having trouble right now. "
                "Please try again!"
            ),
            "error": str(e),
        }), 500


@chatbot_bp.route(
    "/chatbot/history/<session_id>",
    methods=["GET"],
)
def chat_history(session_id):
    """Get chat history for a session."""
    history = (
        ChatHistory.query.filter_by(
            session_id=session_id
        )
        .order_by(ChatHistory.created_at.asc())
        .all()
    )

    return jsonify({
        "success": True,
        "session_id": session_id,
        "history": [
            {
                "user": h.user_message,
                "bot": h.bot_response,
                "time": h.created_at.isoformat(),
            }
            for h in history
        ],
    })