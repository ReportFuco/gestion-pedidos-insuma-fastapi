from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

def add_cors(app: FastAPI):
    if os.getenv("ENV") == "production":
        origins = [
            "https://fucolabs.dev",
            "https://www.fucolabs.dev"
        ]
    else:
        origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://192.168.1.2:5173",
            "https://erp.insuma.cl",
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"]
    )