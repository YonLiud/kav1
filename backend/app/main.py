from fastapi import FastAPI
from . import models
from .database import engine
from .routes import router as visitor_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(visitor_router)
