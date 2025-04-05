# In websocket/client.py
import asyncio
import json
import websockets
from PySide6.QtCore import QObject, Signal

class WebSocketClient(QObject):
    connected = Signal()
    disconnected = Signal()
    error_occurred = Signal(str)
    visitors_updated = Signal(list)
    # Add a signal for the request-response cycle
    request_completed = Signal(dict)

    def __init__(self):
        super().__init__()
        self.websocket = None
        self.connected_url = None
        self._response_event = asyncio.Event()
        self._last_response = None

    async def connect(self, url):
        """Connect to WebSocket server"""
        try:
            self.websocket = await websockets.connect(url, ping_interval=30)
            self.connected_url = url
            self.connected.emit()
            asyncio.create_task(self.listen())
            return True
        except Exception as e:
            self.error_occurred.emit(f"Connection error: {str(e)}")
            return False

    async def listen(self):
        """Listen for incoming messages"""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    print("Received message:", data)

                    # Handle sync messages separately
                    if data.get('type') == 'sync' and data.get('target') == 'getVisitorsInside':
                        print("Sync message received")
                        # Don't wait for response, just request new data
                        asyncio.create_task(self.get_visitors_inside())
                        continue
                    
                    # Handle visitor data responses
                    if data.get('status') == 'OK' and data.get('code') == 'VISITORS_RETRIEVED':
                        visitors = data.get('data', [])
                        if isinstance(visitors, list):
                            self.visitors_updated.emit(visitors)
                    
                    # Store the last response for request-response cycle
                    self._last_response = data
                    self._response_event.set()

                except json.JSONDecodeError:
                    self.error_occurred.emit("Invalid JSON received")
        except Exception as e:
            if not isinstance(e, (websockets.exceptions.ConnectionClosed, asyncio.CancelledError)):
                self.error_occurred.emit(f"Connection error: {str(e)}")
            await self.disconnect()

    async def get_visitors_inside(self):
        """Request and wait for visitors data"""
        if not self.websocket:
            self.error_occurred.emit("Not connected to server")
            return

        try:
            # Clear previous response
            self._response_event.clear()
            self._last_response = None
            
            # Send request
            request_data = json.dumps({
                'type': 'getVisitorsInside'
            })
            print("Sending request for visitors data:", request_data)  # Debug

            await self.websocket.send(request_data)
            print("Sent getVisitorsInside request")  # Debug

            # Wait for the response with a timeout of 10 seconds
            try:
                # The wait will now time out if the response isn't received within 10 seconds
                await asyncio.wait_for(self._response_event.wait(), timeout=10.0)
                if self._last_response and isinstance(self._last_response.get('data'), list):
                    return self._last_response['data']
                else:
                    self.error_occurred.emit("Invalid response received or no data")
                    print("Invalid response or no data in response.")  # Debug

            except asyncio.TimeoutError:
                self.error_occurred.emit("Server response timeout")
                print("Timeout occurred while waiting for visitors data")  # Debug
                return None

        except Exception as e:
            self.error_occurred.emit(f"Request error: {str(e)}")
            await self.disconnect()
            return None