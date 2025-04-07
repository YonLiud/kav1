from sqlalchemy import Column, Integer, String, Boolean, JSON
from .database import Base

class Visitor(Base):
    __tablename__ = "visitors"

    dbid = Column("dbid", Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    visitorid = Column(String, unique=True, index=True, nullable=False)
    inside = Column(Boolean, default=False, nullable=False)
    properties = Column("properties", JSON, nullable=True)
