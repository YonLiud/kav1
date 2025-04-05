export class BaseController {
  protected sendSuccess(code: string, msg: string, data?: any) {
    console.log(`Sending success response with code: ${code}, message: ${msg}`);  // This will print your desired info
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
