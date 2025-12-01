<div align="center"><!-- Asegúrate de que la imagen esté en tu repo --><img src="web_app/static/imagen.png" alt="Logo TurisBot" width="120" height="120">TurisBot CDMXTu asistente inteligente para explorar la Ciudad de México<!-- ESTADÍSTICAS DE LENGUAJE REALES --><p><a href="#-características">Características</a> •<a href="#-estructura">Estructura</a> •<a href="#-instalación">Instalación</a> •<a href="#-uso">Uso</a> •<a href="#-contacto">Contacto</a></p></div>🚀 DescripciónTurisBot CDMX es una solución integral (Web + Móvil) diseñada para asistir a turistas y ciudadanos de la CDMX. Utiliza un motor de procesamiento de lenguaje natural (AIML) para responder preguntas sobre turismo, transporte y seguridad en tiempo real.El proyecto demuestra la integración de una API RESTful en Flask con clientes multiplataforma (Navegador Web y App Android nativa).✨ CaracterísticasFuncionalidadDescripción🤖 Chatbot IARespuestas automáticas basadas en patrones AIML.🌍 MultilenguajeSoporte instantáneo para Español 🇲🇽, Inglés 🇺🇸, Alemán 🇩🇪 y Francés 🇫🇷.🚇 Info TransporteTarifas y horarios de Metro, Metrobús y Ecobici.🏛️ TurismoRecomendaciones de museos, zonas arqueológicas y gastronomía.🌗 Modo OscuroInterfaz adaptable (Claro/Oscuro) para mejorar la lectura.📱 Cross-PlatformFunciona en cualquier navegador y como App nativa.📂 Estructura del ProyectoTurisBot-CDMX/
├── 🌍 web_app/                  (Backend & Web Frontend)
│   ├── app.py                   # Servidor Flask Principal
│   ├── aiml/                    # 🧠 Cerebro del Chatbot
│   │   ├── main.aiml            # Reglas generales
│   │   ├── transporte.aiml      # Base de conocimiento: Transporte
│   │   └── ...
│   ├── static/                  # Estilos CSS y Scripts JS
│   ├── templates/               # HTML5
│   └── textos_chatbot.xml       # Textos i18n (Idiomas)
│
└── 📱 mobile_app_python/        (Cliente Móvil Kivy)
    ├── main.py                  # App Launcher
    ├── kivy_app.kv              # UI Design Language
    ├── buildozer.spec           # Configuración Android (APK)
    └── utils/                   # Conectores API
🛠️ InstalaciónPrerrequisitosPython 3.10 o superiorpip (Gestor de paquetes)1. Clonar y Configurar Entornogit clone [https://github.com/LeoCodec/TurisBot-CDMX.git](https://github.com/LeoCodec/TurisBot-CDMX.git)
cd TurisBot-CDMX

# Crear entorno virtual (Recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
2. Instalar DependenciasEl proyecto tiene dependencias separadas para Web y Móvil.Para el Servidor Web:cd web_app
pip install -r requirements.txt
Para la App Móvil:cd ../mobile_app_python
pip install kivy requests
▶️ UsoPaso 1: Iniciar el Cerebro (Backend)Es necesario que el servidor esté corriendo para que el chatbot responda.# Desde la carpeta web_app/
python app.py
El servidor iniciará en: http://127.0.0.1:5000Paso 2: Usar el ClienteOpción A: Web BrowserAbre tu navegador y ve a http://localhost:5000.Opción B: App Móvil (Simulador)Abre una nueva terminal.# Desde mobile_app_python/
python main.py
🧠 ¿Cómo funciona la IA? (AIML)El chatbot utiliza AIML (Artificial Intelligence Markup Language). El flujo de una conversación es:Input: Usuario escribe "¿Cuánto cuesta el metro?"Normalización: Python convierte a mayúsculas y quita acentos -> CUANTO CUESTA EL METRO.Matching: El motor busca en transporte.aiml:<category>
    <pattern>CUANTO CUESTA EL METRO</pattern>
    <template>El boleto cuesta 5 pesos.</template>
</category>
Output: El servidor devuelve la respuesta al cliente (Web o App).📸 Capturas de Pantalla<div align="center"><img src="web_app/static/Captura1.png" alt="Vista Web" width="400" style="border-radius:10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);"><!-- Agrega tus capturas aquí --></div>📞 Contacto y CréditosDesarrollado por Leo Cruz.📧 Email: leocode.contacto@gmail.com🐙 GitHub: @LeoCodecProyecto académico para la materia Sistemas Basados en Conocimiento.
