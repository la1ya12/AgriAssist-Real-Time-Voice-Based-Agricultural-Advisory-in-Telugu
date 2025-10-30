# utils/nlp_model.py
import re

class IntentClassifier:
    def predict(self, text):
        text = text.strip().lower()

        # 🌦 Weather intent
        if any(word in text for word in [
            "వాతావరణం", "వర్షం", "వర్షం పడుతుందా", "ఎండ", "ఎండగా", "ఎండగా ఉందా",
            "సూర్యుడు", "మబ్బు", "మబ్బుగా", "చలి", "ఉష్ణోగ్రత", "వాతావరణం చెప్పండి",
            "సూర్యకాంతి", "వెచ్చగా", "చల్లగా"
        ]):
            return "weather", self.extract_location(text)

        # 💰 Price intent
        elif any(word in text for word in ["ధర", "రేట్", "మార్కెట్", "అమ్మకం", "ధర చెప్పండి"]):
            return "price", self.extract_crop(text)

        # 🌾 Advisory intent
        elif any(word in text for word in ["సలహా", "పంట", "వ్యవసాయం", "ఎరువు", "పంటకు సలహా"]):
            return "advisory", self.extract_crop(text)

        else:
            return "unknown", None

    def extract_location(self, text):
        telugu_to_english = {
            # Telangana
            "హైదరాబాద్": "Hyderabad",
            "మేడ్చల్": "Medchal",
            "మెదక్": "Medak",
            "వరంగల్": "Warangal",
            "నిజామాబాద్": "Nizamabad",
            "కరీంనగర్": "Karimnagar",
            "కామారెడ్డి": "Kamareddy",
            "సిద్దిపేట": "Siddipet",
            "మహబూబ్‌నగర్": "Mahbubnagar",
            "సంగారెడ్డి": "Sangareddy",
            "వికారాబాద్": "Vikarabad",
            "రంగారెడ్డి": "Ranga Reddy",
            "ఖమ్మం": "Khammam",
            "భద్రాద్రి": "Bhadradri Kothagudem",
            "మహబూబాబాద్": "Mahabubabad",
            "సూర్యాపేట": "Suryapet",
            "యాదాద్రి": "Yadadri Bhuvanagiri",
            "జోగులాంబ": "Jogulamba Gadwal",
            "నాగర్ కర్నూల్": "Nagarkurnool",
            "మంచిర్యాల": "Mancherial",
            "జగిత్యాల": "Jagtial",
            "పెద్దపల్లి": "Peddapalli",
            "నిర్మల్": "Nirmal",
            "అదిలాబాద్": "Adilabad",
            "ములుగు": "Mulugu",
            "జయశంకర్": "Jayashankar Bhupalpally",
            "కోటగూడెం": "Kothagudem",
            "జనగామ": "Jangaon",
            "రాజన్న": "Rajanna Sircilla",
            # Andhra (optional)
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
            "కడప": "Kadapa",
            "కర్నూలు": "Kurnool",
            "తిరుపతి": "Tirupati"
        }

        for telugu, eng in telugu_to_english.items():
            if telugu in text:
                return eng  # ✅ Return English name directly for weather API
        return "Medchal"  # Default

    def extract_crop(self, text):
        text = text.lower()

        crop_map = {
        # 🌶 Chillies
            "మిర్చి": "మిర్చి",
            "chilli": "మిర్చి",
            "chillies": "మిర్చి",

        # 🌾 Paddy / Rice
            "బియ్యం": "బియ్యం",
            "వరి": "వరి",
            "rice": "వరి",
            "paddy": "వరి",

        # 🧵 Cotton
            "పత్తి": "పత్తి",
            "cotton": "పత్తి",

        # 🌽 Maize / Corn
            "మొక్కజొన్న": "మొక్కజొన్న",
            "corn": "మొక్కజొన్న",
            "maize": "మొక్కజొన్న",

        # 🌾 Jowar
            "జొన్న": "జొన్న",
            "jowar": "జొన్న",

        # 🥜 Groundnut / పల్లీ
            "వేరుసెనగ": "గ్రౌండ్‌నట్",
            "పల్లీ": "గ్రౌండ్‌నట్",
            "పల్లీలు": "గ్రౌండ్‌నట్",
            "సెనగ": "గ్రౌండ్‌నట్",
            "గ్రౌండ్ నెట్": "గ్రౌండ్‌నట్",
            "గ్రౌండ్‌నట్": "గ్రౌండ్‌నట్",
            "ground nut": "గ్రౌండ్‌నట్",
            "groundnut": "గ్రౌండ్‌నట్",
            "peanut": "గ్రౌండ్‌నట్",
            "peanuts": "గ్రౌండ్‌నట్",
        }

        for key, val in crop_map.items():
            if key in text:
                return val

    # 🆕 if user mentioned an unknown crop name, extract that Telugu word after 'ధర'
        if "ధర" in text:
            parts = text.split("ధర")[0].strip().split()
            if parts:
                return parts[-1]  # last word before "ధర"
        return None
