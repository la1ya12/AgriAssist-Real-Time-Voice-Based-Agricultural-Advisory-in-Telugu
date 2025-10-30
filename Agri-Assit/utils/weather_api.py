import requests

def get_weather(city="Medchal"):
    api_key = "322a0dc336116712f655acf15f1277b1"  # 🔸 Replace with your real key

    # 🌦 Telugu → English mapping for Telangana & Andhra Pradesh
    telugu_to_english = {
        # Telangana
        "హైదరాబాద్": "Hyderabad",
        "మేడ్చల్": "Medchal",
        "మేడ్చల్ మల్కాజిగిరి": "Medchal Malkajgiri",
        "వరంగల్": "Warangal",
        "నిజామాబాద్": "Nizamabad",
        "కరీంనగర్": "Karimnagar",
        "అదిలాబాద్": "Adilabad",
        "మంచిర్యాల": "Mancherial",
        "జగిత్యాల": "Jagtial",
        "పెద్దపల్లి": "Peddapalli",
        "రాజన్న సిరిసిల్ల": "Rajanna Sircilla",
        "నిర్మల్": "Nirmal",
        "కుమ్రంభీం ఆసిఫాబాద్": "Kumuram Bheem Asifabad",
        "జయశంకర్ భూపాలపల్లి": "Jayashankar Bhupalpally",
        "ములుగు": "Mulugu",
        "భద్రాద్రి కొత్తగూడెం": "Bhadradri Kothagudem",
        "ఖమ్మం": "Khammam",
        "మహబూబాబాద్": "Mahabubabad",
        "సూర్యాపేట": "Suryapet",
        "యాదాద్రి భువనగిరి": "Yadadri Bhuvanagiri",
        "జోగులాంబ గద్వాల్": "Jogulamba Gadwal",
        "నాగర్ కర్నూల్": "Nagarkurnool",
        "మహబూబ్‌నగర్": "Mahbubnagar",
        "వికారాబాద్": "Vikarabad",
        "రంగారెడ్డి": "Ranga Reddy",
        "సంగారెడ్డి": "Sangareddy",
        "మెదక్": "Medak",
        "సిద్దిపేట": "Siddipet",
        "కామారెడ్డి": "Kamareddy",
        "జనగామ": "Jangaon",
        "యాదగిరిగుట్ట": "Yadagirigutta",
        "నారాయణపేట్": "Narayanpet",
        "కొత్తగూడెం": "Kothagudem",
        "భూపాలపల్లి": "Bhupalpally",

        # Andhra Pradesh
        "విశాఖపట్నం": "Visakhapatnam",
        "విజయనగరం": "Vizianagaram",
        "శ్రీకాకుళం": "Srikakulam",
        "తూర్పు గోదావరి": "East Godavari",
        "పశ్చిమ గోదావరి": "West Godavari",
        "కృష్ణా": "Krishna",
        "గుంటూరు": "Guntur",
        "ప్రకాశం": "Prakasam",
        "నెల్లూరు": "Nellore",
        "చిత్తూరు": "Chittoor",
        "తిరుపతి": "Tirupati",
        "అన్నమయ్య": "Annamayya",
        "కడప": "Kadapa",
        "నంద్యాల": "Nandyal",
        "కర్నూలు": "Kurnool",
        "అల్లూరి సీతారామరాజు": "Alluri Sitarama Raju",
        "ఎలూరు": "Eluru",
        "బాపట్ల": "Bapatla",
        "కొనసీమ": "Konaseema",
        "పల్నాడు": "Palnadu",
        "నంద్యాల": "Nandyal",
        "పరమతీ పురం మన్యాం": "Parvathipuram Manyam",
        "తిరుపతి జిల్లా": "Tirupati",
        "శ్రీ శత్యసాయి": "Sri Sathya Sai"
    }

    # Reverse mapping for display
    eng_to_telugu = {v: k for k, v in telugu_to_english.items()}

    # Pick the correct city
    if city in telugu_to_english:
        eng_city = telugu_to_english[city]
    else:
        eng_city = city

    display_name = eng_to_telugu.get(eng_city, city)

    # 🌦 Fetch from OpenWeatherMap
    url = f"https://api.openweathermap.org/data/2.5/weather?q={eng_city}&appid={api_key}&lang=te&units=metric"

    try:
        r = requests.get(url)
        data = r.json()
        if data.get("main"):
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"{display_name} లో ప్రస్తుత ఉష్ణోగ్రత {temp}°C, వాతావరణం {desc}."
        else:
            return f"{display_name} వాతావరణ సమాచారం అందుబాటులో లేదు."
    except Exception as e:
        print("❌ Weather API error:", e)
        return "వాతావరణ సమాచారం పొందడంలో సమస్య ఏర్పడింది."
