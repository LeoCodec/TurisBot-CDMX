from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, DictProperty
from utils.api import send_message


class TurisBotApp(App):

    chat_history = StringProperty("Bienvenido a TurisBot CDMX\n")
    theme = "light"

    # 🎨 Paleta para tema claro
    colores_claros = {
        "bg": (1, 1, 1, 1),
        "text": (0, 0, 0, 1),
        "input_bg": (0.95, 0.95, 0.95, 1),
        "button_bg": (0.1, 0.45, 0.9, 1),
        "button_text": (1, 1, 1, 1)
    }

    # 🌙 Paleta para tema oscuro
    colores_oscuros = {
        "bg": (0.07, 0.07, 0.07, 1),
        "text": (0.96, 0.96, 0.96, 1),
        "input_bg": (0.15, 0.15, 0.15, 1),
        "button_bg": (0.25, 0.25, 0.25, 1),
        "button_text": (1, 1, 1, 1)
    }

    # Diccionario vinculado al KV
    colores = DictProperty()

    def build(self):
        self.colores = self.colores_claros
        return Builder.load_file("kivy_app.kv")

    # ⭐ FUNCION CORRECTA ⭐
    def cambiar_tema(self):
        if self.theme == "light":
            self.theme = "dark"
            self.colores = self.colores_oscuros
        else:
            self.theme = "light"
            self.colores = self.colores_claros

    def enviar_mensaje(self, mensaje):
        mensaje = mensaje.strip()
        if not mensaje:
            return

        self.chat_history += f"[color=#1A73E8]Tú:[/color] {mensaje}\n"
        respuesta = send_message(mensaje)
        self.chat_history += f"[color=#0F9D58]Bot:[/color] {respuesta}\n"
        self.root.ids.input_box.text = ""


if __name__ == "__main__":
    TurisBotApp().run()
