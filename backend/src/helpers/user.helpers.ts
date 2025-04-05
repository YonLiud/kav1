import { Op, where } from 'sequelize';
import User from '../models/user.model';

export const getUserById = async (id: number) => {
    const user = await User.findByPk(id);
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  };

export const getUsersByName = async (name: string) => {
  const users = await User.findAll({
    where: {
      name: {
        [Op.like]: `%${name}%`,
      },
    },
  });
  return users;
}

export const getAllUsers = async () => {
  const users = await User.findAll();
  return users;
};
