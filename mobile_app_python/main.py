from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, DictProperty
from kivy.clock import Clock
from utils.api import send_message

class TurisBotApp(App):
    idioma_actual_code = StringProperty("es")
    hint_text_actual = StringProperty("Escribe tu mensaje...")
    
    # NUEVO: Propiedad para la ruta de la imagen de la bandera
    flag_src = StringProperty("assets/mx.png") 

    # NUEVO: Tu "JSON" de configuración de banderas
    banderas = {
        "es": "assets/mx.png",
        "en": "assets/us.png",
        "de": "assets/de.png",
        "fr": "assets/fr.png"
    }
    
    # Propiedades para el Tema
    tema_actual = StringProperty("dark")
    colores = DictProperty()

    # 🎨 PALETA IDENTICA A TU WEB
    colores_oscuros = {
        "bg": (0.07, 0.07, 0.07, 1),
        "container": (0.12, 0.12, 0.12, 1),
        "text": (0.92, 0.92, 0.92, 1),
        "user_bubble": (0.39, 0.71, 0.96, 1),
        "bot_bubble": (0.50, 0.78, 0.52, 1),
        "btn_bg": (0.91, 0.12, 0.39, 1),
        "btn_text": (1, 1, 1, 1),
        "input_bg": (0.12, 0.12, 0.12, 1),
        "cursor": (0.91, 0.12, 0.39, 1)
    }

    colores_claros = {
        "bg": (0.96, 0.97, 0.98, 1),
        "container": (1, 1, 1, 1),
        "text": (0.13, 0.13, 0.13, 1),
        "user_bubble": (0.10, 0.45, 0.91, 1),
        "bot_bubble": (0.06, 0.61, 0.34, 1),
        "btn_bg": (0.10, 0.45, 0.91, 1),
        "btn_text": (1, 1, 1, 1),
        "input_bg": (0.98, 0.99, 1, 1),
        "cursor": (0.10, 0.45, 0.91, 1)
    }

    def build(self):
        self.colores = self.colores_oscuros
        return Builder.load_file("kivy_app.kv")

    def cambiar_tema(self):
        if self.tema_actual == "dark":
            self.tema_actual = "light"
            self.colores = self.colores_claros
        else:
            self.tema_actual = "dark"
            self.colores = self.colores_oscuros

    def cambiar_idioma(self, seleccion):
        # 1. Obtener código limpio (ej: "es")
        code = seleccion.lower()
        self.idioma_actual_code = code
        
        # 2. NUEVO: Actualizar la imagen buscando en el diccionario
        # Si no encuentra la imagen, usa mx.png por defecto
        self.flag_src = self.banderas.get(code, "assets/mx.png")

        # 3. Actualizar placeholder
        placeholders = {
            "es": "Escribe tu mensaje...",
            "en": "Type your message...",
            "de": "Nachricht eingeben...",
            "fr": "Écrivez votre message..."
        }
        self.hint_text_actual = placeholders.get(code, "...")

    def enviar_mensaje(self):
        input_widget = self.root.ids.input_box
        msg = input_widget.text.strip()
        if not msg: return

        self.agregar_burbuja(msg, es_usuario=True)
        input_widget.text = ""
        Clock.schedule_once(lambda dt: self._procesar_envio(msg))

    def _procesar_envio(self, msg):
        respuesta = send_message(msg, self.idioma_actual_code)
        self.agregar_burbuja(respuesta, es_usuario=False)

    def agregar_burbuja(self, texto, es_usuario):
        chat_list = self.root.ids.chat_history
        from kivy.factory import Factory
        
        if es_usuario:
            burbuja = Factory.BurbujaUsuario()
            burbuja.text = f"Tú:\n{texto}"
            burbuja.color = self.colores["user_bubble"]
        else:
            burbuja = Factory.BurbujaBot()
            burbuja.text = f"TurisBot:\n{texto}"
            burbuja.color = self.colores["bot_bubble"]
            
        chat_list.add_widget(burbuja)
        self.root.ids.scroller.scroll_y = 0

if __name__ == "__main__":
    TurisBotApp().run()