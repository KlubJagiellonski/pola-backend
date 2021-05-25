export abstract class ErrorHandler extends Error {
  constructor(public handledError?: unknown) {
    super();
  }

  buildMessage(message: string): string {
    if (this.handledError) {
      return message + `: ${this.handledError}`;
    }
    return message;
  }
}

export class FetchError extends ErrorHandler {
  /**
   * Generic error for fetching data from outside data source
   * @param dataTypeName Name of data to be fetched
   * @param apiName Name of end point
   * @param handledError Handled incoming error object
   */
  constructor(apiName: string, public handledError?: unknown) {
    super();
    this.name = 'Fetch Error';
    this.message = this.buildMessage(`Cannot fetch data. Check if ${apiName} is available`);
  }
}

export class EmptyResponseDataError extends ErrorHandler {
  /**
   * Generic error for retrieving undefined data from outside data source
   * @param dataTypeName Name of data to be fetched
   * @param handledError Handled incoming error object
   */
  constructor(dataTypeName: string, public handledError?: unknown) {
    super();
    this.name = 'Empty Response Error';
    this.message = this.buildMessage(`Obtained empty ${dataTypeName} collection`);
  }
}
