import { Model, DataTypes } from 'sequelize';
import sequelize from '../config/database';

class User extends Model {
  declare id: number;
  declare name: string;
}

User.init({
  name: DataTypes.STRING
}, { sequelize, modelName: 'user' });

export default User;