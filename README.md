# MYB – Backend (FastAPI)

Este es el backend del proyecto **MYB – Mind Your Business**, encargado del procesamiento de nóminas mediante:

- OCR (EasyOCR/Tesseract)
- Anonimización automática (regex + spaCy)
- Extracción inteligente con IA (OpenAI API)
- Comparación con convenios laborales
- API REST desarrollada con FastAPI

## Endpoints iniciales
- `GET /health` → Comprobación del estado
- `POST /upload` → Subir nómina para análisis

## Tecnologías
- Python 3
- FastAPI
- EasyOCR / Tesseract
- spaCy
- OpenAI API
- DigitalOcean App Platform

