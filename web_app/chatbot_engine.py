# chatbot_engine.py
import aiml
import os

class ChatbotEngine:
    def __init__(self, aiml_dir):
        self.kernel = aiml.Kernel()
        self.aiml_dir = aiml_dir
        self._load_aiml_files()

    def _load_aiml_files(self):
        # Aprende todos los archivos AIML dentro de aiml_dir
        for root, _, files in os.walk(self.aiml_dir):
            for f in files:
                if f.lower().endswith(".aiml"):
                    path = os.path.join(root, f)
                    try:
                        self.kernel.learn(path)
                    except Exception as e:
                        print(f"Error cargando {path}: {e}")

    def get_response(self, text):
        try:
            resp = self.kernel.respond(text)
            return resp
        except Exception as e:
            print("Error en kernel.respond:", e)
            return ""
