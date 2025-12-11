#  Mind Your Business (MYB) - Analizador de Nóminas con IA

**MYB** es una aplicación Full Stack diseñada para empoderar a los trabajadores, ayudándoles a entender sus nóminas mediante Inteligencia Artificial, garantizando siempre la privacidad de sus datos.

## Características Principales

* **Lectura Inteligente (OCR):** Extracción de texto desde PDFs y fotos usando `EasyOCR` y `PyMuPDF`.
* **Privacidad por Diseño:** Sistema de anonimización propio que detecta y censura nombres, DNI y cuentas bancarias antes de enviar datos a la nube.
* **Análisis con IA:** Integración con **OpenAI (GPT-4o)** para explicar conceptos legales y verificar cálculos salariales.
* **Arquitectura Limpia:** Backend estructurado en capas (Controladores, Servicios, Utilidades).

## Tecnologías Usadas

### Backend 
* **Lenguaje:** Python 3.10+
* **Framework:** FastAPI
* **IA & NLP:** OpenAI API, SpaCy (para anonimización), EasyOCR.

### Frontend 📱
* **Framework:** Flutter (Dart)
* **Plataforma:** Web, Android, iOS.

## 🔧 Instalación y Uso

1. Clonar el repositorio.
2. Crear un archivo `.env` basado en el ejemplo y añadir tu `OPENAI_API_KEY`.
3. Ejecutar el servidor: `uvicorn main:app --reload`.
