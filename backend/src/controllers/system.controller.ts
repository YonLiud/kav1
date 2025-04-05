import { sendSyncBroadcast } from "../helpers/ws.helper";

export const ping = (): any => {
  return { type: 'pong' };
};

export const fakesync =(): any => {
  sendSyncBroadcast('getVisitorsInside', 'Visitor updated, syncing visitors...');
  return { type: "OK"}
}