"""Trip planning API routes."""

from flask import Blueprint, request, jsonify
from database import db, TripPlan
from services.ai_planner import AITripPlanner
from services.budget_engine import BudgetEngine

planner_bp = Blueprint("planner", __name__)
ai_planner = AITripPlanner()


@planner_bp.route("/plan", methods=["POST"])
def generate_plan():
    """
    Generate AI trip plan.

    Expected JSON:
    {
        "name": "Ravi Sharma",
        "email": "ravi@email.com",
        "budget": 10000,
        "days": 3,
        "interests": ["heritage", "spiritual", "food"],
        "travelers": 2,
        "start_city": "Bhopal"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data provided. Send JSON body.",
            }), 400

        # Extract parameters with defaults
        name = data.get("name", "Traveler")
        email = data.get("email", "")
        budget = float(data.get("budget", 5000))
        days = int(data.get("days", 3))
        interests = data.get(
            "interests", ["heritage", "history"]
        )
        travelers = int(data.get("travelers", 1))
        start_city = data.get("start_city", "Bhopal")

        # Validate
        if budget < 500:
            return jsonify({
                "success": False,
                "message": (
                    "Budget too low. Minimum ₹500 required."
                ),
            }), 400

        if days < 1 or days > 30:
            return jsonify({
                "success": False,
                "message": "Days must be between 1 and 30.",
            }), 400

        # Handle interests as string or list
        if isinstance(interests, str):
            interests = [
                i.strip()
                for i in interests.split(",")
            ]

        # Generate itinerary
        itinerary = ai_planner.generate_itinerary(
            budget=budget,
            days=days,
            interests=interests,
            travelers=travelers,
            start_city=start_city,
        )

        # Get budget optimization
        budget_plan = BudgetEngine.optimize_budget(
            budget, days, travelers
        )

        # Save to database
        trip = TripPlan(
            user_name=name,
            email=email,
            budget=budget,
            days=days,
            interests=",".join(interests),
            travelers=travelers,
            generated_plan=str(itinerary),
            total_cost=itinerary["total_estimated_cost"],
            safety_score=itinerary["safety_score"],
        )
        db.session.add(trip)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": (
                f"🎉 AI Trip Plan generated for {name}! "
                f"{days}-day {itinerary['trip_name']} — "
                f"Estimated cost: "
                f"₹{itinerary['total_estimated_cost']}/person"
            ),
            "plan_id": trip.id,
            "itinerary": itinerary,
            "budget_optimization": budget_plan,
        }), 200

    except ValueError as e:
        return jsonify({
            "success": False,
            "message": f"Invalid input: {str(e)}",
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}",
        }), 500


@planner_bp.route("/plan/<int:plan_id>", methods=["GET"])
def get_plan(plan_id):
    """Retrieve a saved trip plan."""
    trip = TripPlan.query.get(plan_id)
    if not trip:
        return jsonify({
            "success": False,
            "message": "Plan not found",
        }), 404

    return jsonify({
        "success": True,
        "plan": trip.to_dict(),
    })


@planner_bp.route("/plan/quick", methods=["POST"])
def quick_plan():
    """
    Quick plan with minimal inputs.
    Just name and budget (backward compatible
    with original frontend).
    """
    try:
        data = request.get_json()
        name = data.get("name", "Traveler")
        budget = float(data.get("budget", 5000))

        itinerary = ai_planner.generate_itinerary(
            budget=budget,
            days=3,
            interests=["heritage", "spiritual", "nature"],
            travelers=1,
            start_city="Bhopal",
        )

        trip = TripPlan(
            user_name=name,
            budget=budget,
            days=3,
            interests="heritage,spiritual,nature",
            generated_plan=str(itinerary),
            total_cost=itinerary["total_estimated_cost"],
            safety_score=itinerary["safety_score"],
        )
        db.session.add(trip)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": (
                f"🎉 Hi {name}! Your 3-day MP trip is ready!\n\n"
                f"📍 {itinerary['trip_name']}\n"
                f"💰 Est. Cost: "
                f"₹{itinerary['total_estimated_cost']}/person\n"
                f"🛡️ Safety Score: "
                f"{itinerary['safety_score']}/100\n\n"
                f"Check the full itinerary below!"
            ),
            "plan_id": trip.id,
            "itinerary": itinerary,
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}",
        }), 500


@planner_bp.route(
    "/budget/optimize", methods=["POST"]
)
def optimize_budget():
    """Get budget optimization suggestions."""
    try:
        data = request.get_json()
        budget = float(data.get("budget", 5000))
        days = int(data.get("days", 3))
        travelers = int(data.get("travelers", 1))

        result = BudgetEngine.optimize_budget(
            budget, days, travelers
        )

        return jsonify({
            "success": True,
            "optimization": result,
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e),
        }), 500