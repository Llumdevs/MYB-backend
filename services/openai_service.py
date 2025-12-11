import openai
import os
import json
from dotenv import load_dotenv #leer env

# 1. Cargar la configuración
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Si no hay clave, avisamos (pero no rompemos el programa todavía)
if not api_key:
    print("ADVERTENCIA: No se encontró OPENAI_API_KEY en .env")

# Configuramos el cliente
client = openai.OpenAI(api_key=api_key)

def analyze_payroll(text_anonymized):
    """
    Recibe: Texto de la nómina (censurado).
    Envía: A GPT-4o-mini para análisis real.
    Devuelve: JSON estructurado.
    """
    print("Conectando OpenAI...")
    
    # EL PROMPT: Las instrucciones para el experto
    system_prompt = """
    Eres un experto abogado laboralista y asesor financiero en España.
    Analiza el texto de esta nómina (OCR).
    
    Tu misión es extraer datos y dar consejos útiles.
    Devuelve SOLO un JSON válido con esta estructura exacta:
    {
        "resumen": "Breve explicación general de la nómina en 2 frases.",
        "salario_bruto": 0.00,
        "salario_neto": 0.00,
        "consejos": [
            "Consejo 1 sobre impuestos o convenio",
            "Consejo 2 sobre mejoras posibles",
            "Consejo 3 (opcional)"
        ]
    }
    Si no encuentras algún dato, pon 0.00 o "No encontrado".
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # El modelo que usamos
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analiza esto:\n\n{text_anonymized}"}
            ],
            response_format={"type": "json_object"}, # Obligamos a que sea JSON
            temperature=0.2 # Creatividad baja (para que sea preciso con los números)
        )
        
        # Leemos la respuesta de la IA
        content = response.choices[0].message.content
        print("Recibido correctamente.")
        
        # Convertimos el texto a Diccionario Python
        return json.loads(content)

    except Exception as e:
        print(f"Error en OpenAI: {e}")
        # En caso de error, devolvemos algo para que la app no explote
        return {
            "resumen": "Hubo un error al analizar la nómina con la IA.",
            "salario_bruto": 0,
            "salario_neto": 0,
            "consejos": ["Inténtalo de nuevo más tarde."]
        }