from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from . import crud, schemas, database, websocket
from .visitor_logger import VisitorLogger

router = APIRouter()
ws_manager = websocket.WebSocketManager()
visitor_logger = VisitorLogger()

# ? Websocket Routes


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.send_personal_message(data, websocket)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


# ? HTTP Routes


@router.get("/visitors")
def get_visitors(db: Session = Depends(database.get_db)):
    return crud.get_visitors(db)


@router.get("/visitors/inside")
def get_visitors_inside(db: Session = Depends(database.get_db)):
    visitors = crud.get_visitors_inside(db)
    result = []
    for v in visitors:
        latest_log = crud.get_latest_log_for_visitor(db, v.dbid)
        action = None
        if latest_log:
            action = {latest_log.action: latest_log.timestamp.isoformat()}
        visitor_data = {
            "inside": v.inside,
            "dbid": v.dbid,
            "name": v.name,
            "visitorid": v.visitorid,
            "properties": v.properties or {},
            "action": action,
        }
        result.append(visitor_data)
    return result


@router.post("/visitor")
def add_visitor(visitor: schemas.VisitorCreate, db: Session = Depends(database.get_db)):
    db_visitor = crud.create_visitor(
        db=db,
        name=visitor.name,
        visitorid=visitor.visitorid,
        properties=visitor.properties,
    )
    if db_visitor:
        visitor_logger.log_event(
            event_type="CREATE",
            visitor_id=db_visitor.visitorid,
            visitor_name=db_visitor.name,
            additional_info=f"Properties: {db_visitor.properties}",
        )
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
async def change_status(
    visitor_id: str, is_inside: bool, db: Session = Depends(database.get_db)
):
    visitor = crud.update_visitor_status(db, visitor_id, is_inside)

    if not visitor:
        return {"message": "Visitor not found"}

    event_type = "ENTRY" if is_inside else "EXIT"
    visitor_logger.log_event(
        event_type=event_type, visitor_id=visitor.visitorid, visitor_name=visitor.name
    )

    try:
        await ws_manager.broadcast("sync")
    except Exception as e:
        print(f"Broadcast failed: {e}")

    return {"visitor": visitor}


@router.post("/visitors/{visitor_id}/delete")
async def delete_visitor(visitor_id: str, db: Session = Depends(database.get_db)):
    visitor = crud.delete_visitor(db, visitor_id)

    if not visitor:
        return {"message": "Visitor not found"}

    visitor_logger.log_event(
        event_type="DELETE", visitor_id=visitor.visitorid, visitor_name=visitor.name
    )

    try:
        await ws_manager.broadcast("sync")
    except Exception as e:
        print(f"Broadcast failed: {e}")

    return {"message": "Visitor deleted successfully", "visitor": visitor}


@router.get("/logs")
def get_all_logs(db: Session = Depends(database.get_db)):
    return crud.get_all_logs(db)


@router.get("/logs/{visitor_id}")
def get_logs_for_visitor(visitor_id: str, db: Session = Depends(database.get_db)):
    logs = crud.get_logs_for_visitor(db, visitor_id)
    if logs:
        return logs
    else:
        raise HTTPException(status_code=404, detail="No logs found for this visitor")
