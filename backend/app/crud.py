from sqlalchemy.orm import Session
from . import models

def get_visitors_inside(db: Session):
    return db.query(models.Visitor).filter(models.Visitor.inside == True).all()

def create_visitor(db: Session, name: str, visitorid: str, properties: dict):
    db_visitor = models.Visitor(name=name, visitorid=visitorid, inside=False, properties=properties)
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor

def update_visitor_status(db: Session, visitor_id: str, is_inside: bool):
    visitor = db.query(models.Visitor).filter(models.Visitor.visitor_id == visitor_id).first()
    
    if visitor:
        visitor.inside = is_inside
        db.commit()
        db.refresh(visitor)
        return visitor
    return None

def get_visitor_by_id(db: Session, visitor_id: str):
    return db.query(models.Visitor).filter(models.Visitor.visitorid == visitor_id).first()

def search_visitors_by_name(db: Session, search_query: str):
    return db.query(models.Visitor).filter(models.Visitor.name.ilike(f"%{search_query}%")).all()