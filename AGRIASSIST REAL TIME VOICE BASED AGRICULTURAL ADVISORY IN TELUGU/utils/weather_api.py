import requests

# 🔑 OpenWeatherMap API Key
API_KEY = "322a0dc336116712f655acf15f1277b1"

# 🌍 Telugu → English district mapping (ALL Telangana + Andhra Pradesh)
TELUGU_TO_ENGLISH = {

    # ================= TELANGANA =================
    "హైదరాబాద్": "Hyderabad",
    "మెదక్": "Medak",
    "మేడ్చల్": "Medchal",
    "మేడ్చల్ మల్కాజ్‌గిరి": "Medchal",
    "వరంగల్": "Warangal",
    "హనుమకొండ": "Warangal",
    "నిజామాబాద్": "Nizamabad",
    "కరీంనగర్": "Karimnagar",
    "పెద్దపల్లి": "Peddapalli",
    "జగిత్యాల": "Jagtial",
    "రాజన్న సిరిసిల్ల": "Rajanna Sircilla",
    "సిద్దిపేట": "Siddipet",
    "సంగారెడ్డి": "Sangareddy",
    "వికారాబాద్": "Vikarabad",
    "మహబూబ్‌నగర్": "Mahbubnagar",
    "నాగర్‌కర్నూల్": "Nagarkurnool",
    "వనపర్తి": "Wanaparthy",
    "జోగులాంబ గద్వాల్": "Jogulamba Gadwal",
    "నారాయణపేట": "Narayanpet",
    "ఖమ్మం": "Khammam",
    "భద్రాద్రి కొత్తగూడెం": "Bhadradri Kothagudem",
    "సూర్యాపేట": "Suryapet",
    "నల్గొండ": "Nalgonda",
    "యాదాద్రి భువనగిరి": "Yadadri Bhuvanagiri",
    "మహబూబాబాద్": "Mahabubabad",
    "జనగాం": "Jangaon",
    "ములుగు": "Mulugu",
    "ఆదిలాబాద్": "Adilabad",
    "నిర్మల్": "Nirmal",
    "మంచిర్యాల": "Mancherial",
    "కుమురం భీమ్ ఆసిఫాబాద్": "Asifabad",

    # ================= ANDHRA PRADESH =================
    "విశాఖపట్నం": "Visakhapatnam",
    "అల్లూరి సీతారామ రాజు": "Visakhapatnam",
    "అనకాపల్లి": "Anakapalle",
    "శ్రీకాకుళం": "Srikakulam",
    "విజయనగరం": "Vizianagaram",
    "పార్వతీపురం మన్యం": "Vizianagaram",
    "కాకినాడ": "Kakinada",
    "కోనసీమ": "Konaseema",
    "తూర్పు గోదావరి": "Rajahmundry",
    "పడమటి గోదావరి": "Eluru",
    "ఏలూరు": "Eluru",
    "కృష్ణా": "Machilipatnam",
    "ఎన్టీఆర్": "Vijayawada",
    "గుంటూరు": "Guntur",
    "బాపట్ల": "Bapatla",
    "పల్నాడు": "Narasaraopet",
    "ప్రకాశం": "Ongole",
    "నెల్లూరు": "Nellore",
    "కడప": "Kadapa",
    "అన్నమయ్య": "Kadapa",
    "అనంతపురం": "Anantapur",
    "శ్రీ సత్య సాయి": "Anantapur",
    "కర్నూలు": "Kurnool",
    "నంద్యాల": "Nandyal",
    "చిత్తూరు": "Chittoor",
    "తిరుపతి": "Tirupati"
}

# 🌦 English → Simple Telugu weather descriptions
WEATHER_TELUGU = {
    "clear sky": "ఆకాశం స్వచ్ఛంగా ఉంది",
    "few clouds": "కొద్దిగా మేఘాలు ఉన్నాయి",
    "scattered clouds": "చిన్నచిన్న మేఘాలు ఉన్నాయి",
    "broken clouds": "మేఘాలు ఎక్కువగా ఉన్నాయి",
    "overcast clouds": "ఆకాశం పూర్తిగా మేఘావృతమై ఉంది",

    "light rain": "తేలికపాటి వర్షం పడుతోంది",
    "moderate rain": "మధ్యస్థ వర్షం పడుతోంది",
    "heavy intensity rain": "భారీ వర్షం పడుతోంది",
    "very heavy rain": "అత్యంత భారీ వర్షం పడుతోంది",

    "thunderstorm": "ఉరుములతో కూడిన వర్షం",
    "mist": "మబ్బు కమ్ముకుంది",
    "haze": "పొగమంచు ఉంది",
    "fog": "మంచు కమ్ముకుంది",
    "smoke": "పొగ ఉంది",
    "dust": "దుమ్ము ఎక్కువగా ఉంది",
    "sand": "ఇసుక గాలి వీస్తోంది"
}


def get_weather(city_telugu=None):
    """
    Fetch real-time weather and return simple Telugu response
    """

    if not city_telugu:
        city_telugu = "హైదరాబాద్"

    # Telugu → English conversion
    city_english = TELUGU_TO_ENGLISH.get(city_telugu, "Hyderabad")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city_english}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return f"{city_telugu} వాతావరణ సమాచారం ప్రస్తుతం అందుబాటులో లేదు."

        temp = round(data["main"]["temp"], 1)
        desc_en = data["weather"][0]["description"].lower()
        desc_te = WEATHER_TELUGU.get(desc_en, "వాతావరణం సాధారణంగా ఉంది")

        return (
            f"{city_telugu} లో ప్రస్తుతం ఉష్ణోగ్రత {temp}°C.\n"
            f"వాతావరణ పరిస్థితి: {desc_te}."
        )

    except Exception:
        return "వాతావరణ సమాచారాన్ని పొందడంలో సమస్య వచ్చింది."
