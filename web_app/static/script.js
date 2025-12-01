// script.js - Maneja envíos y recepción del bot
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const chatBox = document.getElementById("chat-box");
    const langSelect = document.getElementById("lang-select");
    // inicialLang viene de index.html inyectado por Flask
    let lang = typeof inicialLang !== "undefined" ? inicialLang : "es";

    langSelect.addEventListener("change", function () {
        lang = this.value;
        // recargar la página con parámetro lang para actualizar textos
        const url = new URL(window.location.href);
        url.searchParams.set("lang", lang);
        window.location = url.toString();
    });

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
        // petición al backend
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

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") sendMessage();
    });
});
