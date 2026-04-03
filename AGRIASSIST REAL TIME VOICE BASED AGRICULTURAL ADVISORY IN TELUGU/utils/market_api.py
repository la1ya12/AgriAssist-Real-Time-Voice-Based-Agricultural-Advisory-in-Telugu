# utils/market_api.py

import random

# 🌾 Fallback crop market prices (₹ / quintal)
CROP_PRICES = {
    "మిర్చి": {"min": 12000, "max": 18000, "unit": "క్వింటాల్"},
    "పత్తి": {"min": 5500, "max": 7500, "unit": "క్వింటాల్"},
    "వరి": {"min": 2200, "max": 2800, "unit": "క్వింటాల్"},
    "మొక్కజొన్న": {"min": 1800, "max": 2300, "unit": "క్వింటాల్"},
    "పల్లీలు": {"min": 5000, "max": 6500, "unit": "క్వింటాల్"},
}


def fetch_market_price_from_api(crop):
    """
    🔌 Placeholder for external market price API
    (e.g., data.gov.in / mandi price API)

    Returns:
    - None → API unavailable (demo case)
    - dict → if real API is integrated in future
    """

    # --- API NOT CONNECTED (INTENTIONAL) ---
    # This simulates API failure or downtime
    return None


def get_market_price(crop=None):
    """
    Hybrid market price retrieval:
    1. Try external API
    2. Fallback to internal dataset
    """

    if not crop:
        return (
            "దయచేసి పంట పేరు చెప్పండి.\n"
            "ఉదాహరణకు: మిర్చి ధర, వరి ధర."
        )

    # 1️⃣ Try API
    api_data = fetch_market_price_from_api(crop)
    if api_data:
        return (
            f"{crop} పంట మార్కెట్ ధర ప్రస్తుతం "
            f"₹{api_data['price']} ప్రతి క్వింటాల్."
        )

    # 2️⃣ Fallback dataset
    if crop not in CROP_PRICES:
        return f"{crop} పంటకు ధర సమాచారం ప్రస్తుతం అందుబాటులో లేదు."

    data = CROP_PRICES[crop]
    min_price = data["min"]
    max_price = data["max"]

    return (
        f"{crop} పంట మార్కెట్ ధర సుమారు "
        f"₹{min_price} నుండి ₹{max_price} వరకు "
        f"ప్రతి {data['unit']}కి ఉంటుంది."
    )
