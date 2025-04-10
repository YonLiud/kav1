# Kav1 Visitor Management System

Kav1 is a visitor management system with a PySide6 frontend and FastAPI backend. It offers real-time updates via WebSocket and a user-friendly interface for managing visitor data.

## Features

### Frontend
- **Visitor Management**: Add, search, update, and delete visitor records.
- **Real-Time Updates**: Automatically sync visitor data using WebSocket communication.
- **Dialogs**: Intuitive dialogs for creating visitors, searching, and viewing visitor details.
- **Dark Mode Support**: Enhanced UI with dark mode compatibility.
- **Standalone Executable**: Built using PyInstaller for easy deployment.

### Backend
- **FastAPI Framework**: A robust and scalable backend for handling visitor data.
- **SQLite Database**: Lightweight database for storing visitor information.
- **WebSocket Support**: Real-time communication for syncing visitor data.
- **Logging**: Logs visitor events (e.g., entry, exit, creation, deletion) for auditing purposes.
- **REST API**: Exposes endpoints for managing visitor data.

### Installer
- **Inno Setup**: Generates a Windows installer for easy installation of the application.

## Installation

### Prerequisites
- Python 3.11 or higher
- SQLite (pre-installed with Python)
- Node.js (optional, for frontend development)
- Inno Setup (for building the installer)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/YonLiud/kav1.git
   cd kav1
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Running the backend
1. Navigate to the backend directory and start the server
```bash
cd backend
python server.py --host 0.0.0.0 --port 3000
```
2. Navigate to the frontend directory and start the client
```bash
cd frontend
python main.py
```

## API Endpoints

### Visitors
- **GET /visitors**  
    Retrieve all visitors.

- **GET /visitors/inside**  
    Retrieve visitors currently inside the facility.

- **POST /visitor**  
    Add a new visitor.  
    **Request Body**:  
    ```json
    {
        "name": "John Doe",
        "visitorid": "12345",
    }
    ```
- **GET /visitors/{visitor_id}**
    Retrieve a visitor by their unique ID.

- **POST /visitors/{visitor_id/status}**
    Update a visitor's status (e.g., mark as inside or outside).
    **Request Body**:
    ```json
    {
    "status": "inside"
    }
    ```

- **POST /visitors/{visitor_id}/delete**
    Delete a visitor by their unique ID.

WebSocket
- **ws://\<host>:\<port>/ws**
WebSocket endpoint for real-time updates on visitor data.

## Logging

Visitor events (e.g., entry, exit, creation, deletion) are logged in the ``visitor_logs`` directory. Logs are organized by date and are saved in a `.csv` format

## Build
To build the program and the installer for it:

1. Build the executables:
```bash
.\build_windows.bat
```

2. Build the installer using Inno Setup
```bash
"ISCC.exe kav1.iss
```

## License

This project is licensed under the [GNU General Public License (GPL)](https://www.gnu.org/licenses/gpl-3.0.html). You are free to use, modify, and distribute the project under the terms of this license.