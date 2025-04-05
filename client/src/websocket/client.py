import asyncio
import websockets
import json
from PySide6.QtCore import QObject, Signal

class WebSocketClient(QObject):
    connected = Signal()
    disconnected = Signal()
    error_occurred = Signal(str)
    visitors_updated = Signal(list)  # Emits when we get fresh visitor data

    def __init__(self):
        super().__init__()
        self.websocket = None
        self.connected_url = None

    async def connect(self, url):
        """Connect to the WebSocket server"""
        try:
            self.websocket = await websockets.connect(url)
            self.connected_url = url
            self.connected.emit()
            return True
        except Exception as e:
            self.error_occurred.emit(f"Connection error: {str(e)}")
            return False

    async def disconnect(self):
        """Disconnect from the WebSocket server"""
        if self.websocket:
            await self.websocket.close()
            self.disconnected.emit()
            self.websocket = None
            self.connected_url = None

    async def listen(self):
        """Listen for incoming messages and handle them"""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(data)
                except json.JSONDecodeError:
                    self.error_occurred.emit("Invalid JSON received")
        except Exception as e:
            if not isinstance(e, websockets.exceptions.ConnectionClosed):
                self.error_occurred.emit(f"Connection error: {str(e)}")
            await self.disconnect()

    async def handle_message(self, data):
        """Handle different message types from server"""
        if data.get('type') == 'visitorsInside':
            # Received fresh visitor data
            self.visitors_updated.emit(data.get('payload', []))
        
        elif data.get('type') == 'sync' and data.get('target') == 'getVisitorsInside':
            # Server is telling us to refresh visitor data
            await self.get_visitors_inside()

    async def get_visitors_inside(self):
        """Request current visitors inside"""
        if self.websocket:
            await self.websocket.send(json.dumps({
                'type': 'getVisitorsInside'
            }))

    async def update_visitor_status(self, visitor_id, inside):
        """Update visitor status (inside/outside)"""
        if self.websocket:
            await self.websocket.send(json.dumps({
                'type': 'updateVisitorInside',
                'payload': {
                    'id': visitor_id,
                    'inside': inside
                }
            }))