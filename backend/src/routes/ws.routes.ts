import { WebSocket } from 'ws';
import { VisitorController } from '../controllers/visitor.controller';
import * as systemController from '../controllers/system.controller';
import { getVisitorById } from '../helpers/visitor.helper';

const visitorController = new VisitorController();

type MessageHandler = (ws: WebSocket, payload?: any) => Promise<any>;

const routes: Record<string, MessageHandler> = {
  getVisitors: visitorController.getVisitors.bind(visitorController),
  getVisitorsInside: visitorController.getVisitorsInside.bind(visitorController),
  getVisitorById: visitorController.getVisitorById.bind(visitorController),
  getVisitorsByName: visitorController.getVisitorsByName.bind(visitorController),
  createVisitor: visitorController.createVisitor.bind(visitorController),
  updateVisitorInside: visitorController.updateVisitorInside.bind(visitorController),
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
