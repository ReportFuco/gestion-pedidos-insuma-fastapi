from app.routes import clientes, notas_venta, auth, usuarios
from fastapi import FastAPI
import uvicorn


app = FastAPI(
    title="API Insuma",
    version="1.0.0",
    root_path="/insuma"
)

# Incluir routers
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(clientes.router)
app.include_router(notas_venta.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Insuma 🚀"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        workers=4
    )