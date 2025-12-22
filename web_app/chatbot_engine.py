import aiml
import os
import re
import unicodedata

class ChatbotEngine:
    """
    Motor de IA optimizado para cargar archivos AIML de forma estable.
    Solo procesa texto en Español para evitar conflictos de patrones.
    """
    def __init__(self, aiml_dir):
        self.kernel = aiml.Kernel()
        self.aiml_dir = aiml_dir
        self.kernel.verbose(False)
        self._load_aiml_files()

    def _load_aiml_files(self):
        print(f"--- Cargando CEREBRO en: {self.aiml_dir} ---")
        if not os.path.exists(self.aiml_dir):
            print(f"Error: No existe la carpeta {self.aiml_dir}")
            return

        for root, _, files in os.walk(self.aiml_dir):
            for f in files:
                if f.lower().endswith(".aiml"):
                    try:
                        self.kernel.learn(os.path.join(root, f))
                        print(f"✔ Cargado: {f}")
                    except Exception as e:
                        print(f"❌ Error en {f}: {e}")

    def _normalizar(self, text):
        """Limpia acentos y convierte a mayúsculas para match exacto"""
        if not text: return ""
        text = text.upper()
        nfkd = unicodedata.normalize('NFKD', text)
        text = u"".join([c for c in nfkd if not unicodedata.combining(c)])
        text = re.sub(r"[^A-Z0-9 ]", "", text)
        return text.strip()

    def get_response(self, text_es):
        """Busca respuesta en el kernel AIML"""
        limpio = self._normalizar(text_es)
        print(f"IA Pensando patrón: '{limpio}'")
        response = self.kernel.respond(limpio)
        return response if response else ""