// src/controllers/UserController.ts
import { BaseController } from './base.controller';
import * as userHelper from '../helpers/user.helpers';
import User from '../models/user.model';

export class UserController extends BaseController {
  public async getUsers() {
    try {
      const users = await userHelper.getAllUsers();
      if (users.length === 0) {
        return this.sendError('NO_USERS_FOUND', 'No users found in the database');
      }
      return this.sendSuccess('USERS_RETRIEVED', 'Users fetched successfully', users);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return this.sendError('FETCH_USERS_ERROR', errorMessage);
    }
  }

  public async createUser(payload: any) {
    try {
      const newUser = await User.create(payload);
      return this.sendSuccess('USER_CREATED', 'User created successfully', newUser);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return this.sendError('CREATE_USER_ERROR', errorMessage);
    }
  }

  public async updateUserInside(payload: any) {
    const { id, inside } = payload;
    try {
      const user = await userHelper.getUserById(id);
      user.inside = inside;
      await user.save();
      return this.sendSuccess('USER_UPDATED', 'User inside updated successfully', user);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return this.sendError('UPDATE_USER_ERROR', errorMessage);
    }
  }

  public async getUserById(payload: any) {
    const { id } = payload;
    try {
      const user = await userHelper.getUserById(id);
      return this.sendSuccess('USER_RETRIEVED', 'User fetched successfully', user);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return this.sendError('FETCH_USER_ERROR', errorMessage);
    }
  }
  public async getUsersByName(payload: any) {
    const { name } = payload;
    try {
      const users = await userHelper.getUsersByName(name);
      return this.sendSuccess('USERS_RETRIEVED', 'Users fetched successfully', users);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return this.sendError('FETCH_USERS_ERROR', errorMessage);
    }
  }
}
