from flask import Flask, render_template, request, session
import os
import xml.etree.ElementTree as ET
from chatbot_engine import ChatbotEngine
from deep_translator import GoogleTranslator

# CONFIGURACIÓN
BASE_DIR = os.path.dirname(__file__)
XML_PATH = os.path.join(BASE_DIR, "textos_chatbot.xml")
AIML_DIR = os.path.join(BASE_DIR, "aiml")

app = Flask(__name__)
app.secret_key = "turisbot_cdmx_2026_pro"

# CARGAR TEXTOS DE INTERFAZ (ES, EN, DE)
def cargar_textos(ruta):
    try:
        tree = ET.parse(ruta)
        root = tree.getroot()
        data = {}
        for lang in root.findall("language"):
            code = lang.get("code")
            data[code] = {txt.get("key"): txt.text for txt in lang.findall("text")}
        return data
    except Exception as e:
        print(f"Error XML: {e}")
        return {"es": {"titulo": "TurisBot"}}

TEXTOS_WEB = cargar_textos(XML_PATH)
engine = ChatbotEngine(AIML_DIR)

@app.route("/", methods=["GET"])
def index():
    # Solo aceptamos es, en, de
    lang = request.args.get("lang", session.get("idioma", "es"))
    if lang not in ['es', 'en', 'de']: lang = 'es'
    session["idioma"] = lang
    
    textos = TEXTOS_WEB.get(lang, TEXTOS_WEB['es'])
    return render_template("index.html", textos=textos, idioma=lang)

@app.route("/api/chat", methods=["POST"])
def api_chat():
    user_msg = request.form.get("msg", "")
    current_lang = session.get("idioma", "es")

    # 1. Traducir entrada -> Español (si no es es)
    msg_es = user_msg
    if current_lang != "es":
        try:
            msg_es = GoogleTranslator(source='auto', target='es').translate(user_msg)
        except: pass

    # 2. Obtener respuesta del Cerebro (en Español)
    respuesta_es = engine.get_response(msg_es)
    
    if not respuesta_es:
        return TEXTOS_WEB.get(current_lang, {}).get("fallback", "No tengo esa información.")

    # 3. Traducir salida -> Idioma del usuario (si no es es)
    # IMPORTANTE: No traducimos si hay HTML (tarjetas) para no romper etiquetas
    if current_lang != "es" and "<div" not in respuesta_es:
        try:
            respuesta_final = GoogleTranslator(source='es', target=current_lang).translate(respuesta_es)
            return respuesta_final
        except: pass

    return respuesta_es

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)