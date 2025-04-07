from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
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
            await ws_manager.send_personal_message(data, websocket)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        print("❌ Client disconnected")

#? HTTP Routes

@router.get("/visitors")
def get_visitors(db: Session = Depends(database.get_db)):
    return crud.get_visitors_inside(db)

@router.post("/visitor")
def add_visitor(visitor: schemas.VisitorCreate, db: Session = Depends(database.get_db)):
    db_visitor = crud.create_visitor(db=db, name=visitor.name, visitorid=visitor.visitorid, properties=visitor.properties)
    if db_visitor:
        return db_visitor
    else:
        raise HTTPException(status_code=400, detail="Failed to create visitor")


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

@router.post("/visitors/{visitor_id}/status")
async def change_status(visitor_id: str, is_inside: bool, db: Session = Depends(database.get_db)):
    visitor = crud.update_visitor_status(db, visitor_id, is_inside)
    
    if not visitor:
        return {"message": "Visitor not found"}

    try:
        await ws_manager.broadcast("sync")
    except Exception as e:
        print(f"Broadcast failed: {e}")

    return {"visitor": visitor}