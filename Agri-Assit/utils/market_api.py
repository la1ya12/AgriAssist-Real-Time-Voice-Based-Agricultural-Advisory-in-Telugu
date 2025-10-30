# utils/market_api.py
import requests

# ✅ Replace with your real API key from data.gov.in
API_KEY = "YOUR_API_KEY"
DATA_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

# ✅ Fallback static dataset (in ₹/క్వింటాల్)
FALLBACK_PRICES = {
    "మిర్చి": {"avg": 12000, "min": 10000, "max": 14000},
    "బియ్యం": {"avg": 2500, "min": 2200, "max": 2800},
    "పత్తి": {"avg": 6400, "min": 6000, "max": 6800},
    "మొక్కజొన్న": {"avg": 2200, "min": 2000, "max": 2400},
    "వరి": {"avg": 2300, "min": 2100, "max": 2500},
    "జొన్న": {"avg": 2100, "min": 1900, "max": 2300},
    "గ్రౌండ్‌నట్": {"avg": 6000, "min": 5500, "max": 6500},
}

# ✅ Telugu → English crop mapping
CROP_MAP = {
     "మిర్చి": "Chillies",
    "బియ్యం": "Paddy",
    "పత్తి": "Cotton",
    "మొక్కజొన్న": "Maize",
    "జొన్న": "Jowar",
    "వరి": "Rice",
    "గ్రౌండ్‌నట్": "Groundnut",
}

def get_market_price(crop="మిర్చి", district=None):
    """
    Hybrid crop price retriever:
    - Uses Agmarknet API for real-time prices
    - Falls back to local static prices if API fails
    - Responds politely if crop not available
    """
    # ✅ If crop is not recognized, respond politely
    if crop not in CROP_MAP and crop not in FALLBACK_PRICES:
        return f"{crop} ధర సమాచారం ప్రస్తుతం అందుబాటులో లేదు రైతు గారు."

    eng_crop = CROP_MAP.get(crop, None)

    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 5,
        "filters[state]": "Telangana"
    }

    if eng_crop:
        params["filters[commodity]"] = eng_crop
    if district:
        params["filters[district]"] = district

    try:
        res = requests.get(DATA_URL, params=params, timeout=10)
        data = res.json()

        if data.get("records"):
            record = data["records"][0]
            market = record.get("market", "మార్కెట్")
            modal_price = record.get("modal_price", "తెలియదు")
            min_price = record.get("min_price", "తెలియదు")
            max_price = record.get("max_price", "తెలియదు")

            return (f"{district or ''} లో {market} మార్కెట్‌లో {crop} ధరలు — "
                    f"సగటు ₹{modal_price}, కనిష్టం ₹{min_price}, గరిష్టం ₹{max_price} క్వింటాల్‌కి.")
        else:
            # No record → fallback
            return fallback_price(crop, district)

    except Exception:
        # API failure → fallback
        return fallback_price(crop, district)

def fallback_price(crop, district=None):
    """Static fallback price info"""
    if crop not in FALLBACK_PRICES:
        return f"{crop} ధర సమాచారం ప్రస్తుతం అందుబాటులో లేదు రైతు గారు."

    p = FALLBACK_PRICES[crop]
    location_text = f"{district} లో " if district else ""
    return (f"{location_text}{crop} మార్కెట్ ధర ప్రస్తుతం సగటుగా ₹{p['avg']} క్వింటాల్‌కి ఉంది "
            f"(కనిష్టం ₹{p['min']} – గరిష్టం ₹{p['max']}).")
