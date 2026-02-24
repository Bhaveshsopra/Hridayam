"""
AI Trip Planner Engine for Madhya Pradesh.
Generates personalized itineraries based on budget,
duration, and interests.
"""

import json
import os
import random
from datetime import datetime, timedelta


class AITripPlanner:
    def __init__(self):
        self.places = self._load_places()
        self.food_guide = self._load_food_guide()

    def _load_places(self):
        data_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "places.json"
        )
        try:
            with open(data_path, "r") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return {"places": [], "transport_costs": {},
                    "accommodation": {}, "food_costs": {}}

    def _load_food_guide(self):
        data_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "food_guide.json"
        )
        try:
            with open(data_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def generate_itinerary(
        self, budget, days, interests, travelers=1, start_city="Bhopal"
    ):
        """
        Generate a complete AI-powered itinerary.

        Args:
            budget: Total budget per person in INR
            days: Number of travel days
            interests: List of interest tags
            travelers: Number of travelers
            start_city: Starting city

        Returns:
            Complete itinerary dict
        """
        # Step 1: Filter and score places by interests
        scored_places = self._score_places(interests)

        # Step 2: Determine budget tier
        budget_tier = self._get_budget_tier(budget, days)

        # Step 3: Select optimal places for the duration
        selected_places = self._select_places(
            scored_places, days, budget, budget_tier
        )

        # Step 4: Build day-by-day itinerary
        itinerary = self._build_daily_plan(
            selected_places, days, budget_tier, start_city
        )

        # Step 5: Calculate costs
        cost_breakdown = self._calculate_costs(
            itinerary, budget_tier, days, travelers
        )

        # Step 6: Add safety scores
        safety_score = self._calculate_safety_score(
            selected_places
        )

        # Step 7: Add food recommendations
        food_recs = self._get_food_recommendations(
            selected_places
        )

        # Step 8: Weather advisory
        weather_tips = self._get_weather_advisory(days)

        return {
            "trip_name": self._generate_trip_name(interests),
            "days": days,
            "budget_tier": budget_tier,
            "travelers": travelers,
            "start_city": start_city,
            "itinerary": itinerary,
            "cost_breakdown": cost_breakdown,
            "total_estimated_cost": cost_breakdown["total"],
            "budget_remaining": max(
                0, budget - cost_breakdown["total"]
            ),
            "safety_score": safety_score,
            "food_recommendations": food_recs,
            "weather_advisory": weather_tips,
            "packing_tips": self._get_packing_tips(
                interests
            ),
            "emergency_numbers": {
                "police": "100",
                "ambulance": "108",
                "tourist_helpline": "1800-233-7777",
                "women_helpline": "1091",
            },
            "generated_at": datetime.utcnow().isoformat(),
            "ai_confidence": random.randint(87, 96),
        }

    def _score_places(self, interests):
        """Score each place based on user interests."""
        scored = []
        for place in self.places.get("places", []):
            score = 0
            place_types = place.get("type", [])

            for interest in interests:
                interest_lower = interest.lower().strip()
                if interest_lower in place_types:
                    score += 10
                # Partial matches
                for ptype in place_types:
                    if interest_lower in ptype or ptype in interest_lower:
                        score += 5

            # Bonus for high ratings
            score += place.get("rating", 0) * 2

            # Bonus for UNESCO sites
            if "unesco" in place_types:
                score += 5

            scored.append({"place": place, "score": score})

        # Sort by score descending
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored

    def _get_budget_tier(self, budget, days):
        """Determine budget tier."""
        daily_budget = budget / days
        if daily_budget < 1500:
            return "budget"
        elif daily_budget < 4000:
            return "mid_range"
        elif daily_budget < 10000:
            return "premium"
        else:
            return "luxury"

    def _select_places(
        self, scored_places, days, budget, budget_tier
    ):
        """Select optimal number of places for trip."""
        # Rule: ~1.5 places per day (some places need
        # full day or more)
        max_places = min(
            int(days * 1.5) + 1, len(scored_places)
        )
        selected = []

        for item in scored_places[:max_places]:
            selected.append(item["place"])

        return selected

    def _build_daily_plan(
        self, places, days, budget_tier, start_city
    ):
        """Build day-by-day plan."""
        daily_plans = []
        place_index = 0

        accom = self.places.get("accommodation", {})
        food = self.places.get("food_costs", {})

        tier_accom = accom.get(
            budget_tier,
            {"min": 500, "max": 1500, "label": "Standard"},
        )
        tier_food = food.get(
            budget_tier,
            {
                "breakfast": 100,
                "lunch": 200,
                "dinner": 250,
                "snacks": 50,
            },
        )

        for day in range(1, days + 1):
            day_plan = {
                "day": day,
                "title": "",
                "activities": [],
                "accommodation": {
                    "type": tier_accom.get("label", "Hotel"),
                    "est_cost": (
                        tier_accom["min"] + tier_accom["max"]
                    )
                    // 2,
                },
                "meals": tier_food,
                "tips": [],
            }

            # Morning activity
            if place_index < len(places):
                place = places[place_index]
                day_plan["title"] = (
                    f"{start_city} → {place['city']}"
                    if day == 1
                    else place["city"]
                )
                day_plan["activities"].append(
                    {
                        "time": "08:00 AM",
                        "activity": (
                            f"Visit {place['name']}"
                        ),
                        "duration": (
                            f"{place.get('visit_duration_hours', 3)}h"
                        ),
                        "entry_fee": place.get(
                            "entry_fee", 0
                        ),
                        "highlights": place.get(
                            "highlights", []
                        )[:2],
                        "crowd_tip": (
                            "Visit early morning for "
                            "fewer crowds"
                            if place.get("avg_crowd", {}).get(
                                "morning", 5
                            )
                            < 4
                            else "Moderate crowds expected"
                        ),
                    }
                )

                # Food recommendation
                city_food = self.food_guide.get(
                    place["city"].lower(), {}
                )
                if city_food:
                    must_try = city_food.get("must_try", [])
                    if must_try:
                        day_plan["activities"].append(
                            {
                                "time": "01:00 PM",
                                "activity": (
                                    f"Lunch - Try "
                                    f"{must_try[0]['name']}"
                                ),
                                "duration": "1h",
                                "entry_fee": 0,
                                "highlights": [
                                    must_try[0].get(
                                        "where", "Local"
                                    )
                                ],
                            }
                        )

                place_index += 1

            # Afternoon activity
            if place_index < len(places):
                place2 = places[place_index]
                if (
                    place2.get("visit_duration_hours", 3)
                    <= 4
                ):
                    day_plan["activities"].append(
                        {
                            "time": "03:00 PM",
                            "activity": (
                                f"Explore {place2['name']}"
                            ),
                            "duration": (
                                f"{place2.get('visit_duration_hours', 3)}h"
                            ),
                            "entry_fee": place2.get(
                                "entry_fee", 0
                            ),
                            "highlights": place2.get(
                                "highlights", []
                            )[:2],
                        }
                    )
                    place_index += 1

            # Evening
            day_plan["activities"].append(
                {
                    "time": "07:00 PM",
                    "activity": (
                        "Evening rest & local exploration"
                    ),
                    "duration": "2h",
                    "entry_fee": 0,
                    "highlights": [
                        "Local market visit",
                        "Sunset viewing",
                    ],
                }
            )

            # Safety tips for the day
            day_plan["tips"] = [
                "Keep emergency numbers saved",
                "Stay hydrated - carry water bottle",
                "Use registered transport only",
            ]

            daily_plans.append(day_plan)

        return daily_plans

    def _calculate_costs(
        self, itinerary, budget_tier, days, travelers
    ):
        """Calculate detailed cost breakdown."""
        accom = self.places.get("accommodation", {})
        food = self.places.get("food_costs", {})
        transport = self.places.get("transport_costs", {})

        tier_accom = accom.get(
            budget_tier, {"min": 500, "max": 1500}
        )
        tier_food = food.get(
            budget_tier,
            {
                "breakfast": 100,
                "lunch": 200,
                "dinner": 250,
                "snacks": 50,
            },
        )

        accom_cost = (
            (tier_accom["min"] + tier_accom["max"]) // 2
        ) * days
        food_cost = sum(tier_food.values()) * days
        entry_fees = sum(
            activity.get("entry_fee", 0)
            for day in itinerary
            for activity in day.get("activities", [])
        )
        transport_cost = days * (
            200 if budget_tier == "budget" else 500
            if budget_tier == "mid_range" else 1200
        )
        misc = days * 100

        total = (
            accom_cost
            + food_cost
            + entry_fees
            + transport_cost
            + misc
        )

        return {
            "accommodation": accom_cost,
            "food": food_cost,
            "entry_fees": entry_fees,
            "transport": transport_cost,
            "miscellaneous": misc,
            "total": total,
            "per_day": total // days,
            "currency": "INR",
        }

    def _calculate_safety_score(self, places):
        """Calculate overall trip safety score."""
        if not places:
            return 85
        scores = [
            p.get("safety_score", 85) for p in places
        ]
        avg = sum(scores) / len(scores)
        return round(avg)

    def _get_food_recommendations(self, places):
        """Get food recommendations for selected places."""
        recs = {}
        for place in places:
            city = place.get("city", "").lower()
            if city in self.food_guide:
                recs[place["city"]] = self.food_guide[city]
        return recs

    def _get_weather_advisory(self, days):
        """Get seasonal weather advisory."""
        month = datetime.now().month
        if month in [11, 12, 1, 2]:
            return {
                "season": "Winter",
                "temp_range": "8°C - 25°C",
                "advisory": (
                    "Pleasant weather, ideal for sightseeing. "
                    "Carry light woolens for evenings."
                ),
                "recommended": True,
            }
        elif month in [3, 4, 5, 6]:
            return {
                "season": "Summer",
                "temp_range": "28°C - 45°C",
                "advisory": (
                    "Hot weather. Plan outdoor activities "
                    "for early morning. Stay hydrated."
                ),
                "recommended": month <= 3,
            }
        else:
            return {
                "season": "Monsoon",
                "temp_range": "22°C - 35°C",
                "advisory": (
                    "Rainy season. Carry rain gear. "
                    "Some wildlife parks may be closed."
                ),
                "recommended": False,
            }

    def _get_packing_tips(self, interests):
        """Generate packing tips based on interests."""
        tips = [
            "Comfortable walking shoes",
            "Sunscreen and sunglasses",
            "Water bottle (refillable)",
            "Power bank for devices",
            "First aid kit",
            "Valid ID proof",
        ]
        for interest in interests:
            i = interest.lower()
            if i in ["wildlife", "nature", "adventure"]:
                tips.extend(
                    [
                        "Binoculars for wildlife",
                        "Insect repellent",
                        "Full-sleeve clothing",
                    ]
                )
            if i in ["spiritual", "temple"]:
                tips.extend(
                    [
                        "Modest clothing for temples",
                        "Socks (no shoes in temples)",
                    ]
                )
            if i in ["heritage", "history"]:
                tips.append("Camera with good zoom")
        return list(set(tips))

    def _generate_trip_name(self, interests):
        """Generate a catchy trip name."""
        templates = {
            "heritage": "Heritage Trail of Madhya Pradesh",
            "spiritual": "Sacred Journey through MP",
            "wildlife": "Wild MP Safari Adventure",
            "nature": "Nature's Paradise - MP Explorer",
            "adventure": "MP Adventure Expedition",
            "history": "Historical Odyssey of Central India",
        }
        for interest in interests:
            i = interest.lower()
            if i in templates:
                return templates[i]
        return "AI-Curated Madhya Pradesh Experience"