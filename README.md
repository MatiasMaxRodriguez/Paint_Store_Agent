# Paint Store Agent 🎨🤖

Un agente inteligente de atención al cliente diseñado para una pinturería, capaz de guiar a los usuarios en el cálculo de metros cuadrados por ambientes y proporcionar alternativas de presupuestos de pintura en base a un catálogo en PDF alojado en un Bucket de Google Cloud Storage (GCS).

El proyecto está desarrollado utilizando **Python**, **Flask**, la librería oficial del SDK de **Google GenAI**, y está preparado para ser desplegado en contenedores sobre **Google Cloud Run**.

---

## 🚀 Características Principales

* **Asistencia Conversacional Guiada:** El agente interactúa paso a paso con el cliente (consultando ambientes, dimensiones y sumando superficies totales).
* **Base de Conocimiento en Cloud Storage:** Lee dinámicamente un documento PDF con precios y especificaciones desde un bucket de GCP.
* **Cálculo de Alternativas:** Proporciona múltiples opciones de presupuestos y rendimiento de pintura (considerando aplicaciones a dos manos).
* **Despliegue en la Nube:** Arquitectura lista para producción containerizada mediante Docker y alojada en Google Cloud Run.

---

## 🛠️ Stack Tecnológico

* **Python 3.11+**
* **Google GenAI SDK** (para la gestión del modelo y las instrucciones del agente)
* **Flask** (para el servidor web y la interfaz de chat)
* **Google Cloud Storage & PyPDF** (para la lectura del catálogo en PDF)
* **Gunicorn** (como servidor WSGI de producción)
* **Docker & Google Cloud Run**

---

## 📁 Estructura del Proyecto

```text
pintureria-agent/
├── agent.py          # Definición del agente y su prompt de sistema
├── tools.py          # Lógica de conexión a GCS y cálculo de alternativas
├── main.py           # Servidor web Flask e interfaz visual de chat
├── requirements.txt  # Dependencias del proyecto
└── Dockerfile        # Configuración para contenedorizar la aplicación
```

---

## ⚙️ Configuración y Despliegue Local

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/Paint_Store_Agent.git
   cd Paint_Store_Agent
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura tus variables de entorno:**
   Crea un archivo `.env` o define las variables en tu entorno:
   ```env
   GEMINI_API_KEY=tu_api_key_de_google
   GCS_BUCKET_NAME=nombre-de-tu-bucket
   GCS_BLOB_NAME=catalogo_pinturas.pdf
   ```

4. **Ejecuta la aplicación localmente:**
   ```bash
   python main.py
   ```
   Abre tu navegador en `http://localhost:8080`.

---

## ☁️ Despliegue en Google Cloud Run

Para desplegar el agente directamente en Cloud Run utilizando la compilación por fuente:

```bash
gcloud run deploy pintureria-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=tu_api_key,GCS_BUCKET_NAME=tu_bucket
```

---

## 👨‍💻 Autor

Desarrollado por **Matías Maximiliano Rodríguez**.
