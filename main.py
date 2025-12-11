from fastapi import FastAPI
#permisos para conexion
from fastapi.middleware.cors import CORSMiddleware

#routers
from api.health import router as health_router
from api.upload import router as upload_router
from api.analyze import router as analyze_router

app = FastAPI(title="MYB - Mind Your Business API")

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- "*" permite entrar a cualquiera
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#conecta el router de healh a la app principal
app.include_router(health_router)

app.include_router(upload_router)

app.include_router(analyze_router)

#prueba de mensaje saludo
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Mind Your Business"}

