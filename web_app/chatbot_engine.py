import aiml
import os
import re
from langdetect import detect
from deep_translator import GoogleTranslator

class ChatbotEngine:
    def __init__(self, aiml_dir):
        self.kernel = aiml.Kernel()
        self.aiml_dir = aiml_dir
        self.kernel.verbose(False)
        self._load_aiml_files()

    
    # CARGA AIML
    
    def _load_aiml_files(self):
        print(f"--- Cargando AIML desde: {self.aiml_dir} ---")
        for root, _, files in os.walk(self.aiml_dir):
            for f in files:
                if f.lower().endswith(".aiml"):
                    try:
                        self.kernel.learn(os.path.join(root, f))
                        print(f"✔ AIML cargado: {f}")
                    except Exception as e:
                        print(f"❌ Error cargando {f}: {e}")

    
    # NORMALIZACIÓN
    
    def _normalizar(self, text):
        text = text.upper()
        text = re.sub(r"[^A-Z0-9ÁÉÍÓÚÜÑ ]", "", text)

        # Eliminar acentos
        acentos = {
            "Á": "A", "É": "E", "Í": "I",
            "Ó": "O", "Ú": "U", "Ü": "U",
            "Ñ": "N",
        }
        for k, v in acentos.items():
            text = text.replace(k, v)

        return text.strip()

    
    # DETECTAR IDIOMA NATURAL
    
    def _detectar_idioma(self, text):
        try:
            return detect(text)
        except:
            return "es"

    
    # TRADUCCIÓN AUTOMÁTICA
    
    def _traducir(self, texto_es, idioma_destino):
        if idioma_destino == "es":
            return texto_es  # No traducir

        try:
            return GoogleTranslator(
                source="es",
                target=idioma_destino
            ).translate(texto_es)
        except:
            return texto_es

    
    # RESPUESTA PRINCIPAL
    
    def get_response(self, text):

        # Normalizar para patrones AIML
        limpio = self._normalizar(text)

        # Detectar idioma real del usuario
        idioma = self._detectar_idioma(text)

        # Obtener respuesta en español (idioma base del AIML)
        respuesta_es = self.kernel.respond(limpio)

        # Si AIML no entiende → fallback por idioma
        if not respuesta_es or respuesta_es.strip() == "":
            fallbacks = {
                "es": "No entendí eso, ¿podrías repetirlo?",
                "en": "Sorry, I didn't understand that.",
                "fr": "Désolé, je n'ai pas compris.",
                "de": "Entschuldigung, das habe ich nicht verstanden.",
            }
            return fallbacks.get(idioma, "No entendí eso.")

        # Traducir solo si usuario no habla español
        idiomas_google = {
            "es": "es",
            "en": "en",
            "fr": "fr",
            "de": "de"
        }

        destino = idiomas_google.get(idioma, "es")

        return self._traducir(respuesta_es, destino)
