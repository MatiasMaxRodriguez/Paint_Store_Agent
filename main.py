import os
import traceback
from flask import Flask, request, jsonify, render_template_string
from google.genai import types
from agent import root_agent

app = Flask(__name__)

# Configuración básica (Cloud Run inyecta automáticamente la variable PORT)
PORT = int(os.environ.get("PORT", 8080))

# Interfaz web simple integrada
CHAT_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Asistente Pinturería - Chat</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f9; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .chat-container { width: 100%; max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .chat-box { height: 400px; border: 1px solid #ddd; border-radius: 4px; overflow-y: scroll; padding: 10px; margin-bottom: 15px; background: #fafafa; }
        .message { margin-bottom: 10px; padding: 8px 12px; border-radius: 6px; line-height: 1.4; }
        .user { background: #e3f2fd; text-align: right; margin-left: 20%; }
        .assistant { background: #e8f5e9; text-align: left; margin-right: 20%; }
        .input-group { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; }
        button { padding: 10px 20px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background: #115293; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h2>Asistente de Pinturería 🎨</h2>
        <div id="chat-box" class="chat-box"></div>
        <div class="input-group">
            <input type="text" id="user-input" placeholder="Escribe tu mensaje aquí..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Enviar</button>
        </div>
    </div>
    <script>
        const chatBox = document.getElementById('chat-box');
        
        async function sendMessage() {
            const inputField = document.getElementById('user-input');
            const message = inputField.value.trim();
            if (!message) return;

            appendMessage(message, 'user');
            inputField.value = '';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                appendMessage(data.response || "Error de respuesta del agente.", 'assistant');
            } catch (error) {
                appendMessage("Error de conexión con el servidor.", 'assistant');
            }
        }

        function appendMessage(text, sender) {
            const div = document.createElement('div');
            div.className = `message ${sender}`;
            div.innerText = text;
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter') sendMessage();
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    """Sirve una interfaz visual básica para interactuar con el agente."""
    return render_template_string(CHAT_HTML)

@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint requerido por Cloud Run para verificar que el contenedor está activo."""
    return jsonify({"status": "healthy"}), 200

import traceback

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    """
    Endpoint principal con manejo de errores detallado para depuración.
    """
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"response": "El mensaje no puede estar vacío."}), 200

        from google import genai
        client = genai.Client()
        
        response = client.models.generate_content(
            model=root_agent.model,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=root_agent.instruction,
                temperature=0.3
            )
        )

        agent_response_text = response.text
        return jsonify({"response": agent_response_text})

    except Exception as e:
        # 1. Imprime el error técnico completo en los logs de Cloud Run
        error_completo = traceback.format_exc()
        app.logger.error(f"EXCEPCIÓN DETALLADA:\n{error_completo}")
        
        # 2. Envía el error exacto a la interfaz web para verlo en el chat
        return jsonify({"response": f"⚠️ Error técnico: {str(e)}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)