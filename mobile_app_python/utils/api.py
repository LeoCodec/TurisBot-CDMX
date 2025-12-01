import requests

SERVER_URL = "http://127.0.0.1:5000/chat"

def send_message(mensaje):
    try:
        response = requests.post(
            SERVER_URL,
            json={"mensaje": mensaje},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("respuesta", "Sin respuesta del servidor.")
        else:
            return f"Error {response.status_code}: No se pudo obtener respuesta."

    except Exception as e:
        return f"Error: No se pudo conectar al servidor ({e})"
