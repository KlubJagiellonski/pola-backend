export abstract class ApiConnector {
  protected readonly apiUrl: string;

  protected constructor(apiUrl: string) {
    this.apiUrl = apiUrl;
  }
}
