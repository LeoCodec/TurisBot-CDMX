# app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import xml.etree.ElementTree as ET
from chatbot_engine import ChatbotEngine

# Config
BASE_DIR = os.path.dirname(__file__)
XML_PATH = os.path.join(BASE_DIR, "textos_chatbot.xml")
AIML_DIR = os.path.join(BASE_DIR, "aiml")

app = Flask(__name__)
app.secret_key = "cambio_por_una_clave_mas_segura"  # cambia para producción

# Cargar textos multilenguaje desde XML
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

# Inicializar motor AIML
engine = ChatbotEngine(AIML_DIR)

def obtener_idioma():
    # obtener de query param > session > default 'es'
    lang = request.args.get("lang")
    if lang and lang in TEXTOS:
        session["idioma"] = lang
        return lang
    if "idioma" in session and session["idioma"] in TEXTOS:
        return session["idioma"]
    return "es"

@app.route("/", methods=["GET"])
def index():
    idioma = obtener_idioma()
    textos = TEXTOS.get(idioma, TEXTOS["es"])
    return render_template("index.html", textos=textos, idioma=idioma)

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Recibe:
      - msg: texto del usuario
      - lang: código de idioma (es,en,de,fr) opcional
    Devuelve:
      - respuesta del bot (texto)
    """
    user_msg = request.form.get("msg", "").strip()
    lang = request.form.get("lang", None)
    if not user_msg:
        return "No recibí mensaje.", 400
    if lang is None:
        # si no viene, tomar de session o default
        lang = session.get("idioma", "es")
    else:
        # guardar preferencia en session
        if lang in TEXTOS:
            session["idioma"] = lang
        else:
            lang = "es"

    # Preprocesamiento: AIML trabaja mejor con mayúsculas sin tildes
    # (python-aiml suele buscar patrones en mayúsculas)
    msg_for_kernel = user_msg.upper()

    # El motor AIML puede tener respuestas en varios idiomas si programaste patrones multi-idioma
    bot_response = engine.get_response(msg_for_kernel)

    # Si el bot no responde, devolver texto por idioma
    if not bot_response or bot_response.strip() == "":
        fallback = TEXTOS[lang].get("respuesta_demo", "No tengo información sobre eso.")
        bot_response = f"{fallback}"

    return bot_response

if __name__ == "__main__":
    # Si quieres cambiar puerto, modifícalo aquí
    app.run(host="0.0.0.0", port=5000, debug=True)
