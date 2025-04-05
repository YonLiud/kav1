import { WebSocket } from 'ws';
import User from '../models/user.model';

export const getUsers = async () => {
    return await User.findAll();
  };
  
  export const createUser = async (payload: any) => {
    console.log('📦 createUser - payload:', payload);
    return await User.create(payload);
  };
  
  export const updateUserInside = async (payload: any) => {
    const { id, inside } = payload;
    const user = await User.findByPk(id);
  
    if (!user) {
      throw new Error('User not found');
    }
  
    user.inside = inside;
    await user.save();
  
    return user;
  };