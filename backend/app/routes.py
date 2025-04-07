# routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, schemas, database

router = APIRouter()

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
