from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os
import uuid
import re

from utils.nlp_model import IntentClassifier
from utils.weather_api import get_weather
from utils.market_api import get_market_price
from utils.crop_advisory import get_crop_advisory
from utils.schemes import get_government_schemes

app = Flask(__name__)
classifier = IntentClassifier()


def clean_for_tts(text):
    """
    Remove emojis and special symbols so gTTS
    does NOT read them as 'image', 'symbol', etc.
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub("", text)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/voice', methods=['POST'])
def voice():
    text = request.form.get('text', '').strip()

    display_text = ""
    tts_text = ""

    if not text:
        display_text = "క్షమించండి రైతు గారు 🙏\nమీ మాట వినలేకపోయాను."
        tts_text = "క్షమించండి రైతు గారు. మీ మాట వినలేకపోయాను."

    else:
        intent, entity = classifier.predict(text)

        # 👋 Greeting
        if intent == "greeting":
            display_text = (
                "నమస్కారం రైతు గారు 🙏\n"
                "నేను మీ తెలుగు రైతు సహాయకుడిని 🌾\n"
                "మీకు ఎలా సహాయం చేయగలను?"
            )
            tts_text = (
                "నమస్కారం రైతు గారు. "
                "నేను మీ తెలుగు రైతు సహాయకుడిని. "
                "మీకు ఎలా సహాయం చేయగలను?"
            )

        # ℹ️ Help / Capabilities
        elif intent == "help":
            display_text = (
                "నేను మీ తెలుగు రైతు సహాయకుడిని 🌾\n\n"
                "నేను ఈ విషయాల్లో సహాయం చేయగలను:\n"
                "• వాతావరణ సమాచారం (ఉదాహరణకు: మెదక్ వాతావరణం)\n"
                "• పంట మార్కెట్ ధరలు (ఉదాహరణకు: మిర్చి ధర)\n"
                "• సాగు సలహాలు (ఉదాహరణకు: వరి సాగు సలహా)\n"
                "• ప్రభుత్వ పథకాలు (ఉదాహరణకు: రైతు బంధు పథకం)\n\n"
                "మీకు కావాల్సిన విషయం అడగండి."
            )
            tts_text = display_text

        # 🌦 Weather
        elif intent == "weather":
            display_text = get_weather(entity)
            tts_text = display_text

        # 💰 Market price
        elif intent == "price":
            display_text = get_market_price(entity)
            tts_text = display_text

        # 🌱 Crop advisory
        elif intent == "advisory":
            display_text = get_crop_advisory(entity)
            tts_text = display_text

        # 🏛 Government schemes
        elif intent == "scheme":
            display_text = get_government_schemes(entity)
            tts_text = display_text

        # ❌ Unknown
        else:
            display_text = (
                "క్షమించండి రైతు గారు 😔\n"
                "మీ ప్రశ్న అర్థం కాలేదు.\n"
                "మీకు ఎలా సహాయం చేయగలను?"
            )
            tts_text = (
                "క్షమించండి రైతు గారు. "
                "మీ ప్రశ్న అర్థం కాలేదు. "
                "మీకు ఎలా సహాయం చేయగలను?"
            )

    # Clean text for TTS
    tts_text = clean_for_tts(tts_text)

    # Delete old audio files
    for f in os.listdir("static"):
        if f.startswith("response_") and f.endswith(".mp3"):
            try:
                os.remove(os.path.join("static", f))
            except:
                pass

    # Generate audio
    audio_name = f"response_{uuid.uuid4().hex[:6]}.mp3"
    audio_path = os.path.join("static", audio_name)

    try:
        tts = gTTS(tts_text, lang="te")
        tts.save(audio_path)
        audio_url = "/" + audio_path
    except:
        audio_url = ""

    return jsonify({
        "text": display_text,
        "audio": audio_url
    })


if __name__ == "__main__":
    app.run(debug=True)
