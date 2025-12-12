from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

from services.ocr_service import extract_text 
from services.anonimizador import anonymize_text
# Importamos AMBAS funciones de análisis
from services.openai_service import analyze_payroll, analyze_payroll_image 

router = APIRouter()
os.makedirs("tmp", exist_ok=True)

@router.post("/analyze")
async def analyze_payroll_endpoint(file: UploadFile = File(...)):
    
    filename = file.filename.lower()
    
    # 1. Guardar en disco (como querías)
    temp_filename = f"temp_{file.filename}"
    temp_path = os.path.join("tmp", temp_filename)
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Leemos los bytes para procesar
        with open(temp_path, "rb") as f:
            file_content = f.read()

        # --- BIFURCACIÓN DEL CAMINO ---
        
        # CAMINO A: Es una IMAGEN (JPG/PNG) -> Usamos GPT-4 Vision 👁️
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            print(f"📸 Imagen detectada ({filename}). Usando GPT-4 Vision...")
            # Enviamos la imagen DIRECTA a OpenAI (sin pasar por EasyOCR local)
            result_json = analyze_payroll_image(file_content)
            return result_json

        # CAMINO B: Es un PDF -> Usamos el método clásico 📄
        elif filename.endswith('.pdf'):
            print(f"📄 PDF detectado ({filename}). Usando OCR Local...")
            
            # 1. OCR Local
            text = extract_text(file_content, file.filename)
            if not text.strip():
                 raise HTTPException(status_code=400, detail="PDF vacío o ilegible.")
            
            # 2. Anonimizar texto
            clean_text = anonymize_text(text)
            
            # 3. Analizar texto
            result_json = analyze_payroll(clean_text)
            return result_json

        else:
             raise HTTPException(status_code=400, detail="Formato no soportado.")

    except Exception as e:
        print(f"❌ Error crítico: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)