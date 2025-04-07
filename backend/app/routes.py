# routes.py
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, database, websocket
router = APIRouter()

ws_manager = websocket.WebSocketManager()

#? Websocket Routes

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    print("✅ Client connected")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📨 Received: {data}")
            await websocket.send_text("Message Received: " + data)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        print("❌ Client disconnected")

#? HTTP Routes

@router.get("/visitors")
def get_visitors(db: Session = Depends(database.get_db)):
    return crud.get_visitors_inside(db)

@router.post("/visitor")
def add_visitor(name: str, visitorid: str, inside: bool, properties: dict, db: Session = Depends(database.get_db)):
    return crud.create_visitor(db=db, name=name, visitorid=visitorid, inside=inside, properties=properties)

@router.get("/visitors/search")
def search_visitors(search_query: str, db: Session = Depends(database.get_db)):
    visitors = crud.search_visitors_by_name(db, search_query)
    if visitors:
        return {"visitors": visitors}
    else:
        return {"message": "No visitors found matching the search"}

@router.get("/visitors/{visitor_id}")
def get_visitor(visitor_id: str, db: Session = Depends(database.get_db)):
    visitor = crud.get_visitor_by_id(db, visitor_id)
    if visitor:
        return {"visitor": visitor}
    else:
        return {"message": "Visitor not found"}
