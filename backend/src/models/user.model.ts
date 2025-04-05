import { Model, DataTypes } from 'sequelize';
import sequelize from '../config/database';

class User extends Model {
  declare id: number;
  declare name: string;
  declare inside: boolean;
}

User.init({
  name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  inside: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
  }
}, { sequelize, modelName: 'user' });

export default User;