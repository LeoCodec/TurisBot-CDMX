#  TurisBot CDMX - Servidor Flask (Web + App Móvil)

# Librerías
from flask import Flask, render_template, request, jsonify, session
import os
import xml.etree.ElementTree as ET
from chatbot_engine import ChatbotEngine


# CONFIG GENERAL

BASE_DIR = os.path.dirname(__file__)
XML_PATH = os.path.join(BASE_DIR, "textos_chatbot.xml")
AIML_DIR = os.path.join(BASE_DIR, "aiml")

app = Flask(__name__)
app.secret_key = "clave_super_segura_123"  #se deb de se cambiar en producción


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


# CONTROL DE IDIOMA

def obtener_idioma():
    lang = request.args.get("lang")

    # si viene en URL → guardar en sesión
    if lang and lang in TEXTOS:
        session["idioma"] = lang
        return lang

    # si ya existía en sesión → usarlo
    if "idioma" in session and session["idioma"] in TEXTOS:
        return session["idioma"]

    return "es"  # idioma por defecto

# RUTA PRINCIPAL (WEB)

@app.route("/", methods=["GET", "POST"])
def index():
    idioma = obtener_idioma()
    textos = TEXTOS.get(idioma, TEXTOS["es"])

    mensaje = ""
    respuesta = ""

    if request.method == "POST":
        mensaje = request.form.get("mensaje", "")
        idioma = request.form.get("idioma", "es")
        textos = TEXTOS.get(idioma, TEXTOS["es"])

        mensaje_proc = mensaje.upper()
        respuesta = engine.get_response(mensaje_proc)

        if not respuesta:
            respuesta = textos.get("respuesta_demo", "No tengo información sobre eso.")

    return render_template("index.html",
                           textos=textos,
                           idioma=idioma,
                           mensaje=mensaje,
                           respuesta=respuesta)


# ENDPOINT PARA AJAX WEB

@app.route("/api/chat", methods=["POST"])
def api_chat_web():
    user_msg = request.form.get("msg", "").strip()

    if not user_msg:
        return "No recibí mensaje.", 400

    idioma = session.get("idioma", "es")
    user_msg_proc = user_msg.upper()
    bot_response = engine.get_response(user_msg_proc)

    if not bot_response:
        bot_response = TEXTOS[idioma].get("respuesta_demo", "No tengo información sobre eso.")

    return bot_response


# ENDPOINT PARA APP MÓVIL (Kivy)
@app.route("/chat", methods=["POST"])
def api_chat_movil():
    """
    Recibe JSON: { "mensaje": "Hola" }
    Devuelve:    { "respuesta": "Hola turista!" }
    """
    data = request.get_json()
    mensaje = data.get("mensaje", "")

    if not mensaje.strip():
        return jsonify({"respuesta": "No recibí mensaje."})

    mensaje_proc = mensaje.upper()
    respuesta = engine.get_response(mensaje_proc)

    if not respuesta:
        idioma = session.get("idioma", "es")
        respuesta = TEXTOS[idioma].get("respuesta_demo", "No tengo información.")

    return jsonify({"respuesta": respuesta})


# EJECUTAR SERVIDOR

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
