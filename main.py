from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.api.routes import router

app = FastAPI(title="LSC API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type"],
)

app.include_router(router)