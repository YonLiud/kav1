import User from '../models/user.model';

export const getUserById = async (id: number) => {
    const user = await User.findByPk(id);
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  };