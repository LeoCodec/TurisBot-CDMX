import requests

# Asegúrate de que esta IP sea la de tu PC si pruebas en un celular real.
# Si pruebas en la misma PC, 127.0.0.1 está bien.
SERVER_URL = "http://127.0.0.1:5000/chat"

def send_message(mensaje, idioma="es"):
    try:
        # Enviamos mensaje Y el idioma seleccionado
        payload = {
            "mensaje": mensaje,
            "lang": idioma
        }
        
        response = requests.post(SERVER_URL, json=payload, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return data.get("respuesta", "Sin respuesta del servidor.")
        else:
            return f"Error {response.status_code}: Servidor no disponible."

    except Exception as e:
        return f"Error de conexión: {e}"