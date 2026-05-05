from fastapi import FastAPI
from presentation.api.routes import router

app = FastAPI(title="LSC API")
app.include_router(router)