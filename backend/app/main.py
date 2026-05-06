from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import productos

app = FastAPI(title="TPV Ortopedia")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(productos.router)

@app.get("/")
def root():
    return {"mensaje": "TPV Ortopedia funcionando correctamente"}

from app.routers import usuarios
app.include_router(usuarios.router)

from app.routers import ventas
app.include_router(ventas.router)

from app.routers import caja
app.include_router(caja.router)