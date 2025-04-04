import { WebSocketServer } from 'ws';
import sequelize from './config/database';
import { handleMessage } from './routes/ws.routes';

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 3000;
const wss = new WebSocketServer({ port: PORT });

sequelize.sync().then(() => {
  console.log(`✅ WebSocket server running on ws://localhost:${PORT}`);
});

wss.on('connection', (ws) => {
  console.log('🔌 New client connected');

  ws.on('message', (message: string) => handleMessage(ws, message));
  ws.on('close', () => console.log('❌ Client disconnected'));
});
