# Kav1 Server

This is the backend for the Kav1 Visitor Management System, built with FastAPI and SQLite.
It provides RESTful APIs, WebSocket support, and database operations.

### Files overview

| file              	| purpose                                         	|
|-------------------	|-------------------------------------------------	|
| `main.py`           	| Entry point to launch the FastAPI app           	|
| `database.py`       	| Sets up the SQLite DB and session maker         	|
| `models.py`         	| SQLAlchemy models for Visitors and Logs         	|
| `schemas.py`        	| Pydantic models for API validation              	|
| `crud.py`           	| All database logic and queries                  	|
| `routes.py`         	| API endpoints definition (visitors, logs, etc.) 	|
| `visitor_logger.py` 	| Writes logs to DB for visitor actions           	|
| `websocket.py`      	| WebSocket endpoint and broadcast logic          	|
| `version.py`        	| -                                               	|

### Database migration steps

1. Perform changes
2. Run ``alembic revision --autogenerate -m "commit text"``
3. Run ``alembic upgrade head``
