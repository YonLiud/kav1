import { WebSocket } from 'ws';
import * as userController from '../controllers/user.controller';
import * as systemController from '../controllers/system.controller'

type MessageHandler = (ws: WebSocket, payload?: any) => void | Promise<void>;

const routes: Record<string, MessageHandler> = {
  getUsers: userController.getUsers,
  createUser: userController.createUser,
  ping: systemController.ping,
};

export const handleMessage = async (ws: WebSocket, message: string) => {
  try {
    const { type, payload } = JSON.parse(message);

    const handler = routes[type];
    if (!handler) {
      return ws.send(JSON.stringify({ type: 'error', message: 'Unknown command' }));
    }

    await handler(ws, payload);
  } catch (err) {
    ws.send(JSON.stringify({ type: 'error', message: 'Invalid message format' }));
  }
};
