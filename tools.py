import os
import io
from google.cloud import storage
from pypdf import PdfReader

def obtener_catalogo_desde_gcs() -> str:
    """Descarga el PDF de precios y rendimiento desde un bucket de GCP y extrae su texto."""
    bucket_name = os.environ.get("GCS_BUCKET_NAME", "catalogo-pintureria-bucket")
    blob_name = os.environ.get("GCS_BLOB_NAME", "catalogo_pinturas.pdf")
    
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        pdf_bytes = blob.download_as_bytes()
        reader = PdfReader(io.BytesIO(pdf_bytes))
        
        texto_catalogo = ""
        for page in reader.pages:
            texto_catalogo += page.extract_text() + "\n"
            
        return texto_catalogo
    except Exception as e:
        return f"Error al acceder a GCS ({str(e)}). Usando catálogo base: " \
               "1. Línea Económica: Rendimiento 10m² por litro (2 manos). Precio por L: $3500. " \
               "2. Línea Standard: Rendimiento 12m² por litro (2 manos). Precio por L: $5800. " \
               "3. Línea Superior: Rendimiento 14m² por litro (2 manos). Precio por L: $8900."

def calcular_alternativas_pintura(metros_totales: float) -> str:
    """
    Calcula la cantidad de pintura necesaria y 3 alternativas de presupuesto 
    basándose en los metros cuadrados totales a cubrir (considerando 2 manos).
    
    Args:
        metros_totales: Los metros cuadrados totales a pintar.
    """
    catalogo_texto = obtener_catalogo_desde_gcs()
    
    rendimientos = [
        {"categoria": "Línea Económica", "rendimiento_m2_l": 10.0, "precio_litro": 3500.0},
        {"categoria": "Línea Standard (Látex)", "rendimiento_m2_l": 12.0, "precio_litro": 5800.0},
        {"categoria": "Línea Superior (Lavable)", "rendimiento_m2_l": 14.0, "precio_litro": 8900.0}
    ]
    
    resultado = f"Para una superficie total de {metros_totales:.2f} m² (considerando 2 manos de aplicación):\n\n"
    
    for alt in rendimientos:
        litros_necesarios = metros_totales / alt["rendimiento_m2_l"]
        costo_total = litros_necesarios * alt["precio_litro"]
        
        resultado += f"- **{alt['categoria']}**:\n"
        resultado += f"  * Rendimiento: {alt['rendimiento_m2_l']} m²/L (2 manos)\n"
        resultado += f"  * Cantidad estimada: {litros_necesarios:.1f} litros\n"
        resultado += f"  * Valor total: ${costo_total:,.2f}\n\n"
        
    resultado += f"Catálogo de referencia:\n{catalogo_texto[:200]}..."
    return resultado