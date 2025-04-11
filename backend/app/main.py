from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from . import crud, models, database, websocket
from .database import SessionLocal, engine
from .routes import router as visitor_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(visitor_router)