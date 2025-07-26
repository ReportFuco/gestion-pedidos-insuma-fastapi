from app.routes import clientes, notas_venta, auth, usuarios
from fastapi import FastAPI

app = FastAPI(
    title="API Insuma",
    version="1.0.0"
)

# Incluir routers
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(clientes.router)
app.include_router(notas_venta.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Insuma 🚀"}
