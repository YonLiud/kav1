import { WebSocket } from 'ws';
import User from '../models/user.model';

export const getUsers = async (ws: WebSocket) => {
    const users = await User.findAll();
    ws.send(JSON.stringify({ type: 'users', data: users }));
};

export const createUser = async (ws: WebSocket, payload: any) => {
    const user = await User.create(payload);
    ws.send(JSON.stringify({ type: 'userCreated', data: user }));
};