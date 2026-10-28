FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

# Comando para ejecutar tu aplicación expuesta en Cloud Run
# CMD ["python", "main.py"]
# Usar Gunicorn para producción, leyendo la variable PORT de Cloud Run dinámicamente
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app