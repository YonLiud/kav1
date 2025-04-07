from sqlalchemy import Column, Integer, String, Boolean, JSON
from .database import Base

class Visitor(Base):
    __tablename__ = "visitors"

    dbid = Column("dbid", Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    visitorid = Column(String, unique=True, index=True)
    inside = Column(Boolean, default=False)
    properties = Column("properties", JSON, nullable=True)
