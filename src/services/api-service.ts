export abstract class ApiService {
  protected readonly apiUrl: string;

  protected constructor(apiUrl: string) {
    this.apiUrl = apiUrl;
  }
}
