export class BaseController {
    protected sendSuccess(code: string, msg: string, data?: any) {
      return {
        status: 'OK',
        code,
        message: msg,
        data,
      };
    }
  
    protected sendError(code: string, msg: string) {
      return {
        status: 'ERROR',
        code,
        message: msg,
      };
    }
  }
  