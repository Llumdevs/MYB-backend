from fastapi import FastAPI
from api.health import router as health_router
from api.upload import router as upload_router

app = FastAPI(title="MYB - Mind Your Business API")

#conecta el router de healh a la app principal
app.include_router(health_router)

app.include_router(upload_router)

#prueba de mensaje saludo
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Mind Your Business"}

