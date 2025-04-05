import { WebSocket } from 'ws';
import { UserController } from '../controllers/user.controller';
import * as systemController from '../controllers/system.controller';
import { getUserById } from '../helpers/user.helpers';

const userController = new UserController();  // Instantiate the controller

type MessageHandler = (ws: WebSocket, payload?: any) => Promise<any>;

const routes: Record<string, MessageHandler> = {
  getUsers: userController.getUsers.bind(userController),
  getUserById: userController.getUserById.bind(userController),
  getUsersByName: userController.getUsersByName.bind(userController),
  createUser: userController.createUser.bind(userController),
  updateUserInside: userController.updateUserInside.bind(userController),
  ping: systemController.ping,
};

export const handleMessage = async (ws: WebSocket, message: string) => {
  try {
    const { type, payload } = JSON.parse(message);
    
    console.log('📦 type:', type);
    console.log('📦 payload:', payload);

    const handler = routes[type];
    if (!handler) {
      return ws.send(JSON.stringify({
        status: 'error',
        code: 'UNKNOWN_COMMAND',
        message: 'Unknown command',
      }));
    }

    const result = await handler(payload);

    ws.send(JSON.stringify(result));

  } catch (err: unknown) {
    const errorMessage = err instanceof Error ? err.message : 'Unknown error';
    ws.send(JSON.stringify({
      status: 'error',
      code: 'SERVER_ERROR',
      message: errorMessage,
    }));
  }
};
