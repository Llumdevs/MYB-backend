import openai
import os
import json
import base64 # <--- Necesario para convertir la imagen en texto transportable
from dotenv import load_dotenv 

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("⚠️ ADVERTENCIA: No se encontró OPENAI_API_KEY en .env")

client = openai.OpenAI(api_key=api_key)

# --- FUNCIÓN 1: Para Texto (PDFs) ---
def analyze_payroll(text_anonymized):
    print("--- 🧠 Conectando con OpenAI (Modo Texto)... ---")
    
    system_prompt = """
    Eres un experto abogado laboralista y asesor financiero.
    Analiza el texto de esta nómina.
    ⚠️ PRIVACIDAD: No incluyas nombres propios ni DNI en la respuesta.
    Devuelve SOLO un JSON:
    {
        "resumen": "Resumen breve...",
        "salario_bruto": 0.00,
        "salario_neto": 0.00,
        "consejos": ["Consejo 1", "Consejo 2"]
    }
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analiza esto:\n\n{text_anonymized}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"❌ Error OpenAI: {e}")
        return _error_response()

# --- FUNCIÓN 2: Para Imágenes (Vision) 👁️ ---
def analyze_payroll_image(image_bytes):
    print("--- 👁️ Conectando con OpenAI (Modo Visión)... ---")
    
    # 1. Convertimos la imagen a Base64 (el formato que pide OpenAI)
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    system_prompt = """
    Eres un experto abogado laboralista. Estás viendo una imagen de una nómina.
    Extrae los datos financieros clave y dame consejos.
    
    ⚠️ PRIVACIDAD CRÍTICA: 
    - Aunque veas nombres o DNI en la imagen, NO los transcribas en el JSON.
    - Trata los datos como anónimos.
    
    Devuelve SOLO un JSON válido con esta estructura:
    {
        "resumen": "Resumen breve...",
        "salario_bruto": 0.00,
        "salario_neto": 0.00,
        "consejos": ["Consejo 1", "Consejo 2"]
    }
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # El modelo mini también tiene visión y es barato
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analiza esta imagen de nómina:"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"❌ Error OpenAI Vision: {e}")
        return _error_response()

# Helper para devolver error limpio
def _error_response():
    return {
        "resumen": "Error al analizar.",
        "salario_bruto": 0,
        "salario_neto": 0,
        "consejos": ["Inténtalo de nuevo."]
    }