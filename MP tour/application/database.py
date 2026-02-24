from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class TripPlan(db.Model):
    """Stores generated trip plans."""

    __tablename__ = "trip_plans"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    budget = db.Column(db.Float, nullable=False)
    days = db.Column(db.Integer, default=3)
    interests = db.Column(db.String(500))
    travelers = db.Column(db.Integer, default=1)
    generated_plan = db.Column(db.Text)
    total_cost = db.Column(db.Float)
    safety_score = db.Column(db.Integer)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "budget": self.budget,
            "days": self.days,
            "interests": self.interests,
            "travelers": self.travelers,
            "generated_plan": self.generated_plan,
            "total_cost": self.total_cost,
            "safety_score": self.safety_score,
            "created_at": self.created_at.isoformat(),
        }


class ContactMessage(db.Model):
    """Stores contact form submissions."""

    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(50))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "user_type": self.user_type,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
        }


class SOSAlert(db.Model):
    """Emergency SOS alerts."""

    __tablename__ = "sos_alerts"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location_name = db.Column(db.String(200))
    alert_type = db.Column(
        db.String(50), default="general"
    )  # general, women_safety, medical
    status = db.Column(
        db.String(20), default="active"
    )  # active, responded, resolved
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    resolved_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location_name": self.location_name,
            "alert_type": self.alert_type,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


class ChatHistory(db.Model):
    """Chatbot conversation logs."""

    __tablename__ = "chat_history"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50))
    user_message = db.Column(db.Text)
    bot_response = db.Column(db.Text)
    language = db.Column(db.String(10), default="en")
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )


class PlaceVisit(db.Model):
    """Track place visit analytics."""

    __tablename__ = "place_visits"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.String(50))
    visit_date = db.Column(db.Date)
    crowd_level = db.Column(db.Integer)  # 1-10
    weather = db.Column(db.String(50))
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )


def init_db(app):
    """Initialize database with app context."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully")