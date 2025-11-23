#---------
#Endpoint para subir la nómina
#---------
from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil # Librería estándar para operar con archivos
import os

router = APIRouter()

#donde se guardan las cosas
upload_dir = "tmp"

os.makedirs(upload_dir, exist_ok=True) #crea carpeta si no existe

@router.post("/upload")
async def up_file(file: UploadFile = File(...)):
    """
    Recibe un archivo (PDF o imagen), lo guarda en la carpeta tmp
    y devuelve el nombre del archivo guardado
    """
    #1. revisamos por contenido, no por extension de archivo
    #file.content_type es la etiqueta que envía el navegador
    if "pdf" not in file.content_type and "image" not in file.content_type:
        raise HTTPException(
            status_code=400,
            detail="Formato incorrecto. Revise que su archivo es un PDF o una imagen"
        )
    
    #2. Preparar la rut
    file_path = os.path.join(upload_dir, file.filename)

    #3. Guardar archivo
    try:
        #wb escribe en binario (necesario para pdf o imagen)
        with open(file_path, "wb") as buffer:
            #pilla el archivo, lo mete en el buffer
            shutil.copyfileobj(file.file, buffer)
    except Exception as error:
        #fallo por permisos, disco lleno...
        raise HTTPException(
            status_code=500,
            detail= f"Error al guardar el archivo: {str(error)}")
    
    #4. Respuesta en json
    return { 
        "filename" : file.filename,
        "content_type" : file.content_type,
        "saved_path" : file_path,
        "message" : "Archivo subido correctamente. Pendiente procesar."
    }