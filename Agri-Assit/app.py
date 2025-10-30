from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os, uuid
from utils.weather_api import get_weather
from utils.market_api import get_market_price
from utils.nlp_model import IntentClassifier
from utils.crop_advisory import get_crop_advisory

app = Flask(__name__)
classifier = IntentClassifier()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/voice', methods=['POST'])
def process_voice():
    text = request.form.get('text', '').strip()
    
    if not text:
        reply = "క్షమించండి, మీ మాట వినలేకపోయాను. దయచేసి మళ్లీ ప్రయత్నించండి."
    else:
        intent, slot = classifier.predict(text)
        if intent == "weather":
            reply = get_weather(slot or "మేడ్చల్")
        elif intent == "price":
            reply = get_market_price(slot or "మిర్చి")
        elif intent == "advisory":
            reply = get_crop_advisory(slot or "మిర్చి")
        else:
            reply = "క్షమించండి రైతు గారు, దయచేసి మళ్లీ ప్రయత్నించండి. ఉదాహరణకు — 'మేడ్చల్ వాతావరణం' లేదా 'మిర్చి ధర' అని అడగండి."

    # 🔹 Clean old audio files
    for file in os.listdir("static"):
        if file.startswith("response_"):
            os.remove(os.path.join("static", file))

    # 🔹 Create new audio file with unique name
    audio_id = str(uuid.uuid4())[:8]
    audio_path = f"static/response_{audio_id}.mp3"

    tts = gTTS(reply, lang='te')
    tts.save(audio_path)

    return jsonify({"text": reply, "audio": f"/{audio_path}"})

if __name__ == '__main__':
    app.run(debug=True)
