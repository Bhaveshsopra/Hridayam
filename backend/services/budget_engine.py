"""Budget calculation and optimization engine."""


class BudgetEngine:
    """Smart budget allocation and tracking."""

    BUDGET_TIERS = {
        "backpacker": {
            "daily_min": 500,
            "daily_max": 1200,
            "accommodation": 0.25,
            "food": 0.30,
            "transport": 0.25,
            "activities": 0.15,
            "misc": 0.05,
        },
        "budget": {
            "daily_min": 1200,
            "daily_max": 2500,
            "accommodation": 0.30,
            "food": 0.25,
            "transport": 0.20,
            "activities": 0.20,
            "misc": 0.05,
        },
        "mid_range": {
            "daily_min": 2500,
            "daily_max": 6000,
            "accommodation": 0.35,
            "food": 0.25,
            "transport": 0.15,
            "activities": 0.18,
            "misc": 0.07,
        },
        "premium": {
            "daily_min": 6000,
            "daily_max": 15000,
            "accommodation": 0.40,
            "food": 0.20,
            "transport": 0.15,
            "activities": 0.15,
            "misc": 0.10,
        },
        "luxury": {
            "daily_min": 15000,
            "daily_max": 50000,
            "accommodation": 0.45,
            "food": 0.18,
            "transport": 0.12,
            "activities": 0.15,
            "misc": 0.10,
        },
    }

    @staticmethod
    def optimize_budget(total_budget, days, travelers=1):
        """
        Optimize budget allocation across categories.

        Returns detailed breakdown with recommendations.
        """
        per_person = total_budget / travelers
        daily_pp = per_person / days

        # Determine tier
        tier = "budget"
        for tier_name, tier_data in (
            BudgetEngine.BUDGET_TIERS.items()
        ):
            if (
                tier_data["daily_min"]
                <= daily_pp
                <= tier_data["daily_max"]
            ):
                tier = tier_name
                break
        else:
            if daily_pp > 15000:
                tier = "luxury"
            elif daily_pp < 500:
                tier = "backpacker"

        tier_config = BudgetEngine.BUDGET_TIERS[tier]

        breakdown = {
            "tier": tier,
            "total_budget": total_budget,
            "per_person": per_person,
            "daily_per_person": round(daily_pp),
            "allocation": {
                "accommodation": round(
                    per_person * tier_config["accommodation"]
                ),
                "food": round(
                    per_person * tier_config["food"]
                ),
                "transport": round(
                    per_person * tier_config["transport"]
                ),
                "activities": round(
                    per_person * tier_config["activities"]
                ),
                "miscellaneous": round(
                    per_person * tier_config["misc"]
                ),
            },
            "daily_allocation": {
                "accommodation": round(
                    daily_pp * tier_config["accommodation"]
                ),
                "food": round(
                    daily_pp * tier_config["food"]
                ),
                "transport": round(
                    daily_pp * tier_config["transport"]
                ),
                "activities": round(
                    daily_pp * tier_config["activities"]
                ),
                "miscellaneous": round(
                    daily_pp * tier_config["misc"]
                ),
            },
            "saving_tips": BudgetEngine._get_saving_tips(
                tier
            ),
        }

        return breakdown

    @staticmethod
    def _get_saving_tips(tier):
        """Get budget-specific saving tips."""
        tips = {
            "backpacker": [
                "Stay in dormitories or ashrams",
                "Eat at local dhabas and street stalls",
                "Use public buses (MP State Transport)",
                "Visit free temples and ghats",
                "Carry dry snacks for long journeys",
            ],
            "budget": [
                "Book trains in Sleeper class early",
                "Use MP Tourism budget hotels",
                "Eat at local restaurants, avoid tourist traps",
                "Buy combo tickets at monuments",
                "Travel by shared auto-rickshaws",
            ],
            "mid_range": [
                "Book AC 3-tier trains for comfort",
                "Mix budget and mid-range hotels",
                "Try both street food and restaurants",
                "Pre-book safari slots online",
                "Use Ola/Uber in cities",
            ],
            "premium": [
                "Book heritage hotels for unique experiences",
                "Hire private guides at major sites",
                "Try fine dining at heritage properties",
                "Consider domestic flights for long distances",
                "Book premium safari zones",
            ],
            "luxury": [
                "Stay at Taj, Jehan Numa or heritage palaces",
                "Hire private car with driver for entire trip",
                "Book exclusive tiger safari experiences",
                "Arrange private temple darshans where possible",
                "Consider helicopter tours over forts",
            ],
        }
        return tips.get(tier, tips["budget"])