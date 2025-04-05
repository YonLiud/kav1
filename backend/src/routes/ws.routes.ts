import { WebSocket } from 'ws';
import * as userController from '../controllers/user.controller';
import * as systemController from '../controllers/system.controller';

type MessageHandler = (ws: WebSocket, payload?: any) => Promise<any>;

const routes: Record<string, MessageHandler> = {
  getUsers: userController.getUsers,
  createUser: userController.createUser,
  updateUserInside: userController.updateUserInside,
  ping: systemController.ping,
};

export const handleMessage = async (ws: WebSocket, message: string) => {
  console.log('📦 message:', message);
  try {
    const { type, payload } = JSON.parse(message);
    
    console.log('📦 type:', type);
    console.log('📦 payload:', payload);

    const handler = routes[type];
    if (!handler) {
      return ws.send(JSON.stringify({ type: 'error', message: 'Unknown command' }));
    }

    const result = await handler(payload);

    if (result) {
      ws.send(JSON.stringify({ type: `${type}Success`, data: result }));
    }
  } catch (err: unknown) {
    const errorMessage = err instanceof Error ? err.message : 'Unknown error';
    ws.send(JSON.stringify({ type: 'error', message: errorMessage }));
  }
};