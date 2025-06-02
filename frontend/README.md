# Kav1 Frontend

The frontend is built using PySide6 to provide a modern desktop interface.
It connects to the FastAPI backend via HTTP and WebSocket for real-time updates.
Features include visitor creation, live status updates, search, and log viewing.

## Files Overview

### ``/``

| file             | purpose                                           |
| ---------------- | ------------------------------------------------- |
| `main.py`        | Entry point for launching the PySide6 app         |
| `main.spec`      | PyInstaller spec file for building the executable |
| `clienticon.ico` | App icon                                          |


### ``app/core/``
| file            | purpose                                 |
| --------------- | --------------------------------------- |
| `api_client.py` | Handles all API requests to the backend |
| `settings.py`   | Stores and loads connection settings    |
| `ws_client.py`  | Handles WebSocket communication         |


### ``app/utils/``

| file     | purpose                           |
| -------- | --------------------------------- |
| `log.py` | Local logging for frontend events |

### ``app/views``

| file                   | purpose                                  |
| ---------------------- | ---------------------------------------- |
| `main_window.py`       | Main window layout and app logic         |
| `connection_dialog.py` | Dialog to set and test server connection |

### ``app/views/common/``

| file                | purpose                            |
| ------------------- | ---------------------------------- |
| `warning_dialog.py` | Displays warning or error messages |


### ``app/views/logs``

| file             | purpose                       |
| ---------------- | ----------------------------- |
| `logs_dialog.py` | Shows visitor or general logs |

### ``app/views/search``

| file                      | purpose                       |
| ------------------------- | ----------------------------- |
| `search_dialog.py`        | Input dialog for search query |
| `search_result_dialog.py` | Displays search results       |

### ``app/views/visitor``

| file                        | purpose                            |
| --------------------------- | ---------------------------------- |
| `create_visitor_dialog.py`  | Dialog for adding a new visitor    |
| `visitor_details_dialog.py` | View and update info for a visitor |

### ``