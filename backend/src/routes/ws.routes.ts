import { WebSocket } from 'ws';
import * as userController from '../controllers/user.controller';

export const handleMessage = async (ws: WebSocket, message: string) => {
    try {
        const data = JSON.parse(message);

        switch (data.type) {
        case 'getUsers':
            await userController.getUsers(ws);
            break;
        case 'createUser':
            await userController.createUser(ws, data.payload);
            break;
        case 'ping':
            userController.ping(ws);
            break;
        default:
            ws.send(JSON.stringify({ type: 'error', message: 'Unknown command' }));
    }
  } catch (err) {
    ws.send(JSON.stringify({ type: 'error', message: 'Invalid message format' }));
  }
};
