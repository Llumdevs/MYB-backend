import fitz #para abrir pdfs -> pymupdf
import easyocr #ia para leer img
import numpy as np
import io
from PIL import Image, ImageOps, ImageEnhance

#inicializar ocr solo una vez al principio. Si se hace dentro de la función, el servidor se congelaría cada vez que subo un doc
print("cargarndo ocr...")
reader = easyocr.Reader(['es'], gpu=False) #buscan en español

def extract_text(file_content: bytes, filename: str) -> str:
    text_result = ""
    filename = filename.lower()

    try:
        # --- OPCIÓN A: PDF ---
        if filename.endswith(".pdf"):
            print("📄 Procesando PDF...")
            doc = fitz.open(stream=file_content, filetype="pdf")
            for page in doc:
                text_result += page.get_text()
                    
       # --- OPCIÓN B: IMAGEN (JPG/PNG) ---
        else:
            print("📸 Procesando Imagen (Modo Alta Calidad)...")
            
            try:
                image = Image.open(io.BytesIO(file_content))
            except Exception as e:
                print(f"❌ Error Pillow: {e}")
                return ""

            # 1. ESCALA DE GRISES (Quitamos colores que confunden)
            image = ImageOps.grayscale(image)
            
            # 2. AUMENTAR CONTRASTE (Hacer el negro más negro y el blanco más blanco)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0) # Doble de contraste

            # 3. GESTIÓN DE TAMAÑO (El equilibrio)
            # Una nómina A4 necesita píxeles. 1024 era muy poco.
            # Subimos a 2500. Si la imagen es menor, NO la tocamos.
            if image.width > 2500 or image.height > 2500:
                print("   ⚠️ Imagen gigante: Redimensionando a 2500px para no explotar la RAM")
                image.thumbnail((2500, 2500))
            else:
                print(f"   ✅ Manteniendo resolución original: {image.size}")
            
            # 4. Leer con EasyOCR
            img_np = np.array(image)
            
            # paragraph=False ayuda a leer líneas sueltas (números) mejor
            results = reader.readtext(img_np, detail=0, paragraph=False)
            
            for line in results:
                text_result += line + " "

        return text_result

    except Exception as e:
        print(f"❌ ERROR CRÍTICO EN OCR: {e}")
        return ""