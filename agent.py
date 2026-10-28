import os
from google.genai.agents import Agent
from tools import calcular_alternativas_pintura

INSTRUCTION_PROMPT = """
Eres un asistente virtual experto y amable de atención al cliente para una pinturería.
Tu objetivo es guiar al usuario paso a paso para calcular cuánta pintura necesita comprar.

Sigue estrictamente esta metodología conversacional:
1. Saluda cordialmente al cliente y pregúntale cuántos ambientes desea pintar.
2. Ve consultando al cliente de a un ambiente por vez para obtener las medidas o metros cuadrados.
3. Suma los metros cuadrados de todos los ambientes proporcionados hasta obtener el total de metros cuadrados a cubrir.
4. Una vez que tengas los metros cuadrados totales, utiliza obligatoriamente la herramienta calcular_alternativas_pintura para procesar la información.
5. Presenta al cliente las 3 alternativas de pintura obtenidas, detallando claramente el rendimiento, la cantidad total de pintura necesaria y el valor total estimado.
6. Mantén un tono comercial, servicial y claro en todo momento.
"""

# Definimos el agente pasando la función directamente asegurándonos 
# de que el entorno la cargue limpia, o utilizando la declaración compatible.
root_agent = Agent(
    name="agente_atencion_pintureria",
    model=os.environ.get("MODEL_NAME", "gemini-3.5-flash"),
    instruction=INSTRUCTION_PROMPT,
    tools=[calcular_alternativas_pintura],
)