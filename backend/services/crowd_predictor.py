"""
Crowd prediction using historical patterns
and time-series analysis.
"""

import random
from datetime import datetime


class CrowdPredictor:
    """Predict crowd levels at tourist sites."""

    # Historical crowd patterns (simplified)
    SEASONAL_FACTORS = {
        1: 0.8,   # January
        2: 0.7,   # February
        3: 0.6,   # March
        4: 0.4,   # April
        5: 0.3,   # May (too hot)
        6: 0.3,   # June
        7: 0.5,   # July (monsoon visitors)
        8: 0.5,   # August
        9: 0.6,   # September
        10: 0.9,  # October (season starts)
        11: 1.0,  # November (peak)
        12: 1.0,  # December (peak)
    }

    DAY_FACTORS = {
        0: 0.6,  # Monday
        1: 0.5,  # Tuesday
        2: 0.5,  # Wednesday
        3: 0.6,  # Thursday
        4: 0.8,  # Friday
        5: 1.0,  # Saturday
        6: 1.0,  # Sunday
    }

    TIME_FACTORS = {
        "early_morning": 0.3,   # 6-8 AM
        "morning": 0.6,         # 8-11 AM
        "midday": 0.8,          # 11 AM-2 PM
        "afternoon": 0.9,       # 2-5 PM
        "evening": 0.7,         # 5-7 PM
        "night": 0.2,           # After 7 PM
    }

    @staticmethod
    def predict(place_id, target_date=None, time_of_day="morning"):
        """
        Predict crowd level for a place.

        Returns:
            dict with crowd level (1-10),
            recommendation, and best time
        """
        if target_date is None:
            target_date = datetime.now()

        month = target_date.month
        weekday = target_date.weekday()

        seasonal = CrowdPredictor.SEASONAL_FACTORS.get(
            month, 0.5
        )
        day = CrowdPredictor.DAY_FACTORS.get(weekday, 0.6)
        time = CrowdPredictor.TIME_FACTORS.get(
            time_of_day, 0.5
        )

        # Base crowd level (1-10)
        base_crowd = 5
        noise = random.uniform(-0.5, 0.5)

        crowd_level = min(
            10,
            max(
                1,
                round(
                    base_crowd * seasonal * day * time
                    + noise
                ),
            ),
        )

        # Generate recommendation
        if crowd_level <= 3:
            recommendation = (
                "Excellent time to visit! Very few crowds."
            )
            status = "low"
        elif crowd_level <= 5:
            recommendation = (
                "Moderate crowds. Comfortable visiting."
            )
            status = "moderate"
        elif crowd_level <= 7:
            recommendation = (
                "Busy. Consider visiting early morning."
            )
            status = "high"
        else:
            recommendation = (
                "Very crowded. We recommend off-peak hours."
            )
            status = "very_high"

        # Find best time
        best_times = []
        for time_slot, factor in (
            CrowdPredictor.TIME_FACTORS.items()
        ):
            if factor <= 0.4:
                best_times.append(time_slot)

        return {
            "place_id": place_id,
            "crowd_level": crowd_level,
            "max_level": 10,
            "status": status,
            "recommendation": recommendation,
            "best_times": best_times or ["early_morning"],
            "predicted_for": target_date.isoformat(),
            "time_of_day": time_of_day,
            "factors": {
                "seasonal_factor": seasonal,
                "day_factor": day,
                "time_factor": time,
            },
        }