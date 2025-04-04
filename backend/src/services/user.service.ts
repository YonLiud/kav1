import User from '../models/user.model';

export class UserService {
  static async create(name: string) {
    return await User.create({ name });
  }

  static async list() {
    return await User.findAll();
  }
}