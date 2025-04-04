import { WebSocket } from 'ws';

export const ping = (ws: WebSocket) => {
    ws.send(JSON.stringify({ type: 'pong' }));
}; 
