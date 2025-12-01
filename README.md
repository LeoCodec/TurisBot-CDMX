# 🏙️ TurisBot CDMX  
Asistente inteligente de turismo, transporte y seguridad para la Ciudad de México.  
Incluye **aplicación web (Flask)** y **aplicación móvil (Kivy)** conectadas al mismo backend.

![Python](https://img.shields.io/badge/Python-45.4%25-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-17.7%25-yellow)
![CSS](https://img.shields.io/badge/CSS-16.0%25-blueviolet)
![HTML](https://img.shields.io/badge/HTML-11.3%25-orange)
![KVLang](https://img.shields.io/badge/KVLang-9.6%25-green)

---

## 📌 Descripción general

TurisBot CDMX es un asistente conversacional desarrollado con:

- **Python 3.12**
- **Flask (para la Web App)**
- **Kivy (para la App Móvil)**
- **AIML (Artificial Intelligence Markup Language)**
- **Requests** para comunicación entre aplicaciones

El proyecto permite:

✔ Información turística  
✔ Localización de zonas interesantes  
✔ Transporte público  
✔ Consejos de seguridad  
✔ Múltiples idiomas (es / en / de / fr)  
✔ Tema claro / oscuro  
✔ Banderas disponibles en el selector de idioma  
✔ Integración web + móvil en tiempo real

---

## ⚙️ Instalación

---

### 🔧 1. Crear entorno virtual


python3 -m venv venv
source venv/bin/activate
📦 2. Instalar dependencias
Web App (Flask):
bash
Copiar código
pip install flask python-aiml requests
Mobile App (Kivy):
bash
Copiar código
pip install kivy requests
🚀 Ejecución
🌐 Web App (Flask)
bash
Copiar código
cd web_app
python app.py
La app correrá en:

http://127.0.0.1:5000

http://TU-IP:5000 (ideal para conectarlo desde el celular)

📱 App Móvil (Kivy)
bash
Copiar código
cd mobile_app_python
python main.py
Para generar un APK:

bash
Copiar código
sudo apt install buildozer
buildozer init
buildozer -v android debug

🧠 Inteligencia AIML
El bot usa AIML para controlar las respuestas:

main.aiml → respuestas generales

turismo.aiml → lugares turísticos, museos, parques

transporte.aiml → metro, metrobús, RTP, horarios

seguridad.aiml → emergencias, contacto, precauciones

Flask carga los AIML automáticamente.

🎨 Temas: claro / oscuro
Ambas apps soportan:

✔ Tema claro
Fondo blanco

Texto oscuro

Inputs en gris suave

Botón azul

✔ Tema oscuro
Fondo #121212

Texto blanco/gris claro

Botones oscuros tipo Material

La Web App guarda la preferencia con:

javascript
Copiar código
localStorage.getItem("theme")
La App móvil usa:

scss
Copiar código
app.cambiar_tema()
🌍 Selector de idioma con banderas
Idiomas disponibles:

Idioma	Bandera	Código
Español	🇲🇽	es
Inglés	🇺🇸	en
Alemán	🇩🇪	de
Francés	🇫🇷	fr

El idioma cambia:

Textos en la interfaz

Placeholder del input

Mensaje de bienvenida

Respuestas AIML (si están definidas)

🔗 Comunicación Web ↔ Móvil
Ambas apps se comunican con el backend vía:

bash
Copiar código
POST /api/chat
Parámetros:

ini
Copiar código
msg=texto_del_usuario
lang=es|en|de|fr
La app móvil utiliza requests.post().

🧪 Sugerencias de prueba
Iniciar el servidor Flask

Probar conversación básica

Cambiar tema claro/oscuro

Cambiar idioma y verificar texto dinámico

Conectar desde el teléfono a la IP local

Ejecutar la app móvil y probar chat

Revisar respuestas AIML

📌 Notas importantes
No usar Flask en producción sin WSGI (Gunicorn, Nginx)

Buildozer solo funciona bien en Linux

En Kivy, los colores se actualizan usando DictProperty

Para agregar banderas en móvil puede usarse un footer con imágenes PNG

✨ Autor
Leo Cruz
Desarrollador de software
📧 leocode.contacto@gmail.com

