class IntentClassifier:
    def __init__(self):
        # 🌍 All districts (Telugu) – Telangana + Andhra Pradesh
        self.districts = [
            # Telangana
            "హైదరాబాద్", "మెదక్", "మేడ్చల్", "వరంగల్", "హనుమకొండ",
            "నిజామాబాద్", "కరీంనగర్", "ఖమ్మం", "సంగారెడ్డి",
            "సిద్దిపేట", "వికారాబాద్", "మహబూబ్‌నగర్",
            "నాగర్‌కర్నూల్", "నల్గొండ", "సూర్యాపేట",
            "ఆదిలాబాద్", "నిర్మల్", "మంచిర్యాల",

            # Andhra Pradesh
            "విశాఖపట్నం", "గుంటూరు", "తిరుపతి", "కడప",
            "నెల్లూరు", "కర్నూలు", "అనంతపురం", "చిత్తూరు",
            "శ్రీకాకుళం", "విజయనగరం"
        ]

    def predict(self, text):
        text = text.strip()

        # 👋 Greeting
        if any(w in text for w in ["నమస్తే", "నమస్కారం", "హాయ్", "హలో"]):
            return "greeting", None

        # ℹ️ Help / Capabilities
        if any(w in text for w in [
            "ఏమేమి మాట్లాడగలవు",
            "నువ్వు ఏమి చేయగలవు",
            "నీతో ఏమి అడగవచ్చు",
            "సహాయం",
            "హెల్ప్",
            "help"
        ]):
            return "help", None

        # 🌦 Weather
        if "వాతావరణం" in text:
            return "weather", self.extract_location(text)

        # 💰 Market price
        if any(w in text for w in ["ధర", "రేట్", "మార్కెట్"]):
            return "price", self.extract_crop(text)

        # 🌱 Crop advisory
        if any(w in text for w in ["సాగు", "సలహా", "ఎరువు"]):
            return "advisory", self.extract_crop(text)

        # 🏛 Government schemes (FINAL ROBUST LOGIC)
        if any(w in text for w in [
            "పథకం", "పథకాలు", "పథకాల",
            "స్కీమ్", "యోజన",
            "భీమా", "బీమా"
        ]):
            # ▶ Rythu Bandhu
            if "రైతు బంధు" in text:
                return "scheme", "రైతు బంధు"

            # ▶ Crop Insurance (PMFBY – ALL VARIANTS)
            if any(w in text for w in [
                "రైతు భీమా", "రైతు బీమా",
                "ఫసల్ భీమా", "ఫసల్ బీమా",
                "ఫసల్ భీమా యోజన", "ఫసల్ బీమా యోజన",
                "ప్రధాన్ మంత్రి ఫసల్ భీమా",
                "ప్రధానమంత్రి ఫసల్ బీమా",
                "ప్రధానమంత్రి ఫసల్ బీమా యోజన",
                "తెలుగు రైతు బీమా"
            ]):
                return "scheme", "రైతు భీమా"

            # ▶ PM-KISAN
            if any(w in text for w in ["పిఎం కిసాన్", "పీఎం కిసాన్", "కిసాన్"]):
                return "scheme", "పిఎం కిసాన్"

            # ▶ Soil Health Card
            if "మట్టి ఆరోగ్య కార్డు" in text:
                return "scheme", "మట్టి ఆరోగ్య కార్డు"

            # ▶ Generic schemes query
            return "scheme", "all"

        return "unknown", None

    def extract_location(self, text):
        for district in self.districts:
            if district in text:
                return district
        return None

    def extract_crop(self, text):
        if "మిర్చి" in text:
            return "మిర్చి"
        if "పత్తి" in text:
            return "పత్తి"
        if "వరి" in text:
            return "వరి"
        if "మొక్కజొన్న" in text:
            return "మొక్కజొన్న"
        if "పల్లీలు" in text:
            return "పల్లీలు"
        return None
