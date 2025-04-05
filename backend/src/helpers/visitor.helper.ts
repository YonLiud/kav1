import { Op, where } from 'sequelize';
import Visitor from '../models/visitor.model';

export const createVisitor = async (visitorData: any) => {
  const visitor = await Visitor.create(visitorData);
  return visitor;
}

export const getVisitorById = async (id: number) => {
    const visitor = await Visitor.findByPk(id);
    if (!visitor) {
      throw new Error('Visitor not found');
    }
    return visitor;
  };

export const getVisitorsByName = async (name: string) => {
  const visitors = await Visitor.findAll({
    where: {
      name: {
        [Op.like]: `%${name}%`,
      },
    },
  });
  return visitors;
}

export const getAllVisitors = async () => {
  const visitors = await Visitor.findAll();
  return visitors;
};

export const getAllVisitorsInside = async () => {
  const visitors = await Visitor.findAll({
    where: {
      inside: true,
    },
  });
  return visitors;
};

export const getVisitorByVisitorId = async (visitorId: string) => {
  const visitor = await Visitor.findOne({
    where: {
      visitorId: visitorId,
    },
  });
  if (!visitor) {
    throw new Error('Visitor not found');
  }
  return visitor;
}

export const updateVisitorInside = async (visitorId: string, inside: boolean) => {
  const visitor = await getVisitorByVisitorId(visitorId);
  visitor.inside = inside;
  await visitor.save();
  return visitor;
}
