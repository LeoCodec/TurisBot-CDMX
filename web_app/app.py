#  TurisBot CDMX - Servidor Flask (Web + App Móvil)

from flask import Flask, render_template, request, jsonify, session
import os
import xml.etree.ElementTree as ET
import unicodedata  # <--- (1) IMPORTANTE: Librería para quitar acentos
from chatbot_engine import ChatbotEngine

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
    
    if not user_msg.strip():
        return "No recibí mensaje.", 400

    idioma = session.get("idioma", "es")
    
    # (3) APLICAR LIMPIEZA AQUÍ
    user_msg_proc = normalizar_texto(user_msg)
    
    # Truco para AIML: Reiniciar contexto
    engine.kernel.setPredicate("topic", "") 
    
    bot_response = engine.get_response(user_msg_proc)

    if not bot_response:
        bot_response = TEXTOS[idioma].get("respuesta_demo", "No tengo información sobre eso.")

    return bot_response

# ENDPOINT PARA APP MÓVIL
@app.route("/chat", methods=["POST"])
def api_chat_movil():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    lang_recibido = data.get("lang", "es")

    if not mensaje.strip():
        return jsonify({"respuesta": "..."})

    # (4) APLICAR LIMPIEZA TAMBIÉN AQUÍ (CRUCIAL PARA LA APP)
    mensaje_proc = normalizar_texto(mensaje)
    
    respuesta = engine.get_response(mensaje_proc)

    if not respuesta:
        textos_lang = TEXTOS.get(lang_recibido, TEXTOS["es"])
        respuesta = textos_lang.get("fallback", "No tengo información disponible.")

    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)