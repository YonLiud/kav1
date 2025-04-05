// src/controllers/VisitorController.ts
import { BaseController } from './base.controller';
import * as visitorHelper from '../helpers/visitor.helper';
import { sendSyncBroadcast } from '../helpers/ws.helper';

export class VisitorController extends BaseController {
  public async getVisitors() {
    try {
      const visitors = await visitorHelper.getAllVisitors();
      if (visitors.length === 0) {
        return this.sendError('NO_VISITORS_FOUND', 'No visitors found in the database');
      }
      return this.sendSuccess('VISITORS_RETRIEVED', 'Visitors fetched successfully', visitors);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return this.sendError('FETCH_VISITORS_ERROR', errorMessage);
    }
  }

  public async getVisitorsInside() {
    try {
      const visitors = await visitorHelper.getAllVisitorsInside();
      if (visitors.length === 0) {
        return this.sendError('NO_VISITORS_FOUND', 'No visitors found in the database');
      }
      return this.sendSuccess('VISITORS_RETRIEVED', 'Visitors fetched successfully', visitors);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return this.sendError('FETCH_VISITORS_ERROR', errorMessage);
    }
  }

  public async createVisitor(payload: any) {
    try {
      const newVisitor = await visitorHelper.createVisitor(payload);
      if (!newVisitor) {
        return this.sendError('VISITOR_CREATION_FAILED', 'Visitor creation failed');
      }
      return this.sendSuccess('VISITOR_CREATED', 'Visitor created successfully', newVisitor);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return this.sendError('CREATE_VISITOR_ERROR', errorMessage);
    }
  }

  public async updateVisitorInside(payload: any) {
    const { id, inside } = payload;
    try {
      const visitor = await visitorHelper.updateVisitorInside(id, inside);
      if (!visitor) {
        return this.sendError('VISITOR_UPDATE_FAILED', 'Visitor update failed');
      }
      sendSyncBroadcast('getVisitorsInside', 'Visitor updated, syncing visitors...');
      return this.sendSuccess('VISITOR_UPDATED', 'Visitor inside updated successfully', visitor);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return this.sendError('UPDATE_VISITOR_ERROR', errorMessage);
    }
  }

  public async getVisitorById(payload: any) {
    const { id } = payload;
    try {
      const visitor = await visitorHelper.getVisitorById(id);
      return this.sendSuccess('VISITOR_RETRIEVED', 'Visitor fetched successfully', visitor);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return this.sendError('FETCH_VISITOR_ERROR', errorMessage);
    }
  }
  public async getVisitorsByName(payload: any) {
    const { name } = payload;
    try {
      const visitors = await visitorHelper.getVisitorsByName(name);
      if (visitors.length === 0) {
        return this.sendError('NO_VISITORS_FOUND', 'No visitors found with that name');
      }
      return this.sendSuccess('VISITORS_RETRIEVED', 'Visitors fetched successfully', visitors);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return this.sendError('FETCH_VISITORS_ERROR', errorMessage);
    }
  }
}
