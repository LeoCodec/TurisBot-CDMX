#  TurisBot CDMX - Servidor Flask (Web)

from flask import Flask, render_template, request, jsonify, session
import os
import xml.etree.ElementTree as ET
import unicodedata  # <--- (1) IMPORTANTE: Librería para quitar acentos
from chatbot_engine import ChatbotEngine
import googletrans
from deep_translator import GoogleTranslator

# CONFIG GENERAL
BASE_DIR = os.path.dirname(__file__)
XML_PATH = os.path.join(BASE_DIR, "textos_chatbot.xml")
AIML_DIR = os.path.join(BASE_DIR, "aiml")

app = Flask(__name__)
app.secret_key = "clave_super_segura_123"

# CARGAR TEXTOS MULTILENGUAJE
def cargar_textos_desde_xml(ruta_xml):
    tree = ET.parse(ruta_xml)
    root = tree.getroot()
    textos = {}
    for lang in root.findall("language"):
        codigo = lang.get("code")
        textos[codigo] = {}
        for txt in lang.findall("text"):
            clave = txt.get("key")
            valor = txt.text or ""
            textos[codigo][clave] = valor
    return textos

TEXTOS = cargar_textos_desde_xml(XML_PATH)

# INICIALIZAR MOTOR AIML
engine = ChatbotEngine(AIML_DIR)

# --- (2) FUNCIÓN NUEVA: LIMPIEZA DE TEXTO ---
def normalizar_texto(texto):
    """
    Elimina acentos y caracteres especiales para que AIML entienda.
    Ejemplo: "¡Hola! ¿Qué línea es?" -> "HOLA QUE LINEA ES"
    """
    if not texto: return ""
    
    # 1. Separar caracteres de sus tildes
    nfkd = unicodedata.normalize('NFKD', texto)
    
    # 2. Filtrar y quedarse solo con las letras base (sin la tilde)
    texto_sin_tildes = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    
    # 3. Convertir a mayúsculas y quitar espacios extra
    return texto_sin_tildes.upper().strip()

# CONTROL DE IDIOMA
def obtener_idioma():
    lang = request.args.get("lang")
    if lang and lang in TEXTOS:
        session["idioma"] = lang
        return lang
    if "idioma" in session and session["idioma"] in TEXTOS:
        return session["idioma"]
    return "es"

# RUTA PRINCIPAL (WEB)
@app.route("/", methods=["GET", "POST"])
def index():
    idioma = obtener_idioma()
    textos = TEXTOS.get(idioma, TEXTOS["es"])
    return render_template("index.html", textos=textos, idioma=idioma, respuesta=textos.get("respuesta_demo"))

# ENDPOINT PARA AJAX WEB
@app.route("/api/chat", methods=["POST"])
def api_chat_web():
    user_msg = request.form.get("msg", "")
    idioma = session.get("idioma", "es")

    # Normalizar
    user_msg_proc = normalizar_texto(user_msg)

    # Si no es español → traducir ANTES del AIML
    if idioma != "es":
        try:
            traducido = GoogleTranslator(source=idioma, target="es").translate(user_msg)
            user_msg_proc = normalizar_texto(traducido)
        except:
            pass

    # Respuesta en español desde el AIML
    bot_response_es = engine.get_response(user_msg_proc)

    if not bot_response_es:
        bot_response_es = TEXTOS["es"].get("respuesta_demo", "No tengo información sobre eso.")

    # Si idioma ≠ español → traducimos la respuesta al idioma del usuario
    if idioma != "es":
        try:
            bot_response = GoogleTranslator(source="es", target=idioma).translate(bot_response_es)
        except:
            bot_response = bot_response_es
    else:
        bot_response = bot_response_es

    return bot_response



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)