🏙️ TurisBot CDMX

Asistente Inteligente de Turismo, Transporte y Seguridad para la Ciudad de México.

Este proyecto integra una Web App (Flask) y una Mobile App (Kivy), ambas conectadas a un mismo cerebro de Inteligencia Artificial basado en AIML.

📌 Descripción General

TurisBot CDMX es un sistema conversacional diseñado para ayudar a turistas y locales. El núcleo del proyecto está construido con:

🐍 Python 3.12: Lenguaje base.

🌶️ Flask: Backend y API REST para la versión web.

📱 Kivy: Framework para la aplicación móvil nativa (Android).

🤖 AIML (Artificial Intelligence Markup Language): Motor de procesamiento de lenguaje natural.

🌐 Requests: Para la comunicación Cliente-Servidor en la app móvil.

Funcionalidades Principales

✔ Consultas Turísticas: Recomendaciones de museos, parques y zonas de interés.
✔ Transporte: Información sobre Metro, Metrobús y tarifas.
✔ Seguridad: Consejos y números de emergencia.
✔ Multilenguaje: Soporte completo para Español (ES), Inglés (EN), Alemán (DE) y Francés (FR).
✔ Interfaz Adaptable: Tema Claro/Oscuro y diseño responsivo.

📁 Estructura del Proyecto

El proyecto se divide en dos grandes módulos: el servidor web (Backend + Frontend Web) y la aplicación móvil (Cliente Android).

TurisBot-CDMX/
│
├── web_app/                          # 🌍 MÓDULO WEB & BACKEND
│   ├── aiml/                         # Cerebro del Chatbot (Base de Conocimiento)
│   │   ├── main.aiml                 # Saludos y lógica general
│   │   ├── seguridad.aiml            # Patrones de seguridad
│   │   ├── transporte.aiml           # Patrones de transporte
│   │   └── turismo.aiml              # Patrones de turismo
│   ├── static/                       # Recursos Frontend
│   │   ├── script.js                 # Lógica JS (AJAX)
│   │   └── style.css                 # Estilos CSS modernos
│   ├── templates/
│   │   └── index.html                # Interfaz Web Principal
│   ├── app.py                        # Servidor Flask (Punto de entrada)
│   ├── chatbot_engine.py             # Motor de carga y procesamiento AIML
│   ├── textos_chatbot.xml            # Textos de UI Multilenguaje
│   └── requirements.txt              # Dependencias del servidor
│
└── mobile_app_python/                # 📱 MÓDULO MÓVIL (KIVY)
    ├── assets/
    │   └── icons/                    # Iconos y recursos gráficos
    ├── utils/
    │   ├── api.py                    # Cliente HTTP para conectar con Flask
    │   └── ui_components.py          # Componentes UI reutilizables
    ├── buildozer.spec                # Configuración de compilación (Android)
    ├── kivy_app.kv                   # Diseño de interfaz (Kivy Language)
    └── main.py                       # Punto de entrada de la App Móvil


⚙️ Instalación y Configuración

1. Prerrequisitos

Tener instalado Python 3.10+. Se recomienda usar un entorno virtual.

# Crear entorno virtual
python3 -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Mac/Linux)
source venv/bin/activate


2. Instalación de Dependencias

Para la Web App (Servidor):

cd web_app
pip install -r requirements.txt
# Instala: flask, python-aiml, requests


Para la Mobile App (Cliente Kivy):

cd mobile_app_python
pip install kivy requests


🚀 Ejecución

Paso 1: Levantar el Servidor (Web App)

El cerebro del bot vive aquí. Es necesario que esto corra primero.

cd web_app
python app.py


El servidor iniciará en: http://127.0.0.1:5000

Nota: Si vas a probar la app móvil desde tu celular, asegúrate de que ambos dispositivos estén en la misma red Wi-Fi y modifica la IP en mobile_app_python/utils/api.py por la IP local de tu PC (ej. 192.168.1.X).

Paso 2: Ejecutar la App Móvil (Simulación en PC)

En una nueva terminal:

cd mobile_app_python
python main.py


Paso 3: Generar APK (Opcional - Requiere Linux)

Para compilar la app para Android usa Buildozer:

cd mobile_app_python
buildozer init
buildozer -v android debug


🧠 Arquitectura del Chatbot (AIML)

La lógica conversacional reside en web_app/aiml/. El sistema carga estos archivos al iniciar app.py.

Categorías (<category>): Unidad básica de conocimiento.

Patrones (<pattern>): Lo que el usuario escribe (normalizado a mayúsculas).

Plantillas (<template>): La respuesta del bot.

Ejemplo de flujo:

Usuario envía: "Hola, ¿cuánto cuesta el metro?"

Python normaliza: "HOLA CUANTO CUESTA EL METRO"

Motor AIML busca coincidencia en transporte.aiml.

Devuelve: "El boleto cuesta 5 pesos."

🎨 Personalización y UI

Temas (Dark/Light Mode)

Web: Detecta preferencia o usa botón de toggle. Persistencia vía localStorage.

Móvil: Gestionado en Kivy mediante utils/ui_components.py y propiedades dinámicas en kivy_app.kv.

Idiomas (i18n)

El sistema soporta cambio dinámico de idioma.

Frontend Web: Selector <select> que recarga los textos desde textos_chatbot.xml.

Backend: La sesión de Flask recuerda el idioma seleccionado (es, en, de, fr) para responder en el idioma correcto si el patrón AIML lo soporta.

🧪 Guía de Pruebas

Para verificar que todo funcione correctamente:

Backend: Ejecuta python app.py. No debe haber errores de "File not found" al cargar los .aiml.

Web: Entra a localhost:5000. Prueba escribir "Hola" y cambiar el idioma a Inglés.

API: Puedes probar la API con CURL o Postman:

curl -X POST http://localhost:5000/api/chat -d "msg=hola&lang=es"


Móvil: Ejecuta la app Kivy. Debería conectar con el servidor (asegura que el servidor esté corriendo). Si dice "Error de conexión", revisa la IP en api.py.

🤝 Autor

Leo Cruz
Desarrollador de Software & Estudiante de Ingeniería

Proyecto realizado como parte de la asignatura de Sistemas Basados en Conocimiento.
