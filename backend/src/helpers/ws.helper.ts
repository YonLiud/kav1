import { WebSocket, WebSocketServer } from 'ws';

const clients = new Set<WebSocket>();

export const setupWebSocket = (wss: WebSocketServer) => {
    wss.on('connection', (ws) => {
      clients.add(ws);
      ws.on('close', () => clients.delete(ws));
    });
};

export const broadcast = (msg: object) => {
    const json = JSON.stringify(msg);
    clients.forEach((ws) => {
        if (ws.readyState === ws.OPEN) {
            ws.send(json);
        }
    });
};

export const sendSyncBroadcast = (target: string, message: string) => {
    setImmediate(() => {
      broadcast({
        type: 'sync',
        target: target,
        message: message,
      });
    });
  };