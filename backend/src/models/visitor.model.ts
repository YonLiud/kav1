import { Model, DataTypes } from 'sequelize';
import sequelize from '../config/database';

class Visitor extends Model {
  declare id: number;
  declare name: string;
  declare inside: boolean;
}

Visitor.init({
  name: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  inside: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
  }
}, { sequelize, modelName: 'visitor' });

export default Visitor;