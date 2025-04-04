import { Sequelize } from 'sequelize';

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: './database.sqlite',
  logging: console.log,
});

export const connectDB = async () => {
  try {
    await sequelize.authenticate();
    console.log('✅ Connected to SQLite');
  } catch (error) {
    console.error('❌ DB connection failed:', error);
  }
};

export default sequelize;
