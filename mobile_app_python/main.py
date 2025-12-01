from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from utils.api import send_message


class TurisBotApp(App):
    chat_history = StringProperty("Bienvenido a TurisBot CDMX\n")

    def build(self):
        return Builder.load_file("kivy_app.kv")

    def enviar_mensaje(self, mensaje):
        mensaje = mensaje.strip()
        if not mensaje:
            return
        
        # Mostrar mensaje del usuario
        self.chat_history += "[color=#2196F3]Tú:[/color] Hola\n"

        # Obtener respuesta de Flask
        respuesta = send_message(mensaje)

        # Mostrar respuesta
        self.chat_history += "[color=#4CAF50]Bot:[/color] Bienvenido turista\n"

        # Limpiar TextInput
        self.root.ids.input_box.text = ""


if __name__ == "__main__":
    TurisBotApp().run()
