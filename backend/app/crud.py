from sqlalchemy.orm import Session
from . import models


def get_visitors(db: Session):
    return db.query(models.Visitor).all()


def get_visitors_inside(db: Session):
    return db.query(models.Visitor).filter(models.Visitor.inside).all()


def create_visitor(db: Session, name: str, visitorid: str, properties: dict):
    db_visitor = models.Visitor(
        name=name, visitorid=visitorid, inside=False, properties=properties
    )
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)

    log_visitor_action(db, db_visitor.dbid, "creation")

    return db_visitor


def update_visitor_status(db: Session, visitor_id: str, is_inside: bool):
    visitor = (
        db.query(models.Visitor).filter(models.Visitor.visitorid == visitor_id).first()
    )

    if visitor:
        visitor.inside = is_inside
        db.commit()
        db.refresh(visitor)
        log_visitor_action(db, visitor.dbid, "entry" if is_inside else "exit")
        return visitor
    return None


def delete_visitor(db: Session, visitor_id: str):
    visitor = (
        db.query(models.Visitor).filter(models.Visitor.visitorid == visitor_id).first()
    )

    if visitor:
        db.delete(visitor)
        db.commit()
        return visitor
    return None


def get_visitor_by_id(db: Session, visitor_id: str):
    return (
        db.query(models.Visitor).filter(models.Visitor.visitorid == visitor_id).first()
    )


def get_visitor_by_dbid(db: Session, visitor_dbid: int):
    return db.query(models.Visitor).filter(models.Visitor.dbid == visitor_dbid).first()


def search_visitors_by_name(db: Session, search_query: str):
    return (
        db.query(models.Visitor)
        .filter(models.Visitor.name.ilike(f"%{search_query}%"))
        .all()
    )


def log_visitor_action(db: Session, visitor_dbid: int, action: str):
    log = models.VisitorLog(
        visitor_dbid=visitor_dbid,
        action=action,
    )
    db.add(log)
    db.commit()
    db.refresh(log)


def get_latest_log_for_visitor(db: Session, visitor_dbid: int):
    return (
        db.query(models.VisitorLog)
        .filter(models.VisitorLog.visitor_dbid == visitor_dbid)
        .order_by(models.VisitorLog.timestamp.desc())
        .first()
    )


def get_logs(db: Session, limit: int = 20):
    return (
        db.query(models.VisitorLog)
        .order_by(models.VisitorLog.timestamp.desc())
        .limit(limit)
        .all()
    )


def get_logs_for_visitor(db: Session, dbid: int):
    return (
        db.query(models.VisitorLog)
        .filter(models.VisitorLog.visitor_dbid == dbid)
        .order_by(models.VisitorLog.timestamp.desc())
        .all()
    )
