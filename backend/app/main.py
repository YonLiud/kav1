from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from . import crud, models, database, websocket
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/visitors")
def get_visitors(db: Session = Depends(get_db)):
    return crud.get_visitors_inside(db)

@app.post("/visitor")
def add_visitor(name: str, visitorid: str, inside: bool, properties: dict, db: Session = Depends(get_db)):
    return crud.create_visitor(db=db, name=name, visitorid=visitorid, inside=inside, properties=properties)