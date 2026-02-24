"""
AI Chatbot engine for tourism queries.
Supports English and Hindi with rule-based +
optional LLM integration.
"""

import json
import os
import random
from datetime import datetime


class ChatbotEngine:
    """Multilingual tourism chatbot."""

    def __init__(self):
        self.places = self._load_places()
        self.context = {}

    def _load_places(self):
        data_path = os.path.join(
            os.path.dirname(__file__),
            "..", "data", "places.json",
        )
        try:
            with open(data_path, "r") as f:
                data = json.load(f)
            return data.get("places", [])
        except FileNotFoundError:
            return []

    def get_response(
        self, message, language="en", session_id=None
    ):
        """
        Process user message and return bot response.

        Args:
            message: User's text message
            language: Language code (en/hi)
            session_id: Session tracking ID

        Returns:
            dict with response text and metadata
        """
        msg = message.lower().strip()

        # Greeting detection
        if any(
            g in msg
            for g in [
                "hello", "hi", "hey", "namaste",
                "namaskar", "hola",
            ]
        ):
            return self._greeting_response(language)

        # Place queries
        for place in self.places:
            if place["id"] in msg or (
                place["name"].lower() in msg
            ):
                return self._place_info_response(
                    place, language
                )

        # Topic-based responses
        if any(
            w in msg
            for w in [
                "budget", "cost", "price", "kitna",
                "paisa", "kharcha", "expensive", "cheap",
            ]
        ):
            return self._budget_response(language)

        if any(
            w in msg
            for w in [
                "safe", "safety", "danger",
                "emergency", "sos", "suraksha",
            ]
        ):
            return self._safety_response(language)

        if any(
            w in msg
            for w in [
                "weather", "mausam", "rain",
                "hot", "cold", "temperature",
            ]
        ):
            return self._weather_response(language)

        if any(
            w in msg
            for w in [
                "food", "eat", "restaurant", "khana",
                "biryani", "poha", "dining",
            ]
        ):
            return self._food_response(language)

        if any(
            w in msg
            for w in [
                "hotel", "stay", "accommodation",
                "lodge", "resort", "room",
            ]
        ):
            return self._accommodation_response(language)

        if any(
            w in msg
            for w in [
                "transport", "bus", "train", "flight",
                "taxi", "auto", "travel", "how to reach",
            ]
        ):
            return self._transport_response(language)

        if any(
            w in msg
            for w in [
                "tiger", "wildlife", "safari",
                "national park", "jungle",
            ]
        ):
            return self._wildlife_response(language)

        if any(
            w in msg
            for w in [
                "temple", "mandir", "spiritual",
                "jyotirlinga", "pooja",
            ]
        ):
            return self._spiritual_response(language)

        if any(
            w in msg
            for w in [
                "best time", "when to visit",
                "kab jaaye", "season",
            ]
        ):
            return self._best_time_response(language)

        if any(
            w in msg
            for w in ["plan", "itinerary", "trip", "tour"]
        ):
            return self._plan_response(language)

        if any(
            w in msg
            for w in ["thank", "thanks", "dhanyavaad", "shukriya"]
        ):
            return self._thanks_response(language)

        if any(
            w in msg
            for w in ["bye", "goodbye", "alvida", "exit"]
        ):
            return self._goodbye_response(language)

        # Default response
        return self._default_response(msg, language)

    def _greeting_response(self, lang):
        responses_en = [
            "🙏 Namaste! Welcome to AI Smart Tourism MP! "
            "I can help you plan trips, find places, check "
            "weather, food recommendations, and more. "
            "What would you like to know?",
            "Hello! 🌟 I'm your AI travel assistant for "
            "Madhya Pradesh. Ask me about places, budget, "
            "safety, food, or let me plan your perfect trip!",
        ]
        responses_hi = [
            "🙏 नमस्ते! AI Smart Tourism MP में आपका स्वागत है! "
            "मैं आपकी यात्रा की योजना बनाने, स्थान खोजने, "
            "मौसम जांचने में मदद कर सकता हूं। "
            "आप क्या जानना चाहेंगे?",
        ]
        responses = (
            responses_hi if lang == "hi" else responses_en
        )
        return {
            "response": random.choice(responses),
            "type": "greeting",
            "suggestions": [
                "Popular places in MP",
                "Plan a 3-day trip",
                "Budget for MP trip",
                "Safety information",
            ],
        }

    def _place_info_response(self, place, lang):
        highlights = ", ".join(
            place.get("highlights", [])[:3]
        )
        resp = (
            f"🏛️ **{place['name']}** — {place['city']}\n\n"
            f"{place['description']}\n\n"
            f"⭐ Rating: {place.get('rating', 'N/A')}/5\n"
            f"💰 Entry: ₹{place.get('entry_fee', 0)} "
            f"(Foreign: ₹{place.get('foreign_fee', 0)})\n"
            f"⏰ Visit Duration: "
            f"{place.get('visit_duration_hours', 3)} hours\n"
            f"🌟 Must See: {highlights}\n"
            f"📅 Best Time: {place.get('best_time', 'Oct-Mar')}\n"
            f"🛡️ Safety Score: "
            f"{place.get('safety_score', 85)}/100"
        )
        return {
            "response": resp,
            "type": "place_info",
            "place": place,
            "suggestions": [
                f"Food near {place['city']}",
                f"Weather in {place['city']}",
                f"Hotels in {place['city']}",
                "Plan trip including this place",
            ],
        }

    def _budget_response(self, lang):
        resp = (
            "💰 **MP Trip Budget Guide:**\n\n"
            "🎒 **Backpacker:** ₹500-1,200/day\n"
            "   • Dormitories, street food, buses\n\n"
            "💼 **Budget:** ₹1,200-2,500/day\n"
            "   • Budget hotels, local restaurants, trains\n\n"
            "🏨 **Mid-Range:** ₹2,500-6,000/day\n"
            "   • 3-star hotels, mix of dining, AC trains\n\n"
            "⭐ **Premium:** ₹6,000-15,000/day\n"
            "   • Heritage hotels, fine dining, private car\n\n"
            "👑 **Luxury:** ₹15,000+/day\n"
            "   • Palace hotels, exclusive safaris, flights\n\n"
            "💡 Tip: A comfortable 3-day MP trip costs "
            "approximately ₹5,000-8,000 per person!"
        )
        return {
            "response": resp,
            "type": "budget",
            "suggestions": [
                "Plan budget trip",
                "Cheapest places to visit",
                "Luxury hotels in MP",
                "Food costs in Bhopal",
            ],
        }

    def _safety_response(self, lang):
        resp = (
            "🛡️ **Safety in Madhya Pradesh:**\n\n"
            "MP is generally very safe for tourists. "
            "Our AI monitors safety 24/7.\n\n"
            "📞 **Emergency Numbers:**\n"
            "• Police: 100\n"
            "• Ambulance: 108\n"
            "• Women Helpline: 1091\n"
            "• Tourist Helpline: 1800-233-7777\n\n"
            "✅ **Safety Tips:**\n"
            "• Use registered guides and taxis\n"
            "• Keep copies of ID documents\n"
            "• Stay on marked trails in forests\n"
            "• Share your GPS location with family\n"
            "• Use our SOS button for emergencies"
        )
        return {
            "response": resp,
            "type": "safety",
            "suggestions": [
                "Women safety features",
                "SOS emergency",
                "Safe areas in MP",
                "Travel insurance",
            ],
        }

    def _weather_response(self, lang):
        month = datetime.now().month
        if month in [11, 12, 1, 2]:
            season = "Winter (Best Season!)"
            temp = "8°C - 25°C"
            tip = "Perfect weather for sightseeing!"
        elif month in [3, 4, 5, 6]:
            season = "Summer"
            temp = "28°C - 45°C"
            tip = "Very hot. Visit hill stations like Pachmarhi."
        else:
            season = "Monsoon"
            temp = "22°C - 35°C"
            tip = "Rainy. Beautiful waterfalls but some parks closed."

        resp = (
            f"⛅ **Current Weather Season in MP:**\n\n"
            f"Season: {season}\n"
            f"Temperature: {temp}\n"
            f"💡 {tip}\n\n"
            f"**Best months to visit MP:** "
            f"October to March\n"
            f"**Monsoon beauty:** July-September "
            f"(Pachmarhi waterfalls are stunning!)"
        )
        return {
            "response": resp,
            "type": "weather",
            "suggestions": [
                "Best time for Khajuraho",
                "Pachmarhi in monsoon",
                "Winter destinations in MP",
            ],
        }

    def _food_response(self, lang):
        resp = (
            "🍜 **Must-Try MP Food:**\n\n"
            "🔸 **Bhopal:** Biryani, Poha-Jalebi, "
            "Mawa Bati, Rogan Josh\n"
            "🔸 **Indore:** Poha, Garadu, Bhutte Ka Kees, "
            "Sarafa Night Market\n"
            "🔸 **Ujjain:** Dal Bafla, Malpua, "
            "Temple Prasad\n"
            "🔸 **Gwalior:** Bedai-Sabzi, Gajak sweets\n\n"
            "⭐ **Top Food Streets:**\n"
            "• Chatori Gali, Bhopal\n"
            "• Sarafa Bazaar, Indore (opens at 10 PM!)\n"
            "• Chappan Dukan, Indore\n\n"
            "💡 Indore is the food capital of MP — "
            "don't miss it!"
        )
        return {
            "response": resp,
            "type": "food",
            "suggestions": [
                "Vegetarian food in MP",
                "Street food safety",
                "Best restaurants in Bhopal",
                "Indore food tour",
            ],
        }

    def _accommodation_response(self, lang):
        resp = (
            "🏨 **Where to Stay in MP:**\n\n"
            "**Budget (₹400-1,000/night):**\n"
            "• MP Tourism guest houses\n"
            "• OYO & FabHotels\n"
            "• Dharamshalas near temples\n\n"
            "**Mid-Range (₹1,000-3,000/night):**\n"
            "• 3-star hotels in city centers\n"
            "• MP Tourism premium properties\n\n"
            "**Luxury (₹5,000+/night):**\n"
            "• Jehan Numa Palace, Bhopal\n"
            "• Noor-Us-Sabah Palace, Bhopal\n"
            "• Taj Usha Kiran, Gwalior\n"
            "• Wildlife lodges near national parks\n\n"
            "💡 Book MP Tourism hotels at mptourism.com"
        )
        return {
            "response": resp,
            "type": "accommodation",
            "suggestions": [
                "Heritage hotels in MP",
                "Budget stays near Khajuraho",
                "Safari lodges",
            ],
        }

    def _transport_response(self, lang):
        resp = (
            "🚂 **Getting Around MP:**\n\n"
            "✈️ **Flights:** Bhopal, Indore, Jabalpur, "
            "Gwalior, Khajuraho airports\n\n"
            "🚂 **Trains:** Well-connected via Indian "
            "Railways. Book on IRCTC.\n"
            "• Shatabdi Express (fast intercity)\n"
            "• Sleeper class (budget-friendly)\n\n"
            "🚌 **Buses:** MP State Transport (MSRTC)\n"
            "• AC Volvo between major cities\n\n"
            "🚗 **Taxis:** ~₹12/km for AC sedan\n"
            "🛺 **Auto:** ~₹8/km in cities\n\n"
            "💡 For wildlife parks, book jeep safaris "
            "in advance online!"
        )
        return {
            "response": resp,
            "type": "transport",
            "suggestions": [
                "Bhopal to Khajuraho",
                "Train schedule",
                "Airport transfers",
            ],
        }

    def _wildlife_response(self, lang):
        resp = (
            "🐯 **Wildlife in MP:**\n\n"
            "MP is the 'Tiger State' of India!\n\n"
            "🌿 **Top National Parks:**\n"
            "• Bandhavgarh — Highest tiger density\n"
            "• Kanha — Jungle Book inspiration\n"
            "• Pench — Beautiful teak forests\n"
            "• Satpura — Walking safaris available\n"
            "• Panna — Tiger reintroduction success\n\n"
            "💰 **Safari Cost:** ₹1,500-4,500/person\n"
            "⏰ **Timings:** 6 AM & 3 PM (two slots)\n"
            "📅 **Season:** October to June\n"
            "🚫 **Closed:** July to September\n\n"
            "💡 Book safaris at mpforest.gov.in — "
            "slots fill up fast!"
        )
        return {
            "response": resp,
            "type": "wildlife",
            "suggestions": [
                "Tiger safari booking",
                "Best park for tigers",
                "Bird watching in MP",
            ],
        }

    def _spiritual_response(self, lang):
        resp = (
            "🙏 **Spiritual Destinations in MP:**\n\n"
            "MP has 2 of India's 12 Jyotirlingas!\n\n"
            "⭐ **Must Visit:**\n"
            "• Mahakaleshwar, Ujjain (Jyotirlinga)\n"
            "• Omkareshwar (Jyotirlinga)\n"
            "• Sanchi Stupa (Buddhist heritage)\n"
            "• Chitrakoot (Ram's exile place)\n"
            "• Orchha — Ram Raja Temple\n"
            "• Amarkantak — Narmada origin\n\n"
            "🕉️ **Special Experience:**\n"
            "Bhasma Aarti at Mahakaleshwar — 4 AM daily\n"
            "Book online at shrimahakaleshwar.com\n\n"
            "💡 Dress modestly for temple visits!"
        )
        return {
            "response": resp,
            "type": "spiritual",
            "suggestions": [
                "Bhasma Aarti booking",
                "Buddhist sites in MP",
                "Narmada Parikrama",
            ],
        }

    def _best_time_response(self, lang):
        resp = (
            "📅 **Best Time to Visit MP:**\n\n"
            "🏆 **BEST: October to March**\n"
            "Pleasant weather (10-25°C), all sites open, "
            "festival season\n\n"
            "☀️ **April to June:**\n"
            "Hot (35-45°C) but fewer crowds. "
            "Good for Pachmarhi hill station.\n\n"
            "🌧️ **July to September:**\n"
            "Monsoon — lush green landscapes, "
            "stunning waterfalls. Some wildlife parks closed.\n\n"
            "🎉 **Festival Season:**\n"
            "• Khajuraho Dance Festival (Feb)\n"
            "• Tansen Music Festival, Gwalior (Dec)\n"
            "• Lokrang Festival, Bhopal (Jan)\n"
            "• Simhasth Kumbh, Ujjain (every 12 years)"
        )
        return {
            "response": resp,
            "type": "best_time",
            "suggestions": [
                "Festivals in MP",
                "Monsoon trip plan",
                "Winter itinerary",
            ],
        }

    def _plan_response(self, lang):
        resp = (
            "🗺️ **Let me help plan your MP trip!**\n\n"
            "I need a few details:\n\n"
            "1️⃣ How many days do you have?\n"
            "2️⃣ What's your budget per person?\n"
            "3️⃣ Your interests? (Heritage / Wildlife / "
            "Spiritual / Adventure / Food)\n\n"
            "Or use our **AI Trip Planner** for an "
            "instant detailed itinerary!\n\n"
            "💡 Popular plans:\n"
            "• 3-day Heritage Trail (₹6,000/person)\n"
            "• 5-day Complete MP (₹12,000/person)\n"
            "• 2-day Wildlife Safari (₹8,000/person)\n"
            "• 4-day Spiritual Journey (₹5,000/person)"
        )
        return {
            "response": resp,
            "type": "planning",
            "suggestions": [
                "3-day heritage trip",
                "Budget trip plan",
                "Wildlife safari plan",
                "Spiritual tour plan",
            ],
        }

    def _thanks_response(self, lang):
        responses = [
            "You're welcome! 🙏 Enjoy your "
            "Madhya Pradesh journey! Jai Hind! 🇮🇳",
            "Happy to help! 🌟 Have an amazing "
            "trip to the Heart of India!",
            "Glad I could assist! 😊 "
            "MP awaits you with open arms!",
        ]
        return {
            "response": random.choice(responses),
            "type": "thanks",
            "suggestions": [
                "Plan another trip",
                "Emergency numbers",
                "Share feedback",
            ],
        }

    def _goodbye_response(self, lang):
        return {
            "response": (
                "👋 Goodbye! Wish you a wonderful journey "
                "through Madhya Pradesh! 🙏\n\n"
                "Remember: I'm available 24/7 whenever "
                "you need travel assistance. Stay safe! 🛡️"
            ),
            "type": "goodbye",
            "suggestions": [],
        }

    def _default_response(self, msg, lang):
        return {
            "response": (
                "🤔 I'm not sure about that, but I can "
                "help you with:\n\n"
                "• 🏛️ Tourist places in MP\n"
                "• 💰 Trip budget planning\n"
                "• 🛡️ Safety information\n"
                "• ⛅ Weather updates\n"
                "• 🍜 Food recommendations\n"
                "• 🏨 Hotel suggestions\n"
                "• 🚂 Transport options\n"
                "• 🐯 Wildlife safaris\n"
                "• 🙏 Spiritual destinations\n\n"
                "Try asking about any of these topics!"
            ),
            "type": "default",
            "suggestions": [
                "Popular places",
                "Plan a trip",
                "Food guide",
                "Safety info",
            ],
        }