from sqlalchemy.orm import Session
from . import models

def get_visitors_inside(db: Session):
    return db.query(models.Visitor).filter(models.Visitor.inside == True).all()

def create_visitor(db: Session, name: str, visitorid: str, inside: bool, properties: dict):
    db_visitor = models.Visitor(name=name, visitorid=visitorid, inside=inside, properties=properties)
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor