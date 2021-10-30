import { AxiosError } from 'axios';

export enum ErrorMessage {
  UNEXPECTED_ERROR = 'Unexpected error',
  FETCH_UNSUCCESSFUL = 'Cannot fetch data, check if endpoint is available',
  EMPTY_PAYLOAD = 'Obtained empty payload',
  INVALID_DATA = 'Obtained invalid data for search query',
  INVALID_REQUEST = 'Invalid request structure',
  NOT_FOUND = 'Not found',
  NETWORK_ERROR = 'Service is unreachable',
  API_ADAPTER_ERROR = 'Something unexpected happened on communication with a service.',
  SERVICE_ERROR = 'Something unexpected happened on the service. Please try again later.',
}

export abstract class ErrorHandler extends Error {
  constructor(public handledError?: unknown) {
    super();
  }

  buildMessage = (message: string): string => {
    if (this.handledError) {
      if (typeof this.handledError === 'string') {
        return message + `: ${this.handledError}`;
      } else if (this.handledError instanceof Error) {
        return message + `: ${this.handledError.message}`;
      }
    }

    return message;
  };
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
    this.message = this.buildMessage(`${apiName}: ${ErrorMessage.FETCH_UNSUCCESSFUL}`);
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
    this.message = this.buildMessage(`${dataTypeName}: ${ErrorMessage.EMPTY_PAYLOAD}`);
  }
}

export class InvalidSearchResultError extends ErrorHandler {
  /**
   * Error describes invalid data returned for valid search query
   * @param handledError Handled incoming error object
   */
  constructor(public handledError?: unknown) {
    super();
    this.name = 'Invalid search result';
    this.message = this.buildMessage(ErrorMessage.INVALID_DATA);
  }
}

export class BadRequestError extends ErrorHandler {
  /**
   * Error describes invalid request structure
   * @param handledError Handled incoming error object
   */
  constructor(public handledError?: unknown) {
    super();
    this.name = 'Bad request';
    this.message = this.buildMessage(ErrorMessage.INVALID_REQUEST);
  }
}

export class MethodNotFoundError extends ErrorHandler {
  /**
   * Error describes "NOT FOUND" case
   * @param handledError Handled incoming error object
   */
  constructor(public handledError?: unknown) {
    super();
    this.name = 'Method not found';
    this.message = this.buildMessage(ErrorMessage.NOT_FOUND);
  }
}

export function isEmptyQueryError(error: AxiosError) {
  const data = error.response?.data;
  return data && data.status === 400 && data.type === 'about:blank';
}

export class ApiAdapterError extends ErrorHandler {
  constructor(public apiName: string, public handledError?: unknown) {
    super();
    this.name = 'API adapter error';
    this.message = this.buildMessage(`${this.apiName}: ${ErrorMessage.API_ADAPTER_ERROR}`);
  }
}

export class InternalServiceError extends ErrorHandler {
  /**
   * Error describes error incoming from a service side
   * @param handledError Handled incoming error object
   */
  constructor(public handledError?: unknown) {
    super();
    this.name = 'Internal service error';
    this.message = this.buildMessage(ErrorMessage.SERVICE_ERROR);
  }
}

export class NetworkError extends ErrorHandler {
  /**
   * Error describes network problem
   * @param handledError Handled incoming error object
   */
  constructor(public handledError?: unknown) {
    super();
    this.name = 'Network error';
    this.message = this.buildMessage(ErrorMessage.NETWORK_ERROR);
  }
}
