document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const chatBox = document.getElementById("chat-box");
    
    let lang = typeof inicialLang !== "undefined" ? inicialLang : "es";

    // ============================================
    // LÓGICA DEL SELECTOR (SOLO BANDERAS)
    // ============================================
    const customSelect = document.getElementById("custom-lang-select");
    
    if (customSelect) {
        const selectedDisplay = customSelect.querySelector(".selected-lang");
        const optionsContainer = customSelect.querySelector(".options");
        const options = customSelect.querySelectorAll(".option");

        // Abrir / Cerrar menú
        selectedDisplay.addEventListener("click", (e) => {
            e.stopPropagation();
            optionsContainer.classList.toggle("show");
        });

        // Cerrar si clic fuera
        document.addEventListener("click", (e) => {
            if (!customSelect.contains(e.target)) {
                optionsContainer.classList.remove("show");
            }
        });

        // Al elegir bandera
        options.forEach(option => {
            option.addEventListener("click", () => {
                const newLang = option.getAttribute("data-lang");
                
                if (newLang !== lang) {
                    const url = new URL(window.location.href);
                    url.searchParams.set("lang", newLang);
                    window.location = url.toString();
                }
                optionsContainer.classList.remove("show");
            });
        });
    }

    // ============================================
    // FUNCIONES DEL CHAT
    // ============================================

    function appendMessage(who, text) {
        const wrapper = document.createElement("div");
        wrapper.className = "message";
        wrapper.innerHTML = `<span class="who ${who === 'user' ? 'user' : 'bot'}">${who === 'user' ? 'Tú' : 'TurisBot'}</span>
                             <span class="text">${text}</span>`;
        chatBox.appendChild(wrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function sendMessage() {
        const msg = input.value.trim();
        if (!msg) return;
        appendMessage('user', msg);
        input.value = "";
        procesarMensaje(msg);
    }

    // Función separada para procesar el envío (usada por botón y por chips)
    function procesarMensaje(msg) {
        const form = new URLSearchParams();
        form.append("msg", msg);
        form.append("lang", lang);

        fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: form.toString()
        })
        .then(r => {
            if (!r.ok) throw new Error("Error en la respuesta");
            return r.text();
        })
        .then(text => {
            appendMessage('bot', text);
        })
        .catch(err => {
            appendMessage('bot', "Error de conexión con el servidor.");
            console.error(err);
        });
    }

    // ============================================
    // NUEVA FUNCIÓN PARA LOS CHIPS (BOTONES DE OPCIONES)
    // ============================================
    // Esta función se llama desde el HTML generado por AIML (onclick="enviarTexto('1')")
    window.enviarTexto = function(texto) {
        appendMessage('user', texto); // Muestra lo que "dijo" el usuario
        procesarMensaje(texto);       // Lo envía al servidor
    };

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") sendMessage();
    });

    const themeBtn = document.getElementById("theme-toggle");
    if (themeBtn) {
        themeBtn.addEventListener("click", () => {
            document.body.classList.toggle("dark-mode");
            localStorage.setItem("theme", document.body.classList.contains("dark-mode") ? "dark" : "light");
        });
    }

    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
});